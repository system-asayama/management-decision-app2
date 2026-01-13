"""
Excel読み取りAPI
運転資金・回転期間・資金繰り前提をExcelから読み取る
"""
from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
import openpyxl
import os
import tempfile

from app.db import SessionLocal
from app.models import User, ROLES
from app.decorators import require_roles
from ..models_decision import Company, FiscalYear
from ..utils.excel_import_helpers import import_working_capital_and_debt_assumptions


bp = Blueprint('excel_import', __name__, url_prefix='/decision/excel-import')


@bp.route('/working-capital-and-debt', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def import_working_capital_and_debt():
    """
    運転資金前提と返済スケジュール前提をExcelから読み取る
    
    リクエスト:
        - file: Excelファイル（multipart/form-data）
        - company_id: 企業ID
        - fiscal_year_ids: 会計年度IDのリスト（カンマ区切り）
    
    レスポンス:
        - working_capital_assumptions: 運転資金前提のリスト
        - debt_repayment_assumptions: 返済スケジュール前提のリスト
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    # パラメータを取得
    company_id = request.form.get('company_id', type=int)
    fiscal_year_ids_str = request.form.get('fiscal_year_ids', '')
    
    if not company_id:
        return jsonify({'error': '企業IDを指定してください'}), 400
    
    if not fiscal_year_ids_str:
        return jsonify({'error': '会計年度IDのリストを指定してください'}), 400
    
    try:
        fiscal_year_ids = [int(fid.strip()) for fid in fiscal_year_ids_str.split(',')]
        if len(fiscal_year_ids) != 3:
            return jsonify({'error': '会計年度IDは3つ指定してください（初年度、2年度、3年度）'}), 400
    except ValueError:
        return jsonify({'error': '会計年度IDの形式が不正です'}), 400
    
    # ファイルを取得
    if 'file' not in request.files:
        return jsonify({'error': 'ファイルがアップロードされていません'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'ファイルが選択されていません'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': 'Excelファイル（.xlsx または .xls）をアップロードしてください'}), 400
    
    db = SessionLocal()
    try:
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 会計年度情報を取得
        for fiscal_year_id in fiscal_year_ids:
            fiscal_year = db.query(FiscalYear).filter(
                FiscalYear.id == fiscal_year_id,
                FiscalYear.company_id == company_id
            ).first()
            
            if not fiscal_year:
                return jsonify({'error': f'会計年度ID {fiscal_year_id} が見つかりません'}), 404
        
        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # Excelファイルを読み込む
            wb = openpyxl.load_workbook(tmp_path, data_only=True)
            
            # データをインポート
            results = import_working_capital_and_debt_assumptions(
                wb, company_id, fiscal_year_ids, db
            )
            
            return jsonify({
                'message': 'インポート成功',
                'working_capital_assumptions': results['working_capital_assumptions'],
                'debt_repayment_assumptions': results['debt_repayment_assumptions'],
                'validation': results.get('validation', {'valid': True, 'errors': [], 'warnings': []})
            })
        finally:
            # 一時ファイルを削除
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/working-capital/<int:fiscal_year_id>', methods=['GET'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def get_working_capital_assumption(fiscal_year_id):
    """
    運転資金前提を取得
    
    パラメータ:
        - fiscal_year_id: 会計年度ID
    
    レスポンス:
        - 運転資金前提データ
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    db = SessionLocal()
    try:
        from ..models_decision import WorkingCapitalAssumption
        
        # 会計年度情報を取得
        fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == fiscal_year_id
        ).first()
        
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == fiscal_year.company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 運転資金前提を取得
        assumption = db.query(WorkingCapitalAssumption).filter(
            WorkingCapitalAssumption.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not assumption:
            return jsonify({'error': '運転資金前提が見つかりません'}), 404
        
        return jsonify({
            'id': assumption.id,
            'company_id': assumption.company_id,
            'fiscal_year_id': assumption.fiscal_year_id,
            'cash_turnover_period': float(assumption.cash_turnover_period) if assumption.cash_turnover_period else None,
            'receivables_turnover_period': float(assumption.receivables_turnover_period) if assumption.receivables_turnover_period else None,
            'inventory_turnover_period': float(assumption.inventory_turnover_period) if assumption.inventory_turnover_period else None,
            'payables_turnover_period': float(assumption.payables_turnover_period) if assumption.payables_turnover_period else None,
            'cash_increase': float(assumption.cash_increase) if assumption.cash_increase else None,
            'receivables_increase': float(assumption.receivables_increase) if assumption.receivables_increase else None,
            'inventory_increase': float(assumption.inventory_increase) if assumption.inventory_increase else None,
            'payables_increase': float(assumption.payables_increase) if assumption.payables_increase else None
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/debt-repayment/<int:fiscal_year_id>', methods=['GET'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def get_debt_repayment_assumption(fiscal_year_id):
    """
    返済スケジュール前提を取得
    
    パラメータ:
        - fiscal_year_id: 会計年度ID
    
    レスポンス:
        - 返済スケジュール前提データ
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    db = SessionLocal()
    try:
        from ..models_decision import DebtRepaymentAssumption
        
        # 会計年度情報を取得
        fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == fiscal_year_id
        ).first()
        
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == fiscal_year.company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 返済スケジュール前提を取得
        assumption = db.query(DebtRepaymentAssumption).filter(
            DebtRepaymentAssumption.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not assumption:
            return jsonify({'error': '返済スケジュール前提が見つかりません'}), 404
        
        return jsonify({
            'id': assumption.id,
            'company_id': assumption.company_id,
            'fiscal_year_id': assumption.fiscal_year_id,
            'beginning_balance': float(assumption.beginning_balance) if assumption.beginning_balance else None,
            'borrowing_amount': float(assumption.borrowing_amount) if assumption.borrowing_amount else None,
            'principal_repayment': float(assumption.principal_repayment) if assumption.principal_repayment else None,
            'ending_balance': float(assumption.ending_balance) if assumption.ending_balance else None,
            'interest_payment': float(assumption.interest_payment) if assumption.interest_payment else None,
            'average_interest_rate': float(assumption.average_interest_rate) if assumption.average_interest_rate else None
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/monthly-cash-flow-plan', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def import_monthly_cash_flow_plan():
    """
    資金繰り計画の月次データをExcelから読み取る
    
    リクエスト:
        - file: Excelファイル（multipart/form-data）
        - company_id: 企業ID
        - fiscal_year_ids: 会計年度IDのリスト（カンマ区切り、3つ）
    
    レスポンス:
        - インポート結果
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    # パラメータを取得
    company_id = request.form.get('company_id', type=int)
    fiscal_year_ids_str = request.form.get('fiscal_year_ids', '')
    
    if not company_id:
        return jsonify({'error': '企業IDを指定してください'}), 400
    
    if not fiscal_year_ids_str:
        return jsonify({'error': '会計年度IDのリストを指定してください'}), 400
    
    try:
        fiscal_year_ids = [int(fid.strip()) for fid in fiscal_year_ids_str.split(',')]
        if len(fiscal_year_ids) != 3:
            return jsonify({'error': '会計年度IDは3つ指定してください（初年度、2年度、3年度）'}), 400
    except ValueError:
        return jsonify({'error': '会計年度IDの形式が不正です'}), 400
    
    # ファイルを取得
    if 'file' not in request.files:
        return jsonify({'error': 'ファイルがアップロードされていません'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'ファイルが選択されていません'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': 'Excelファイル（.xlsx または .xls）をアップロードしてください'}), 400
    
    db = SessionLocal()
    try:
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 会計年度情報を取得
        for fiscal_year_id in fiscal_year_ids:
            fiscal_year = db.query(FiscalYear).filter(
                FiscalYear.id == fiscal_year_id,
                FiscalYear.company_id == company_id
            ).first()
            
            if not fiscal_year:
                return jsonify({'error': f'会計年度ID {fiscal_year_id} が見つかりません'}), 404
        
        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # Excelファイルを読み込む
            wb = openpyxl.load_workbook(tmp_path, data_only=True)
            
            # データをインポート
            from ..utils.monthly_cash_flow_import import import_monthly_cash_flow_plans
            results = import_monthly_cash_flow_plans(wb, company_id, fiscal_year_ids, db)
            
            return jsonify({
                'message': 'インポート成功',
                'results': results
            })
        finally:
            # 一時ファイルを削除
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/monthly-cash-flow-plan/<int:fiscal_year_id>', methods=['GET'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def get_monthly_cash_flow_plan(fiscal_year_id):
    """
    資金繰り計画の月次データを取得
    
    パラメータ:
        - fiscal_year_id: 会計年度ID
    
    レスポンス:
        - 月次データのリスト（12ヶ月分）
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    db = SessionLocal()
    try:
        # 会計年度情報を取得
        fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == fiscal_year_id
        ).first()
        
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == fiscal_year.company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 月次データを取得
        from ..utils.monthly_cash_flow_import import get_monthly_cash_flow_plan
        monthly_data = get_monthly_cash_flow_plan(company.id, fiscal_year_id, db)
        
        return jsonify({
            'company_id': company.id,
            'company_name': company.name,
            'fiscal_year_id': fiscal_year_id,
            'fiscal_year_name': fiscal_year.year_name,
            'monthly_data': monthly_data
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
