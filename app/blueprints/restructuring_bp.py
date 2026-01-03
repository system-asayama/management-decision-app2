"""
財務諸表組換えAPI Blueprint
標準的な財務諸表を経営分析用の組換え財務諸表に変換する
"""
from flask import Blueprint, request, jsonify
from app.db import SessionLocal
from app.models_decision import (
    FiscalYear, ProfitLossStatement, BalanceSheet,
    RestructuredPL, RestructuredBS
)
from app.services.restructuring_service import RestructuringService
from datetime import datetime

restructuring_bp = Blueprint('restructuring', __name__, url_prefix='/api/restructuring')


@restructuring_bp.route('/pl/<int:fiscal_year_id>', methods=['POST'])
def restructure_and_save_pl(fiscal_year_id):
    """
    損益計算書を組換えて保存
    
    標準的なP/Lデータから組換えP/Lを生成し、データベースに保存する
    """
    data = request.get_json() or {}
    
    db = SessionLocal()
    try:
        # 会計年度の存在確認
        fiscal_year = db.query(FiscalYear).filter(FiscalYear.id == fiscal_year_id).first()
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 標準P/Lを取得
        pl = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not pl:
            return jsonify({'error': '損益計算書が見つかりません'}), 404
        
        # P/Lデータを辞書に変換
        pl_data = {
            'sales': pl.sales,
            'cost_of_sales': pl.cost_of_sales,
            'gross_profit': pl.gross_profit,
            'operating_expenses': pl.operating_expenses,
            'operating_income': pl.operating_income,
            'non_operating_income': pl.non_operating_income,
            'non_operating_expenses': pl.non_operating_expenses,
            'ordinary_income': pl.ordinary_income,
            'extraordinary_income': pl.extraordinary_income,
            'extraordinary_loss': pl.extraordinary_loss,
            'income_before_tax': pl.income_before_tax,
            'income_tax': pl.income_tax,
            'net_income': pl.net_income
        }
        
        # 追加データ（リクエストボディから取得）
        additional_data = data.get('additional_data', {})
        
        # 組換え処理
        restructured_data = RestructuringService.restructure_pl(pl_data, additional_data)
        
        # 既存の組換えP/Lを検索
        restructured_pl = db.query(RestructuredPL).filter(
            RestructuredPL.fiscal_year_id == fiscal_year_id
        ).first()
        
        if restructured_pl:
            # 更新
            restructured_pl.sales = restructured_data['sales']
            restructured_pl.cost_of_sales = restructured_data['cost_of_sales']
            restructured_pl.gross_profit = restructured_data['gross_profit']
            restructured_pl.selling_general_admin_expenses = restructured_data['selling_general_admin_expenses']
            restructured_pl.operating_income = restructured_data['operating_income']
            restructured_pl.non_operating_income = restructured_data['non_operating_income']
            restructured_pl.non_operating_expenses = restructured_data['non_operating_expenses']
            restructured_pl.ordinary_income = restructured_data['ordinary_income']
            restructured_pl.extraordinary_income = restructured_data['extraordinary_income']
            restructured_pl.extraordinary_loss = restructured_data['extraordinary_loss']
            restructured_pl.income_before_tax = restructured_data['income_before_tax']
            restructured_pl.income_taxes = restructured_data['income_taxes']
            restructured_pl.net_income = restructured_data['net_income']
            restructured_pl.updated_at = datetime.now()
        else:
            # 新規作成
            restructured_pl = RestructuredPL(
                fiscal_year_id=fiscal_year_id,
                sales=restructured_data['sales'],
                cost_of_sales=restructured_data['cost_of_sales'],
                gross_profit=restructured_data['gross_profit'],
                selling_general_admin_expenses=restructured_data['selling_general_admin_expenses'],
                operating_income=restructured_data['operating_income'],
                non_operating_income=restructured_data['non_operating_income'],
                non_operating_expenses=restructured_data['non_operating_expenses'],
                ordinary_income=restructured_data['ordinary_income'],
                extraordinary_income=restructured_data['extraordinary_income'],
                extraordinary_loss=restructured_data['extraordinary_loss'],
                income_before_tax=restructured_data['income_before_tax'],
                income_taxes=restructured_data['income_taxes'],
                net_income=restructured_data['net_income']
            )
            db.add(restructured_pl)
        
        db.commit()
        db.refresh(restructured_pl)
        
        # 付加価値の構成要素を計算
        added_value_components = RestructuringService.calculate_added_value_components(restructured_data)
        
        return jsonify({
            'restructured_pl': {
                'id': restructured_pl.id,
                'fiscal_year_id': restructured_pl.fiscal_year_id,
                'sales': restructured_pl.sales,
                'cost_of_sales': restructured_pl.cost_of_sales,
                'gross_profit': restructured_pl.gross_profit,
                'selling_general_admin_expenses': restructured_pl.selling_general_admin_expenses,
                'operating_income': restructured_pl.operating_income,
                'non_operating_income': restructured_pl.non_operating_income,
                'non_operating_expenses': restructured_pl.non_operating_expenses,
                'ordinary_income': restructured_pl.ordinary_income,
                'extraordinary_income': restructured_pl.extraordinary_income,
                'extraordinary_loss': restructured_pl.extraordinary_loss,
                'income_before_tax': restructured_pl.income_before_tax,
                'income_taxes': restructured_pl.income_taxes,
                'net_income': restructured_pl.net_income
            },
            'added_value_components': added_value_components,
            'detailed_restructuring': restructured_data
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@restructuring_bp.route('/bs/<int:fiscal_year_id>', methods=['POST'])
def restructure_and_save_bs(fiscal_year_id):
    """
    貸借対照表を組換えて保存
    
    標準的なB/Sデータから組換えB/Sを生成し、データベースに保存する
    """
    data = request.get_json() or {}
    
    db = SessionLocal()
    try:
        # 会計年度の存在確認
        fiscal_year = db.query(FiscalYear).filter(FiscalYear.id == fiscal_year_id).first()
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 標準B/Sを取得
        bs = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not bs:
            return jsonify({'error': '貸借対照表が見つかりません'}), 404
        
        # B/Sデータを辞書に変換
        bs_data = {
            'current_assets': bs.current_assets,
            'fixed_assets': bs.fixed_assets,
            'total_assets': bs.total_assets,
            'current_liabilities': bs.current_liabilities,
            'fixed_liabilities': bs.fixed_liabilities,
            'total_liabilities': bs.total_liabilities,
            'capital': bs.capital,
            'retained_earnings': bs.retained_earnings,
            'total_equity': bs.total_equity
        }
        
        # 追加データ（リクエストボディから取得）
        additional_data = data.get('additional_data', {})
        
        # 組換え処理
        restructured_data = RestructuringService.restructure_bs(bs_data, additional_data)
        
        # 既存の組換えB/Sを検索
        restructured_bs = db.query(RestructuredBS).filter(
            RestructuredBS.fiscal_year_id == fiscal_year_id
        ).first()
        
        if restructured_bs:
            # 更新
            restructured_bs.current_assets = restructured_data['current_assets']
            restructured_bs.fixed_assets = restructured_data['fixed_assets']
            restructured_bs.total_assets = restructured_data['total_assets']
            restructured_bs.current_liabilities = restructured_data['current_liabilities']
            restructured_bs.fixed_liabilities = restructured_data['fixed_liabilities']
            restructured_bs.total_liabilities = restructured_data['total_liabilities']
            restructured_bs.net_assets = restructured_data['net_assets']
            restructured_bs.total_liabilities_and_net_assets = restructured_data['total_liabilities_and_net_assets']
            restructured_bs.updated_at = datetime.now()
        else:
            # 新規作成
            restructured_bs = RestructuredBS(
                fiscal_year_id=fiscal_year_id,
                current_assets=restructured_data['current_assets'],
                fixed_assets=restructured_data['fixed_assets'],
                total_assets=restructured_data['total_assets'],
                current_liabilities=restructured_data['current_liabilities'],
                fixed_liabilities=restructured_data['fixed_liabilities'],
                total_liabilities=restructured_data['total_liabilities'],
                net_assets=restructured_data['net_assets'],
                total_liabilities_and_net_assets=restructured_data['total_liabilities_and_net_assets']
            )
            db.add(restructured_bs)
        
        db.commit()
        db.refresh(restructured_bs)
        
        return jsonify({
            'restructured_bs': {
                'id': restructured_bs.id,
                'fiscal_year_id': restructured_bs.fiscal_year_id,
                'current_assets': restructured_bs.current_assets,
                'fixed_assets': restructured_bs.fixed_assets,
                'total_assets': restructured_bs.total_assets,
                'current_liabilities': restructured_bs.current_liabilities,
                'fixed_liabilities': restructured_bs.fixed_liabilities,
                'total_liabilities': restructured_bs.total_liabilities,
                'net_assets': restructured_bs.net_assets,
                'total_liabilities_and_net_assets': restructured_bs.total_liabilities_and_net_assets
            },
            'detailed_restructuring': restructured_data
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@restructuring_bp.route('/pl/<int:fiscal_year_id>', methods=['GET'])
def get_restructured_pl(fiscal_year_id):
    """組換えP/Lを取得"""
    db = SessionLocal()
    try:
        restructured_pl = db.query(RestructuredPL).filter(
            RestructuredPL.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not restructured_pl:
            return jsonify({'error': '組換えP/Lが見つかりません'}), 404
        
        return jsonify({
            'id': restructured_pl.id,
            'fiscal_year_id': restructured_pl.fiscal_year_id,
            'sales': restructured_pl.sales,
            'cost_of_sales': restructured_pl.cost_of_sales,
            'gross_profit': restructured_pl.gross_profit,
            'selling_general_admin_expenses': restructured_pl.selling_general_admin_expenses,
            'operating_income': restructured_pl.operating_income,
            'non_operating_income': restructured_pl.non_operating_income,
            'non_operating_expenses': restructured_pl.non_operating_expenses,
            'ordinary_income': restructured_pl.ordinary_income,
            'extraordinary_income': restructured_pl.extraordinary_income,
            'extraordinary_loss': restructured_pl.extraordinary_loss,
            'income_before_tax': restructured_pl.income_before_tax,
            'income_taxes': restructured_pl.income_taxes,
            'net_income': restructured_pl.net_income,
            'created_at': restructured_pl.created_at.isoformat(),
            'updated_at': restructured_pl.updated_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@restructuring_bp.route('/bs/<int:fiscal_year_id>', methods=['GET'])
def get_restructured_bs(fiscal_year_id):
    """組換えB/Sを取得"""
    db = SessionLocal()
    try:
        restructured_bs = db.query(RestructuredBS).filter(
            RestructuredBS.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not restructured_bs:
            return jsonify({'error': '組換えB/Sが見つかりません'}), 404
        
        return jsonify({
            'id': restructured_bs.id,
            'fiscal_year_id': restructured_bs.fiscal_year_id,
            'current_assets': restructured_bs.current_assets,
            'fixed_assets': restructured_bs.fixed_assets,
            'total_assets': restructured_bs.total_assets,
            'current_liabilities': restructured_bs.current_liabilities,
            'fixed_liabilities': restructured_bs.fixed_liabilities,
            'total_liabilities': restructured_bs.total_liabilities,
            'net_assets': restructured_bs.net_assets,
            'total_liabilities_and_net_assets': restructured_bs.total_liabilities_and_net_assets,
            'created_at': restructured_bs.created_at.isoformat(),
            'updated_at': restructured_bs.updated_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
