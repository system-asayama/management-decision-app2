"""
運転資金予測API
Excel読み取りで取得した運転資金前提を使用して、将来の運転資金を予測
"""
from flask import Blueprint, request, jsonify, session

from app.db import SessionLocal
from app.models import ROLES
from app.decorators import require_roles
from ..models_decision import Company, FiscalYear
from ..utils.working_capital_forecasting import (
    forecast_working_capital_from_assumptions,
    forecast_multi_year_working_capital,
    calculate_cash_flow_impact,
    forecast_debt_repayment_schedule,
    forecast_multi_year_debt_repayment
)


bp = Blueprint('working_capital_forecast', __name__, url_prefix='/decision/working-capital-forecast')


@bp.route('/single', methods=['GET'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def forecast_single_year():
    """
    単年度の運転資金を予測
    
    パラメータ:
        - fiscal_year_id: 会計年度ID
    
    レスポンス:
        - 運転資金予測結果
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    fiscal_year_id = request.args.get('fiscal_year_id', type=int)
    
    if not fiscal_year_id:
        return jsonify({'error': '会計年度IDを指定してください'}), 400
    
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
        
        # 運転資金を予測
        result = forecast_working_capital_from_assumptions(fiscal_year_id, db)
        
        return jsonify(result)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/multi-year', methods=['GET'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def forecast_multi_year():
    """
    複数年度の運転資金を予測
    
    パラメータ:
        - company_id: 企業ID
        - fiscal_year_ids: 会計年度IDのリスト（カンマ区切り）
    
    レスポンス:
        - 運転資金予測結果のリスト
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    company_id = request.args.get('company_id', type=int)
    fiscal_year_ids_str = request.args.get('fiscal_year_ids', '')
    
    if not company_id:
        return jsonify({'error': '企業IDを指定してください'}), 400
    
    if not fiscal_year_ids_str:
        return jsonify({'error': '会計年度IDのリストを指定してください'}), 400
    
    try:
        fiscal_year_ids = [int(fid.strip()) for fid in fiscal_year_ids_str.split(',')]
    except ValueError:
        return jsonify({'error': '会計年度IDの形式が不正です'}), 400
    
    db = SessionLocal()
    try:
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 複数年度の運転資金を予測
        results = forecast_multi_year_working_capital(fiscal_year_ids, db)
        
        return jsonify({
            'company_id': company_id,
            'company_name': company.company_name,
            'forecasts': results
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/cash-flow-impact', methods=['GET'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def get_cash_flow_impact():
    """
    運転資金変動がキャッシュフローに与える影響を計算
    
    パラメータ:
        - fiscal_year_id: 会計年度ID
    
    レスポンス:
        - キャッシュフロー影響額
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    fiscal_year_id = request.args.get('fiscal_year_id', type=int)
    
    if not fiscal_year_id:
        return jsonify({'error': '会計年度IDを指定してください'}), 400
    
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
        
        # キャッシュフロー影響を計算
        result = calculate_cash_flow_impact(fiscal_year_id, db)
        
        return jsonify(result)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/debt-repayment/single', methods=['GET'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def forecast_debt_single_year():
    """
    単年度の返済計画を予測
    
    パラメータ:
        - fiscal_year_id: 会計年度ID
    
    レスポンス:
        - 返済計画予測結果
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    fiscal_year_id = request.args.get('fiscal_year_id', type=int)
    
    if not fiscal_year_id:
        return jsonify({'error': '会計年度IDを指定してください'}), 400
    
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
        
        # 返済計画を予測
        result = forecast_debt_repayment_schedule(fiscal_year_id, db)
        
        return jsonify(result)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/debt-repayment/multi-year', methods=['GET'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def forecast_debt_multi_year():
    """
    複数年度の返済計画を予測
    
    パラメータ:
        - company_id: 企業ID
        - fiscal_year_ids: 会計年度IDのリスト（カンマ区切り）
    
    レスポンス:
        - 返済計画予測結果のリスト
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    company_id = request.args.get('company_id', type=int)
    fiscal_year_ids_str = request.args.get('fiscal_year_ids', '')
    
    if not company_id:
        return jsonify({'error': '企業IDを指定してください'}), 400
    
    if not fiscal_year_ids_str:
        return jsonify({'error': '会計年度IDのリストを指定してください'}), 400
    
    try:
        fiscal_year_ids = [int(fid.strip()) for fid in fiscal_year_ids_str.split(',')]
    except ValueError:
        return jsonify({'error': '会計年度IDの形式が不正です'}), 400
    
    db = SessionLocal()
    try:
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 複数年度の返済計画を予測
        results = forecast_multi_year_debt_repayment(fiscal_year_ids, db)
        
        return jsonify({
            'company_id': company_id,
            'company_name': company.company_name,
            'forecasts': results
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
