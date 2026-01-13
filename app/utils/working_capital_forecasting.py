"""
運転資金予測モジュール
Excel読み取りで取得した運転資金前提を使用して、将来の運転資金を予測
"""

from typing import Dict, List, Any


def forecast_working_capital_from_assumptions(
    fiscal_year_id: int,
    db
) -> Dict[str, Any]:
    """
    運転資金前提から運転資金を予測
    
    Args:
        fiscal_year_id: 会計年度ID
        db: データベースセッション
    
    Returns:
        運転資金予測結果
    """
    from ..models_decision import (
        WorkingCapitalAssumption,
        ProfitLossStatement,
        FiscalYear
    )
    
    # 運転資金前提を取得
    assumption = db.query(WorkingCapitalAssumption).filter(
        WorkingCapitalAssumption.fiscal_year_id == fiscal_year_id
    ).first()
    
    if not assumption:
        raise ValueError(f'運転資金前提が見つかりません（fiscal_year_id={fiscal_year_id}）')
    
    # 会計年度情報を取得
    fiscal_year = db.query(FiscalYear).filter(
        FiscalYear.id == fiscal_year_id
    ).first()
    
    if not fiscal_year:
        raise ValueError(f'会計年度が見つかりません（fiscal_year_id={fiscal_year_id}）')
    
    # PL情報を取得
    pl = db.query(ProfitLossStatement).filter(
        ProfitLossStatement.fiscal_year_id == fiscal_year_id
    ).first()
    
    if not pl:
        raise ValueError(f'損益計算書が見つかりません（fiscal_year_id={fiscal_year_id}）')
    
    # 売上高と売上原価
    sales = float(pl.sales_revenue or 0)
    cost_of_sales = float(pl.cost_of_sales or 0)
    
    # 月次売上高と月次原価
    monthly_sales = sales / 12
    monthly_cost = cost_of_sales / 12
    
    # 回転期間から各項目を計算
    cash_turnover_period = float(assumption.cash_turnover_period or 0)
    receivables_turnover_period = float(assumption.receivables_turnover_period or 0)
    inventory_turnover_period = float(assumption.inventory_turnover_period or 0)
    payables_turnover_period = float(assumption.payables_turnover_period or 0)
    
    # 各項目の金額を計算
    # 現預金 = 月次売上高 × 現預金回転期間
    cash = monthly_sales * cash_turnover_period
    
    # 売掛債権 = 月次売上高 × 売掛債権回転期間
    receivables = monthly_sales * receivables_turnover_period
    
    # 棚卸資産 = 月次原価 × 棚卸資産回転期間
    inventory = monthly_cost * inventory_turnover_period
    
    # 買掛債務 = 月次原価 × 買掛債務回転期間
    payables = monthly_cost * payables_turnover_period
    
    # 運転資金 = 売掛債権 + 棚卸資産 - 買掛債務
    working_capital = receivables + inventory - payables
    
    # 増減額を取得
    cash_increase = float(assumption.cash_increase or 0)
    receivables_increase = float(assumption.receivables_increase or 0)
    inventory_increase = float(assumption.inventory_increase or 0)
    payables_increase = float(assumption.payables_increase or 0)
    
    # 運転資金増減額 = 売掛債権増加額 + 棚卸資産増加額 - 買掛債務増加額
    working_capital_increase = receivables_increase + inventory_increase - payables_increase
    
    return {
        'fiscal_year_id': fiscal_year_id,
        'fiscal_year_name': fiscal_year.fiscal_year_name,
        'sales': sales,
        'cost_of_sales': cost_of_sales,
        'monthly_sales': monthly_sales,
        'monthly_cost': monthly_cost,
        'assumptions': {
            'cash_turnover_period': cash_turnover_period,
            'receivables_turnover_period': receivables_turnover_period,
            'inventory_turnover_period': inventory_turnover_period,
            'payables_turnover_period': payables_turnover_period
        },
        'forecast': {
            'cash': cash,
            'receivables': receivables,
            'inventory': inventory,
            'payables': payables,
            'working_capital': working_capital
        },
        'increases': {
            'cash_increase': cash_increase,
            'receivables_increase': receivables_increase,
            'inventory_increase': inventory_increase,
            'payables_increase': payables_increase,
            'working_capital_increase': working_capital_increase
        }
    }


def forecast_multi_year_working_capital(
    fiscal_year_ids: List[int],
    db
) -> List[Dict[str, Any]]:
    """
    複数年度の運転資金を予測
    
    Args:
        fiscal_year_ids: 会計年度IDのリスト
        db: データベースセッション
    
    Returns:
        運転資金予測結果のリスト
    """
    results = []
    
    for fiscal_year_id in fiscal_year_ids:
        try:
            result = forecast_working_capital_from_assumptions(fiscal_year_id, db)
            results.append(result)
        except Exception as e:
            print(f'運転資金予測エラー（fiscal_year_id={fiscal_year_id}）: {e}')
            results.append({
                'fiscal_year_id': fiscal_year_id,
                'error': str(e)
            })
    
    return results


