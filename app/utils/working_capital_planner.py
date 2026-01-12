"""
主要運転資金計画モジュール

運転資金の計画と管理を行います。
"""

from typing import Dict, List, Any


def calculate_working_capital(
    accounts_receivable: float,
    inventory: float,
    accounts_payable: float
) -> Dict[str, float]:
    """
    運転資金を計算
    
    Args:
        accounts_receivable: 売掛金
        inventory: 棚卸資産
        accounts_payable: 買掛金
    
    Returns:
        運転資金の計算結果
    """
    # 運転資金 = 売掛金 + 棚卸資産 - 買掛金
    working_capital = accounts_receivable + inventory - accounts_payable
    
    return {
        'accounts_receivable': accounts_receivable,
        'inventory': inventory,
        'accounts_payable': accounts_payable,
        'working_capital': working_capital
    }


def calculate_working_capital_turnover(
    sales: float,
    working_capital: float
) -> float:
    """
    運転資金回転率を計算
    
    Args:
        sales: 売上高
        working_capital: 運転資金
    
    Returns:
        運転資金回転率（回）
    """
    if working_capital == 0:
        return 0.0
    
    return sales / working_capital


def calculate_working_capital_period(
    working_capital: float,
    daily_sales: float
) -> float:
    """
    運転資金回転期間を計算
    
    Args:
        working_capital: 運転資金
        daily_sales: 日商（1日当たり売上高）
    
    Returns:
        運転資金回転期間（日）
    """
    if daily_sales == 0:
        return 0.0
    
    return working_capital / daily_sales


def calculate_accounts_receivable_turnover(
    sales: float,
    accounts_receivable: float
) -> float:
    """
    売掛金回転率を計算
    
    Args:
        sales: 売上高
        accounts_receivable: 売掛金
    
    Returns:
        売掛金回転率（回）
    """
    if accounts_receivable == 0:
        return 0.0
    
    return sales / accounts_receivable


def calculate_inventory_turnover(
    cost_of_sales: float,
    inventory: float
) -> float:
    """
    棚卸資産回転率を計算
    
    Args:
        cost_of_sales: 売上原価
        inventory: 棚卸資産
    
    Returns:
        棚卸資産回転率（回）
    """
    if inventory == 0:
        return 0.0
    
    return cost_of_sales / inventory


def calculate_accounts_payable_turnover(
    cost_of_sales: float,
    accounts_payable: float
) -> float:
    """
    買掛金回転率を計算
    
    Args:
        cost_of_sales: 売上原価
        accounts_payable: 買掛金
    
    Returns:
        買掛金回転率（回）
    """
    if accounts_payable == 0:
        return 0.0
    
    return cost_of_sales / accounts_payable


def plan_working_capital(
    sales: float,
    cost_of_sales: float,
    accounts_receivable_days: int,
    inventory_days: int,
    accounts_payable_days: int
) -> Dict[str, Any]:
    """
    運転資金計画を作成
    
    Args:
        sales: 年間売上高
        cost_of_sales: 年間売上原価
        accounts_receivable_days: 売掛金回収日数
        inventory_days: 棚卸資産保有日数
        accounts_payable_days: 買掛金支払日数
    
    Returns:
        運転資金計画の辞書
    """
    # 日商と日原価を計算
    daily_sales = sales / 365
    daily_cost = cost_of_sales / 365
    
    # 各項目を計算
    accounts_receivable = daily_sales * accounts_receivable_days
    inventory = daily_cost * inventory_days
    accounts_payable = daily_cost * accounts_payable_days
    
    # 運転資金を計算
    working_capital = accounts_receivable + inventory - accounts_payable
    
    # 回転率を計算
    ar_turnover = 365 / accounts_receivable_days if accounts_receivable_days > 0 else 0
    inventory_turnover = 365 / inventory_days if inventory_days > 0 else 0
    ap_turnover = 365 / accounts_payable_days if accounts_payable_days > 0 else 0
    
    # 運転資金回転期間
    wc_period = accounts_receivable_days + inventory_days - accounts_payable_days
    
    # 運転資金回転率
    wc_turnover = 365 / wc_period if wc_period > 0 else 0
    
    return {
        'sales': sales,
        'cost_of_sales': cost_of_sales,
        'daily_sales': daily_sales,
        'daily_cost': daily_cost,
        'accounts_receivable': accounts_receivable,
        'accounts_receivable_days': accounts_receivable_days,
        'accounts_receivable_turnover': ar_turnover,
        'inventory': inventory,
        'inventory_days': inventory_days,
        'inventory_turnover': inventory_turnover,
        'accounts_payable': accounts_payable,
        'accounts_payable_days': accounts_payable_days,
        'accounts_payable_turnover': ap_turnover,
        'working_capital': working_capital,
        'working_capital_period': wc_period,
        'working_capital_turnover': wc_turnover,
        'evaluation': evaluate_working_capital(wc_period, ar_turnover, inventory_turnover)
    }


def calculate_cash_conversion_cycle(
    accounts_receivable_days: int,
    inventory_days: int,
    accounts_payable_days: int
) -> int:
    """
    キャッシュ・コンバージョン・サイクル（CCC）を計算
    
    Args:
        accounts_receivable_days: 売掛金回収日数
        inventory_days: 棚卸資産保有日数
        accounts_payable_days: 買掛金支払日数
    
    Returns:
        CCC（日）
    """
    return accounts_receivable_days + inventory_days - accounts_payable_days


