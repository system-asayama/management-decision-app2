"""
評価API Blueprint
前年比較により評価記号（◎◯△×）を返すAPI
"""

from flask import Blueprint, request, jsonify, session
from ..utils.decorators import require_roles, ROLES
from ..db import SessionLocal
from ..models_decision import (
    Company, FiscalYear, ProfitLossStatement, BalanceSheet
)
from ..utils.evaluation_helpers import evaluate_yoy, evaluate_multiple_indicators

bp = Blueprint('evaluation', __name__, url_prefix='/decision/evaluation')


@bp.route('/get', methods=['GET'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def get_evaluation():
    """
    前年比較により評価記号を返す
    
    Query Parameters:
    - company_id: int (required) - 企業ID
    - fiscal_year_id: int (required) - 当年の会計年度ID
    
    Response:
    {
        "success": true,
        "data": {
            "fiscalYear": {
                "id": 1,
                "label": "2024年度"
            },
            "prevFiscalYear": {
                "id": 0,
                "label": "2023年度"
            },
            "pl": {
                "sales": {
                    "thisYear": 1000000000,
                    "prevYear": 900000000,
                    "ratio": 11.11,
                    "grade": "◎"
                },
                ...
            },
            "bs": {
                "totalAssets": {
                    "thisYear": 1300000000,
                    "prevYear": 1200000000,
                    "ratio": 8.33,
                    "grade": "◯"
                },
                ...
            }
        }
    }
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    try:
        # パラメータ取得
        company_id = request.args.get('company_id', type=int)
        fiscal_year_id = request.args.get('fiscal_year_id', type=int)
        
        # バリデーション
        if not company_id:
            return jsonify({'error': 'company_idは必須です'}), 400
        
        if not fiscal_year_id:
            return jsonify({'error': 'fiscal_year_idは必須です'}), 400
        
        db = SessionLocal()
        try:
            # 企業の存在確認とテナント権限チェック
            company = db.query(Company).filter(
                Company.id == company_id,
                Company.tenant_id == tenant_id
            ).first()
            
            if not company:
                return jsonify({'error': '企業が見つかりません'}), 404
            
            # 当年の会計年度を取得
            fiscal_year = db.query(FiscalYear).filter(
                FiscalYear.id == fiscal_year_id,
                FiscalYear.company_id == company_id
            ).first()
            
            if not fiscal_year:
                return jsonify({'error': '会計年度が見つかりません'}), 404
            
            # 前年の会計年度を取得（開始日が当年より前で、最も近いもの）
            prev_fiscal_year = db.query(FiscalYear).filter(
                FiscalYear.company_id == company_id,
                FiscalYear.start_date < fiscal_year.start_date
            ).order_by(FiscalYear.start_date.desc()).first()
            
            if not prev_fiscal_year:
                return jsonify({'error': '前年の会計年度が見つかりません'}), 404
            
            # 当年のPL/BSを取得
            pl_this_year = db.query(ProfitLossStatement).filter(
                ProfitLossStatement.fiscal_year_id == fiscal_year_id
            ).first()
            
            bs_this_year = db.query(BalanceSheet).filter(
                BalanceSheet.fiscal_year_id == fiscal_year_id
            ).first()
            
            # 前年のPL/BSを取得
            pl_prev_year = db.query(ProfitLossStatement).filter(
                ProfitLossStatement.fiscal_year_id == prev_fiscal_year.id
            ).first()
            
            bs_prev_year = db.query(BalanceSheet).filter(
                BalanceSheet.fiscal_year_id == prev_fiscal_year.id
            ).first()
            
            # PLの指標を評価
            pl_indicators_this_year = {}
            pl_indicators_prev_year = {}
            
            if pl_this_year:
                pl_indicators_this_year = {
                    'sales': pl_this_year.sales,
                    'costOfSales': pl_this_year.cost_of_sales,
                    'grossProfit': pl_this_year.gross_profit,
                    'operatingExpenses': pl_this_year.operating_expenses,
                    'operatingIncome': pl_this_year.operating_income,
                    'nonOperatingIncome': pl_this_year.non_operating_income,
                    'nonOperatingExpenses': pl_this_year.non_operating_expenses,
                    'ordinaryIncome': pl_this_year.ordinary_income,
                    'extraordinaryIncome': pl_this_year.extraordinary_income,
                    'extraordinaryLoss': pl_this_year.extraordinary_loss,
                    'incomeBeforeTax': pl_this_year.income_before_tax,
                    'incomeTax': pl_this_year.income_tax,
                    'netIncome': pl_this_year.net_income
                }
            
            if pl_prev_year:
                pl_indicators_prev_year = {
                    'sales': pl_prev_year.sales,
                    'costOfSales': pl_prev_year.cost_of_sales,
                    'grossProfit': pl_prev_year.gross_profit,
                    'operatingExpenses': pl_prev_year.operating_expenses,
                    'operatingIncome': pl_prev_year.operating_income,
                    'nonOperatingIncome': pl_prev_year.non_operating_income,
                    'nonOperatingExpenses': pl_prev_year.non_operating_expenses,
                    'ordinaryIncome': pl_prev_year.ordinary_income,
                    'extraordinaryIncome': pl_prev_year.extraordinary_income,
                    'extraordinaryLoss': pl_prev_year.extraordinary_loss,
                    'incomeBeforeTax': pl_prev_year.income_before_tax,
                    'incomeTax': pl_prev_year.income_tax,
                    'netIncome': pl_prev_year.net_income
                }
            
            pl_evaluation = evaluate_multiple_indicators(
                pl_indicators_this_year,
                pl_indicators_prev_year
            )
            
            # BSの指標を評価
            bs_indicators_this_year = {}
            bs_indicators_prev_year = {}
            
            if bs_this_year:
                bs_indicators_this_year = {
                    'currentAssets': bs_this_year.current_assets,
                    'fixedAssets': bs_this_year.fixed_assets,
                    'totalAssets': bs_this_year.total_assets,
                    'currentLiabilities': bs_this_year.current_liabilities,
                    'fixedLiabilities': bs_this_year.fixed_liabilities,
                    'totalLiabilities': bs_this_year.total_liabilities,
                    'capital': bs_this_year.capital,
                    'retainedEarnings': bs_this_year.retained_earnings,
                    'totalEquity': bs_this_year.total_equity
                }
            
            if bs_prev_year:
                bs_indicators_prev_year = {
                    'currentAssets': bs_prev_year.current_assets,
                    'fixedAssets': bs_prev_year.fixed_assets,
                    'totalAssets': bs_prev_year.total_assets,
                    'currentLiabilities': bs_prev_year.current_liabilities,
                    'fixedLiabilities': bs_prev_year.fixed_liabilities,
                    'totalLiabilities': bs_prev_year.total_liabilities,
                    'capital': bs_prev_year.capital,
                    'retainedEarnings': bs_prev_year.retained_earnings,
                    'totalEquity': bs_prev_year.total_equity
                }
            
            bs_evaluation = evaluate_multiple_indicators(
                bs_indicators_this_year,
                bs_indicators_prev_year
            )
            
            # レスポンスを構築
            response_data = {
                'fiscalYear': {
                    'id': fiscal_year.id,
                    'label': fiscal_year.year_name
                },
                'prevFiscalYear': {
                    'id': prev_fiscal_year.id,
                    'label': prev_fiscal_year.year_name
                },
                'pl': pl_evaluation,
                'bs': bs_evaluation
            }
            
            return jsonify({
                'success': True,
                'data': response_data
            }), 200
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'データベースエラー: {str(e)}'}), 500
        finally:
            db.close()
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'リクエスト処理エラー: {str(e)}'}), 500