def calculate_cash_flow_impact(
    fiscal_year_id: int,
    db
) -> Dict[str, Any]:
    """
    運転資金変動がキャッシュフローに与える影響を計算
    
    Args:
        fiscal_year_id: 会計年度ID
        db: データベースセッション
    
    Returns:
        キャッシュフロー影響額
    """
    from ..models_decision import WorkingCapitalAssumption
    
    # 運転資金前提を取得
    assumption = db.query(WorkingCapitalAssumption).filter(
        WorkingCapitalAssumption.fiscal_year_id == fiscal_year_id
    ).first()
    
    if not assumption:
        raise ValueError(f'運転資金前提が見つかりません（fiscal_year_id={fiscal_year_id}）')
    
    # 増減額を取得
    cash_increase = float(assumption.cash_increase or 0)
    receivables_increase = float(assumption.receivables_increase or 0)
    inventory_increase = float(assumption.inventory_increase or 0)
    payables_increase = float(assumption.payables_increase or 0)
    
    # キャッシュフローへの影響
    # 売掛債権増加 → キャッシュアウト（マイナス）
    # 棚卸資産増加 → キャッシュアウト（マイナス）
    # 買掛債務増加 → キャッシュイン（プラス）
    
    cf_impact_receivables = -receivables_increase
    cf_impact_inventory = -inventory_increase
    cf_impact_payables = payables_increase
    
    # 合計キャッシュフロー影響額
    total_cf_impact = cf_impact_receivables + cf_impact_inventory + cf_impact_payables
    
    return {
        'fiscal_year_id': fiscal_year_id,
        'cash_flow_impact': {
            'receivables_increase': receivables_increase,
            'cf_impact_receivables': cf_impact_receivables,
            'inventory_increase': inventory_increase,
            'cf_impact_inventory': cf_impact_inventory,
            'payables_increase': payables_increase,
            'cf_impact_payables': cf_impact_payables,
            'total_cf_impact': total_cf_impact
        },
        'interpretation': interpret_cf_impact(total_cf_impact)
    }


def interpret_cf_impact(cf_impact: float) -> str:
    """
    キャッシュフロー影響額を解釈
    
    Args:
        cf_impact: キャッシュフロー影響額
    
    Returns:
        解釈コメント
    """
    if cf_impact > 0:
        return f'運転資金の変動により、キャッシュフローが{abs(cf_impact):,.0f}円改善します。'
    elif cf_impact < 0:
        return f'運転資金の変動により、キャッシュフローが{abs(cf_impact):,.0f}円悪化します。資金調達が必要になる可能性があります。'
    else:
        return '運転資金の変動によるキャッシュフローへの影響はありません。'


def forecast_debt_repayment_schedule(
    fiscal_year_id: int,
    db
) -> Dict[str, Any]:
    """
    返済スケジュール前提から返済計画を予測
    
    Args:
        fiscal_year_id: 会計年度ID
        db: データベースセッション
    
    Returns:
        返済計画予測結果
    """
    from ..models_decision import DebtRepaymentAssumption, FiscalYear
    
    # 返済スケジュール前提を取得
    assumption = db.query(DebtRepaymentAssumption).filter(
        DebtRepaymentAssumption.fiscal_year_id == fiscal_year_id
    ).first()
    
    if not assumption:
        raise ValueError(f'返済スケジュール前提が見つかりません（fiscal_year_id={fiscal_year_id}）')
    
    # 会計年度情報を取得
    fiscal_year = db.query(FiscalYear).filter(
        FiscalYear.id == fiscal_year_id
    ).first()
    
    if not fiscal_year:
        raise ValueError(f'会計年度が見つかりません（fiscal_year_id={fiscal_year_id}）')
    
    # 返済スケジュールデータ
    beginning_balance = float(assumption.beginning_balance or 0)
    borrowing_amount = float(assumption.borrowing_amount or 0)
    principal_repayment = float(assumption.principal_repayment or 0)
    ending_balance = float(assumption.ending_balance or 0)
    interest_payment = float(assumption.interest_payment or 0)
    average_interest_rate = float(assumption.average_interest_rate or 0)
    
    # 月次返済額（元本）
    monthly_principal_repayment = principal_repayment / 12 if principal_repayment > 0 else 0
    
    # 月次利息
    monthly_interest_payment = interest_payment / 12 if interest_payment > 0 else 0
    
    # 月次返済額（元本＋利息）
    monthly_total_repayment = monthly_principal_repayment + monthly_interest_payment
    
    return {
        'fiscal_year_id': fiscal_year_id,
        'fiscal_year_name': fiscal_year.fiscal_year_name,
        'debt_schedule': {
            'beginning_balance': beginning_balance,
            'borrowing_amount': borrowing_amount,
            'principal_repayment': principal_repayment,
            'ending_balance': ending_balance,
            'interest_payment': interest_payment,
            'average_interest_rate': average_interest_rate
        },
        'monthly_schedule': {
            'monthly_principal_repayment': monthly_principal_repayment,
            'monthly_interest_payment': monthly_interest_payment,
            'monthly_total_repayment': monthly_total_repayment
        },
        'cash_flow_impact': {
            'borrowing_cash_in': borrowing_amount,
            'repayment_cash_out': -(principal_repayment + interest_payment),
            'net_cash_flow': borrowing_amount - (principal_repayment + interest_payment)
        }
    }


def forecast_multi_year_debt_repayment(
    fiscal_year_ids: List[int],
    db
) -> List[Dict[str, Any]]:
    """
    複数年度の返済計画を予測
    
    Args:
        fiscal_year_ids: 会計年度IDのリスト
        db: データベースセッション
    
    Returns:
        返済計画予測結果のリスト
    """
    results = []
    
    for fiscal_year_id in fiscal_year_ids:
        try:
            result = forecast_debt_repayment_schedule(fiscal_year_id, db)
            results.append(result)
        except Exception as e:
            print(f'返済計画予測エラー（fiscal_year_id={fiscal_year_id}）: {e}')
            results.append({
                'fiscal_year_id': fiscal_year_id,
                'error': str(e)
            })
    
    return results