def simulate_working_capital_scenarios(
    base_sales: float,
    base_cost_of_sales: float,
    scenarios: List[Dict[str, int]]
) -> List[Dict[str, Any]]:
    """
    複数の運転資金シナリオをシミュレーション
    
    Args:
        base_sales: 基準売上高
        base_cost_of_sales: 基準売上原価
        scenarios: シナリオのリスト
    
    Returns:
        シミュレーション結果のリスト
    """
    results = []
    
    for scenario in scenarios:
        result = plan_working_capital(
            sales=base_sales,
            cost_of_sales=base_cost_of_sales,
            accounts_receivable_days=scenario.get('accounts_receivable_days', 30),
            inventory_days=scenario.get('inventory_days', 30),
            accounts_payable_days=scenario.get('accounts_payable_days', 30)
        )
        result['scenario_name'] = scenario.get('name', 'シナリオ')
        results.append(result)
    
    return results


def evaluate_working_capital(
    working_capital_period: float,
    ar_turnover: float,
    inventory_turnover: float
) -> str:
    """
    運転資金の効率性を評価
    
    Args:
        working_capital_period: 運転資金回転期間
        ar_turnover: 売掛金回転率
        inventory_turnover: 棚卸資産回転率
    
    Returns:
        評価コメント
    """
    comments = []
    
    # 運転資金回転期間の評価
    if working_capital_period < 30:
        comments.append("運転資金回転期間が短く、資金効率が非常に良好です。")
    elif working_capital_period < 60:
        comments.append("運転資金回転期間は適正範囲内です。")
    elif working_capital_period < 90:
        comments.append("運転資金回転期間がやや長く、改善の余地があります。")
    else:
        comments.append("運転資金回転期間が長く、資金効率の改善が必要です。")
    
    # 売掛金回転率の評価
    if ar_turnover > 12:
        comments.append("売掛金の回収が早く、良好です。")
    elif ar_turnover > 6:
        comments.append("売掛金の回収は適正範囲内です。")
    else:
        comments.append("売掛金の回収が遅く、改善が必要です。")
    
    # 棚卸資産回転率の評価
    if inventory_turnover > 12:
        comments.append("在庫回転が早く、効率的です。")
    elif inventory_turnover > 6:
        comments.append("在庫回転は適正範囲内です。")
    else:
        comments.append("在庫回転が遅く、在庫管理の改善が必要です。")
    
    return " ".join(comments)


def calculate_required_working_capital_increase(
    current_sales: float,
    planned_sales: float,
    current_working_capital: float
) -> Dict[str, float]:
    """
    売上増加に伴う運転資金増加額を計算
    
    Args:
        current_sales: 現在の売上高
        planned_sales: 計画売上高
        current_working_capital: 現在の運転資金
    
    Returns:
        運転資金増加額の計算結果
    """
    # 売上高増加率
    sales_growth_rate = ((planned_sales - current_sales) / current_sales) if current_sales > 0 else 0
    
    # 必要運転資金増加額
    required_wc_increase = current_working_capital * sales_growth_rate
    
    # 計画時の運転資金
    planned_working_capital = current_working_capital + required_wc_increase
    
    return {
        'current_sales': current_sales,
        'planned_sales': planned_sales,
        'sales_growth_rate': sales_growth_rate * 100,
        'current_working_capital': current_working_capital,
        'required_wc_increase': required_wc_increase,
        'planned_working_capital': planned_working_capital
    }


def analyze_working_capital_efficiency(
    sales: float,
    cost_of_sales: float,
    accounts_receivable: float,
    inventory: float,
    accounts_payable: float
) -> Dict[str, Any]:
    """
    運転資金の効率性を総合分析
    
    Args:
        sales: 売上高
        cost_of_sales: 売上原価
        accounts_receivable: 売掛金
        inventory: 棚卸資産
        accounts_payable: 買掛金
    
    Returns:
        効率性分析結果の辞書
    """
    # 運転資金を計算
    working_capital = accounts_receivable + inventory - accounts_payable
    
    # 各回転率を計算
    ar_turnover = calculate_accounts_receivable_turnover(sales, accounts_receivable)
    inventory_turnover = calculate_inventory_turnover(cost_of_sales, inventory)
    ap_turnover = calculate_accounts_payable_turnover(cost_of_sales, accounts_payable)
    wc_turnover = calculate_working_capital_turnover(sales, working_capital)
    
    # 各回転期間を計算
    ar_days = 365 / ar_turnover if ar_turnover > 0 else 0
    inventory_days = 365 / inventory_turnover if inventory_turnover > 0 else 0
    ap_days = 365 / ap_turnover if ap_turnover > 0 else 0
    wc_days = 365 / wc_turnover if wc_turnover > 0 else 0
    
    # CCC
    ccc = calculate_cash_conversion_cycle(int(ar_days), int(inventory_days), int(ap_days))
    
    return {
        'working_capital': working_capital,
        'accounts_receivable_turnover': ar_turnover,
        'accounts_receivable_days': ar_days,
        'inventory_turnover': inventory_turnover,
        'inventory_days': inventory_days,
        'accounts_payable_turnover': ap_turnover,
        'accounts_payable_days': ap_days,
        'working_capital_turnover': wc_turnover,
        'working_capital_days': wc_days,
        'cash_conversion_cycle': ccc,
        'evaluation': evaluate_working_capital(ccc, ar_turnover, inventory_turnover)
    }
