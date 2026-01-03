"""
経営分析API Blueprint
4つの視点（成長力、収益力、資金力、生産力）から経営指標を計算する
"""
from flask import Blueprint, request, jsonify
from app.database import get_db_session
from app.models import (
    FiscalYear, ProfitLossStatement, BalanceSheet,
    RestructuredPL, RestructuredBS, FinancialIndicator
)
from app.services.analysis_service import AnalysisService
from app.services.restructuring_service import RestructuringService
from datetime import datetime

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')


def get_financial_data(fiscal_year_id: int, db):
    """
    会計年度の財務データを取得
    
    Args:
        fiscal_year_id: 会計年度ID
        db: データベースセッション
    
    Returns:
        財務データの辞書
    """
    # P/Lデータ
    pl = db.query(ProfitLossStatement).filter(
        ProfitLossStatement.fiscal_year_id == fiscal_year_id
    ).first()
    
    # B/Sデータ
    bs = db.query(BalanceSheet).filter(
        BalanceSheet.fiscal_year_id == fiscal_year_id
    ).first()
    
    # 組換えP/Lデータ
    restructured_pl = db.query(RestructuredPL).filter(
        RestructuredPL.fiscal_year_id == fiscal_year_id
    ).first()
    
    # 組換えB/Sデータ
    restructured_bs = db.query(RestructuredBS).filter(
        RestructuredBS.fiscal_year_id == fiscal_year_id
    ).first()
    
    if not pl or not bs:
        return None
    
    # 基本データ
    data = {
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
        'net_income': pl.net_income,
        'current_assets': bs.current_assets,
        'fixed_assets': bs.fixed_assets,
        'total_assets': bs.total_assets,
        'current_liabilities': bs.current_liabilities,
        'fixed_liabilities': bs.fixed_liabilities,
        'total_liabilities': bs.total_liabilities,
        'capital': bs.capital,
        'retained_earnings': bs.retained_earnings,
        'net_assets': bs.total_equity
    }
    
    # 組換えデータがあれば追加
    if restructured_pl:
        # 組換えP/Lから付加価値などを計算
        pl_dict = {
            'sales': restructured_pl.sales,
            'cost_of_sales': restructured_pl.cost_of_sales,
            'gross_profit': restructured_pl.gross_profit,
            'operating_expenses': restructured_pl.selling_general_admin_expenses,
            'operating_income': restructured_pl.operating_income,
            'non_operating_income': restructured_pl.non_operating_income,
            'non_operating_expenses': restructured_pl.non_operating_expenses,
            'ordinary_income': restructured_pl.ordinary_income,
            'income_before_tax': restructured_pl.income_before_tax,
            'income_tax': restructured_pl.income_taxes,
            'net_income': restructured_pl.net_income
        }
        
        # 付加価値計算（簡易版）
        restructured_data = RestructuringService.restructure_pl(pl_dict, {})
        data['gross_added_value'] = restructured_data.get('gross_added_value', 0)
        data['total_labor_cost'] = restructured_data.get('total_labor_cost', 0)
        data['executive_compensation'] = restructured_data.get('executive_compensation', 0)
        data['capital_regeneration_cost'] = restructured_data.get('capital_regeneration_cost', 0)
        data['research_development_expenses'] = restructured_data.get('research_development_expenses', 0)
        data['variable_expenses'] = restructured_data.get('variable_expenses', 0)
        data['general_expenses'] = restructured_data.get('fixed_expenses', 0)
    
    if restructured_bs:
        data['cash_on_hand'] = restructured_bs.current_assets * 0.2  # 簡易計算
        data['trade_receivables'] = restructured_bs.current_assets * 0.4  # 簡易計算
        data['inventory_assets'] = restructured_bs.current_assets * 0.3  # 簡易計算
        data['tangible_fixed_assets'] = restructured_bs.fixed_assets * 0.8  # 簡易計算
        data['trade_payables'] = restructured_bs.current_liabilities * 0.5  # 簡易計算
        data['total_short_term_debt'] = restructured_bs.current_liabilities * 0.3  # 簡易計算
        data['long_term_debt_excluding_executive'] = restructured_bs.fixed_liabilities * 0.8  # 簡易計算
    
    return data


