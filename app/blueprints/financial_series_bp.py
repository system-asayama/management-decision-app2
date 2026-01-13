"""
複数年度財務諸表シリーズ Blueprint
複数年度のPL/BS/CF（実績＋予算）を並べて予実差異を返すAPI
"""

from flask import Blueprint, request, jsonify, session
from ..utils.decorators import require_roles, ROLES
from ..db import SessionLocal
from ..models_decision import (
    Company, FiscalYear, ProfitLossStatement, BalanceSheet,
    CashFlowPlan, AnnualBudget
)
from sqlalchemy import func
from decimal import Decimal

bp = Blueprint('financial_series', __name__, url_prefix='/decision/financial-series')


def to_float(value):
    """数値をfloatに変換（NoneやDecimalに対応）"""
    if value is None:
        return 0.0
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


@bp.route('/get', methods=['GET'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def get_financial_series():
    """
    複数年度のPL/BS/CF（実績＋予算）を取得し、予実差異を返す
    
    Query Parameters:
    - company_id: int (required) - 企業ID
    - fiscal_year_ids: str (required) - カンマ区切りの会計年度ID（例: "1,2,3"）
    - include_budget: str (optional) - "true"または"false"（デフォルト: "false"）
    
    Response:
    {
        "success": true,
        "data": {
            "years": [
                {"fiscalYearId": 1, "label": "2024年度"},
                {"fiscalYearId": 2, "label": "2025年度"}
            ],
            "actual": {
                "PL": [...],
                "BS": [...],
                "CF": [...]
            },
            "budget": {  // includeBudget=trueの場合のみ
                "PL": [...],
                "BS": [...],
                "CF": [...]
            },
            "variance": {  // includeBudget=trueの場合のみ
                "PL": [...],
                "BS": [...],
                "CF": [...]
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
        fiscal_year_ids_str = request.args.get('fiscal_year_ids', '')
        include_budget = request.args.get('include_budget', 'false').lower() == 'true'
        
        # バリデーション
        if not company_id:
            return jsonify({'error': 'company_idは必須です'}), 400
        
        if not fiscal_year_ids_str:
            return jsonify({'error': 'fiscal_year_idsは必須です'}), 400
        
        try:
            fiscal_year_ids = [int(fid.strip()) for fid in fiscal_year_ids_str.split(',')]
        except ValueError:
            return jsonify({'error': 'fiscal_year_idsの形式が不正です'}), 400
        
        db = SessionLocal()
        try:
            # 企業の存在確認とテナント権限チェック
            company = db.query(Company).filter(
                Company.id == company_id,
                Company.tenant_id == tenant_id
            ).first()
            
            if not company:
                return jsonify({'error': '企業が見つかりません'}), 404
            
            # 会計年度情報を取得
            fiscal_years = db.query(FiscalYear).filter(
                FiscalYear.id.in_(fiscal_year_ids),
                FiscalYear.company_id == company_id
            ).order_by(FiscalYear.start_date).all()
            
            if not fiscal_years:
                return jsonify({'error': '会計年度が見つかりません'}), 404
            
            # years配列を構築
            years_list = [
                {
                    'fiscalYearId': fy.id,
                    'label': fy.year_name
                }
                for fy in fiscal_years
            ]
            
            # 実績データを取得
            actual_pl_list = []
            actual_bs_list = []
            actual_cf_list = []
            
            for fy in fiscal_years:
                # PL実績
                pl = db.query(ProfitLossStatement).filter(
                    ProfitLossStatement.fiscal_year_id == fy.id
                ).first()
                
                if pl:
                    actual_pl_list.append({
                        'fiscalYearId': fy.id,
                        'sales': to_float(pl.sales),
                        'costOfSales': to_float(pl.cost_of_sales),
                        'grossProfit': to_float(pl.gross_profit),
                        'operatingExpenses': to_float(pl.operating_expenses),
                        'operatingIncome': to_float(pl.operating_income),
                        'nonOperatingIncome': to_float(pl.non_operating_income),
                        'nonOperatingExpenses': to_float(pl.non_operating_expenses),
                        'ordinaryIncome': to_float(pl.ordinary_income),
                        'extraordinaryIncome': to_float(pl.extraordinary_income),
                        'extraordinaryLoss': to_float(pl.extraordinary_loss),
                        'incomeBeforeTax': to_float(pl.income_before_tax),
                        'incomeTax': to_float(pl.income_tax),
                        'netIncome': to_float(pl.net_income)
                    })
                else:
                    actual_pl_list.append({
                        'fiscalYearId': fy.id,
                        'sales': 0.0,
                        'costOfSales': 0.0,
                        'grossProfit': 0.0,
                        'operatingExpenses': 0.0,
                        'operatingIncome': 0.0,
                        'nonOperatingIncome': 0.0,
                        'nonOperatingExpenses': 0.0,
                        'ordinaryIncome': 0.0,
                        'extraordinaryIncome': 0.0,
                        'extraordinaryLoss': 0.0,
                        'incomeBeforeTax': 0.0,
                        'incomeTax': 0.0,
                        'netIncome': 0.0
                    })
                
                # BS実績
                bs = db.query(BalanceSheet).filter(
                    BalanceSheet.fiscal_year_id == fy.id
                ).first()
                
                if bs:
                    actual_bs_list.append({
                        'fiscalYearId': fy.id,
                        'currentAssets': to_float(bs.current_assets),
                        'fixedAssets': to_float(bs.fixed_assets),
                        'totalAssets': to_float(bs.total_assets),
                        'currentLiabilities': to_float(bs.current_liabilities),
                        'fixedLiabilities': to_float(bs.fixed_liabilities),
                        'totalLiabilities': to_float(bs.total_liabilities),
                        'capital': to_float(bs.capital),
                        'retainedEarnings': to_float(bs.retained_earnings),
                        'totalEquity': to_float(bs.total_equity)
                    })
                else:
                    actual_bs_list.append({
                        'fiscalYearId': fy.id,
                        'currentAssets': 0.0,
                        'fixedAssets': 0.0,
                        'totalAssets': 0.0,
                        'currentLiabilities': 0.0,
                        'fixedLiabilities': 0.0,
                        'totalLiabilities': 0.0,
                        'capital': 0.0,
                        'retainedEarnings': 0.0,
                        'totalEquity': 0.0
                    })
                
                # CF実績（月次データを年次集計）
                cf_plans = db.query(CashFlowPlan).filter(
                    CashFlowPlan.fiscal_year_id == fy.id
                ).all()
                
                if cf_plans:
                    total_receipts = sum(to_float(cf.actual_total_receipts) for cf in cf_plans)
                    total_payments = sum(to_float(cf.actual_total_payments) for cf in cf_plans)
                    # 期末残高は最終月のものを使用
                    closing_balance = to_float(cf_plans[-1].actual_closing_balance) if cf_plans else 0.0
                    
                    actual_cf_list.append({
                        'fiscalYearId': fy.id,
                        'totalReceipts': total_receipts,
                        'totalPayments': total_payments,
                        'netCashFlow': total_receipts - total_payments,
                        'closingBalance': closing_balance
                    })
                else:
                    actual_cf_list.append({
                        'fiscalYearId': fy.id,
                        'totalReceipts': 0.0,
                        'totalPayments': 0.0,
                        'netCashFlow': 0.0,
                        'closingBalance': 0.0
                    })
            
            # レスポンスデータを構築
            response_data = {
                'years': years_list,
                'actual': {
                    'PL': actual_pl_list,
                    'BS': actual_bs_list,
                    'CF': actual_cf_list
                }
            }
            
            # 予算データと差異を追加（include_budget=trueの場合）
            if include_budget:
                budget_pl_list = []
                budget_bs_list = []
                budget_cf_list = []
                variance_pl_list = []
                variance_bs_list = []
                variance_cf_list = []
                
                for i, fy in enumerate(fiscal_years):
                    # 予算データを取得
                    budget = db.query(AnnualBudget).filter(
                        AnnualBudget.fiscal_year_id == fy.id
                    ).first()
                    
                    if budget:
                        # PL予算
                        budget_pl = {
                            'fiscalYearId': fy.id,
                            'sales': to_float(budget.budget_sales),
                            'costOfSales': to_float(budget.budget_cost_of_sales),
                            'grossProfit': to_float(budget.budget_gross_profit),
                            'operatingExpenses': to_float(budget.budget_operating_expenses),
                            'operatingIncome': to_float(budget.budget_operating_income),
                            'nonOperatingIncome': to_float(budget.budget_non_operating_income),
                            'nonOperatingExpenses': to_float(budget.budget_non_operating_expenses),
                            'ordinaryIncome': to_float(budget.budget_ordinary_income),
                            'extraordinaryIncome': to_float(budget.budget_extraordinary_income),
                            'extraordinaryLoss': to_float(budget.budget_extraordinary_loss),
                            'incomeBeforeTax': to_float(budget.budget_income_before_tax),
                            'incomeTax': to_float(budget.budget_income_tax),
                            'netIncome': to_float(budget.budget_net_income)
                        }
                        budget_pl_list.append(budget_pl)
                        
                        # BS予算
                        budget_bs = {
                            'fiscalYearId': fy.id,
                            'currentAssets': to_float(budget.budget_current_assets),
                            'fixedAssets': to_float(budget.budget_fixed_assets),
                            'totalAssets': to_float(budget.budget_total_assets),
                            'currentLiabilities': to_float(budget.budget_current_liabilities),
                            'fixedLiabilities': to_float(budget.budget_fixed_liabilities),
                            'totalLiabilities': to_float(budget.budget_total_liabilities),
                            'capital': 0.0,  # AnnualBudgetにはcapitalがないため0
                            'retainedEarnings': 0.0,  # AnnualBudgetにはretainedEarningsがないため0
                            'totalEquity': to_float(budget.budget_total_equity)
                        }
                        budget_bs_list.append(budget_bs)
                        
                        # CF予算（月次計画データを年次集計）
                        cf_plans = db.query(CashFlowPlan).filter(
                            CashFlowPlan.fiscal_year_id == fy.id
                        ).all()
                        
                        if cf_plans:
                            planned_receipts = sum(to_float(cf.planned_total_receipts) for cf in cf_plans)
                            planned_payments = sum(to_float(cf.planned_total_payments) for cf in cf_plans)
                            planned_closing = to_float(cf_plans[-1].planned_closing_balance) if cf_plans else 0.0
                        else:
                            planned_receipts = 0.0
                            planned_payments = 0.0
                            planned_closing = 0.0
                        
                        budget_cf = {
                            'fiscalYearId': fy.id,
                            'totalReceipts': planned_receipts,
                            'totalPayments': planned_payments,
                            'netCashFlow': planned_receipts - planned_payments,
                            'closingBalance': planned_closing
                        }
                        budget_cf_list.append(budget_cf)
                        
                        # 差異計算（実績 - 予算）
                        actual_pl = actual_pl_list[i]
                        variance_pl = {
                            'fiscalYearId': fy.id,
                            'sales': actual_pl['sales'] - budget_pl['sales'],
                            'costOfSales': actual_pl['costOfSales'] - budget_pl['costOfSales'],
                            'grossProfit': actual_pl['grossProfit'] - budget_pl['grossProfit'],
                            'operatingExpenses': actual_pl['operatingExpenses'] - budget_pl['operatingExpenses'],
                            'operatingIncome': actual_pl['operatingIncome'] - budget_pl['operatingIncome'],
                            'nonOperatingIncome': actual_pl['nonOperatingIncome'] - budget_pl['nonOperatingIncome'],
                            'nonOperatingExpenses': actual_pl['nonOperatingExpenses'] - budget_pl['nonOperatingExpenses'],
                            'ordinaryIncome': actual_pl['ordinaryIncome'] - budget_pl['ordinaryIncome'],
                            'extraordinaryIncome': actual_pl['extraordinaryIncome'] - budget_pl['extraordinaryIncome'],
                            'extraordinaryLoss': actual_pl['extraordinaryLoss'] - budget_pl['extraordinaryLoss'],
                            'incomeBeforeTax': actual_pl['incomeBeforeTax'] - budget_pl['incomeBeforeTax'],
                            'incomeTax': actual_pl['incomeTax'] - budget_pl['incomeTax'],
                            'netIncome': actual_pl['netIncome'] - budget_pl['netIncome']
                        }
                        variance_pl_list.append(variance_pl)
                        
                        actual_bs = actual_bs_list[i]
                        variance_bs = {
                            'fiscalYearId': fy.id,
                            'currentAssets': actual_bs['currentAssets'] - budget_bs['currentAssets'],
                            'fixedAssets': actual_bs['fixedAssets'] - budget_bs['fixedAssets'],
                            'totalAssets': actual_bs['totalAssets'] - budget_bs['totalAssets'],
                            'currentLiabilities': actual_bs['currentLiabilities'] - budget_bs['currentLiabilities'],
                            'fixedLiabilities': actual_bs['fixedLiabilities'] - budget_bs['fixedLiabilities'],
                            'totalLiabilities': actual_bs['totalLiabilities'] - budget_bs['totalLiabilities'],
                            'capital': actual_bs['capital'] - budget_bs['capital'],
                            'retainedEarnings': actual_bs['retainedEarnings'] - budget_bs['retainedEarnings'],
                            'totalEquity': actual_bs['totalEquity'] - budget_bs['totalEquity']
                        }
                        variance_bs_list.append(variance_bs)
                        
                        actual_cf = actual_cf_list[i]
                        variance_cf = {
                            'fiscalYearId': fy.id,
                            'totalReceipts': actual_cf['totalReceipts'] - budget_cf['totalReceipts'],
                            'totalPayments': actual_cf['totalPayments'] - budget_cf['totalPayments'],
                            'netCashFlow': actual_cf['netCashFlow'] - budget_cf['netCashFlow'],
                            'closingBalance': actual_cf['closingBalance'] - budget_cf['closingBalance']
                        }
                        variance_cf_list.append(variance_cf)
                        
                    else:
                        # 予算データがない場合は0で埋める
                        budget_pl_list.append({
                            'fiscalYearId': fy.id,
                            'sales': 0.0,
                            'costOfSales': 0.0,
                            'grossProfit': 0.0,
                            'operatingExpenses': 0.0,
                            'operatingIncome': 0.0,
                            'nonOperatingIncome': 0.0,
                            'nonOperatingExpenses': 0.0,
                            'ordinaryIncome': 0.0,
                            'extraordinaryIncome': 0.0,
                            'extraordinaryLoss': 0.0,
                            'incomeBeforeTax': 0.0,
                            'incomeTax': 0.0,
                            'netIncome': 0.0
                        })
                        budget_bs_list.append({
                            'fiscalYearId': fy.id,
                            'currentAssets': 0.0,
                            'fixedAssets': 0.0,
                            'totalAssets': 0.0,
                            'currentLiabilities': 0.0,
                            'fixedLiabilities': 0.0,
                            'totalLiabilities': 0.0,
                            'capital': 0.0,
                            'retainedEarnings': 0.0,
                            'totalEquity': 0.0
                        })
                        budget_cf_list.append({
                            'fiscalYearId': fy.id,
                            'totalReceipts': 0.0,
                            'totalPayments': 0.0,
                            'netCashFlow': 0.0,
                            'closingBalance': 0.0
                        })
                        
                        # 実績のみの差異
                        variance_pl_list.append(actual_pl_list[i])
                        variance_bs_list.append(actual_bs_list[i])
                        variance_cf_list.append(actual_cf_list[i])
                
                response_data['budget'] = {
                    'PL': budget_pl_list,
                    'BS': budget_bs_list,
                    'CF': budget_cf_list
                }
                response_data['variance'] = {
                    'PL': variance_pl_list,
                    'BS': variance_bs_list,
                    'CF': variance_cf_list
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