@analysis_bp.route('/growth/<int:fiscal_year_id>', methods=['GET'])
def calculate_growth_indicators(fiscal_year_id):
    """成長力の指標を計算"""
    db = get_db_session()
    try:
        # 当年度の会計年度を取得
        fiscal_year = db.query(FiscalYear).filter(FiscalYear.id == fiscal_year_id).first()
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 前年度の会計年度を取得
        previous_fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.company_id == fiscal_year.company_id,
            FiscalYear.year == fiscal_year.year - 1
        ).first()
        
        if not previous_fiscal_year:
            return jsonify({'error': '前年度のデータが見つかりません'}), 404
        
        # 当年度のデータ
        current_data = get_financial_data(fiscal_year_id, db)
        if not current_data:
            return jsonify({'error': '当年度の財務データが見つかりません'}), 404
        
        # 前年度のデータ
        previous_data = get_financial_data(previous_fiscal_year.id, db)
        if not previous_data:
            return jsonify({'error': '前年度の財務データが見つかりません'}), 404
        
        # 成長力指標を計算
        indicators = AnalysisService.calculate_growth_indicators(current_data, previous_data)
        
        return jsonify({
            'fiscal_year_id': fiscal_year_id,
            'indicators': indicators
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@analysis_bp.route('/profitability/<int:fiscal_year_id>', methods=['GET'])
def calculate_profitability_indicators(fiscal_year_id):
    """収益力の指標を計算"""
    db = get_db_session()
    try:
        # 財務データを取得
        data = get_financial_data(fiscal_year_id, db)
        if not data:
            return jsonify({'error': '財務データが見つかりません'}), 404
        
        # 収益力指標を計算
        indicators = AnalysisService.calculate_profitability_indicators(data)
        
        return jsonify({
            'fiscal_year_id': fiscal_year_id,
            'indicators': indicators
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@analysis_bp.route('/financial-strength/<int:fiscal_year_id>', methods=['GET'])
def calculate_financial_strength_indicators(fiscal_year_id):
    """資金力の指標を計算"""
    db = get_db_session()
    try:
        # 財務データを取得
        data = get_financial_data(fiscal_year_id, db)
        if not data:
            return jsonify({'error': '財務データが見つかりません'}), 404
        
        # 資金力指標を計算
        indicators = AnalysisService.calculate_financial_strength_indicators(data)
        
        return jsonify({
            'fiscal_year_id': fiscal_year_id,
            'indicators': indicators
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@analysis_bp.route('/productivity/<int:fiscal_year_id>', methods=['GET'])
def calculate_productivity_indicators(fiscal_year_id):
    """生産力の指標を計算"""
    data_from_request = request.get_json() or {}
    employee_count = data_from_request.get('employee_count', 1)
    
    db = get_db_session()
    try:
        # 財務データを取得
        data = get_financial_data(fiscal_year_id, db)
        if not data:
            return jsonify({'error': '財務データが見つかりません'}), 404
        
        # 従業員数を追加
        data['employee_count'] = employee_count
        
        # 生産力指標を計算
        indicators = AnalysisService.calculate_productivity_indicators(data)
        
        return jsonify({
            'fiscal_year_id': fiscal_year_id,
            'employee_count': employee_count,
            'indicators': indicators
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@analysis_bp.route('/all/<int:fiscal_year_id>', methods=['GET'])
def calculate_all_indicators(fiscal_year_id):
    """すべての経営指標を計算"""
    data_from_request = request.args
    employee_count = int(data_from_request.get('employee_count', 1))
    
    db = get_db_session()
    try:
        # 当年度の会計年度を取得
        fiscal_year = db.query(FiscalYear).filter(FiscalYear.id == fiscal_year_id).first()
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 当年度のデータ
        current_data = get_financial_data(fiscal_year_id, db)
        if not current_data:
            return jsonify({'error': '財務データが見つかりません'}), 404
        
        current_data['employee_count'] = employee_count
        
        # 前年度のデータ（成長力計算用）
        previous_fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.company_id == fiscal_year.company_id,
            FiscalYear.year == fiscal_year.year - 1
        ).first()
        
        previous_data = None
        if previous_fiscal_year:
            previous_data = get_financial_data(previous_fiscal_year.id, db)
            if previous_data:
                previous_data['employee_count'] = employee_count
        
        # すべての指標を計算
        indicators = AnalysisService.calculate_all_indicators(current_data, previous_data)
        
        return jsonify({
            'fiscal_year_id': fiscal_year_id,
            'employee_count': employee_count,
            'indicators': indicators
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@analysis_bp.route('/save/<int:fiscal_year_id>', methods=['POST'])
def save_indicators(fiscal_year_id):
    """計算した経営指標をデータベースに保存"""
    data = request.get_json()
    
    if 'indicators' not in data:
        return jsonify({'error': 'indicatorsは必須です'}), 400
    
    db = get_db_session()
    try:
        # 会計年度の存在確認
        fiscal_year = db.query(FiscalYear).filter(FiscalYear.id == fiscal_year_id).first()
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        indicators_data = data['indicators']
        saved_indicators = []
        
        # 各指標を保存
        for category, indicators in indicators_data.items():
            for indicator_name, indicator_value in indicators.items():
                # 既存の指標を検索
                existing_indicator = db.query(FinancialIndicator).filter(
                    FinancialIndicator.fiscal_year_id == fiscal_year_id,
                    FinancialIndicator.indicator_name == indicator_name
                ).first()
                
                if existing_indicator:
                    # 更新
                    existing_indicator.indicator_value = indicator_value
                    existing_indicator.category = category
                    existing_indicator.updated_at = datetime.now()
                else:
                    # 新規作成
                    new_indicator = FinancialIndicator(
                        fiscal_year_id=fiscal_year_id,
                        indicator_name=indicator_name,
                        indicator_value=indicator_value,
                        category=category
                    )
                    db.add(new_indicator)
                    saved_indicators.append(indicator_name)
        
        db.commit()
        
        return jsonify({
            'message': '経営指標を保存しました',
            'saved_count': len(saved_indicators)
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
