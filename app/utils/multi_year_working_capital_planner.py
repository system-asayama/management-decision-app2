"""
多年度運転資金計画モジュール

3年間の運転資金計画を統合的に管理します。
"""

from typing import Dict, List, Any


def calculate_working_capital_from_turnover(
    sales: float,
    accounts_receivable_days: float,
    inventory_days: float,
    accounts_payable_days: float,
    cost_of_sales: float = None
) -> Dict[str, Any]:
    """
    回転期間から運転資金を計算
    
    Args:
        sales: 売上高
        accounts_receivable_days: 売掛金回転期間（日）
        inventory_days: 棚卸資産回転期間（日）
        accounts_payable_days: 買掛金回転期間（日）
        cost_of_sales: 売上原価（Noneの場合は売上高の70%と仮定）
    
    Returns:
        dict: 運転資金の内訳
    """
    if cost_of_sales is None:
        cost_of_sales = sales * 0.7
    
    # 1日あたりの売上高と原価
    daily_sales = sales / 365
    daily_cost = cost_of_sales / 365
    
    # 各項目を計算
    accounts_receivable = daily_sales * accounts_receivable_days
    inventory = daily_cost * inventory_days
    accounts_payable = daily_cost * accounts_payable_days
    
    # 正味運転資金
    net_working_capital = accounts_receivable + inventory - accounts_payable
    
    # キャッシュコンバージョンサイクル
    cash_conversion_cycle = accounts_receivable_days + inventory_days - accounts_payable_days
    
    return {
        'accounts_receivable': accounts_receivable,
        'inventory': inventory,
        'accounts_payable': accounts_payable,
        'net_working_capital': net_working_capital,
        'cash_conversion_cycle': cash_conversion_cycle
    }


def create_multi_year_working_capital_plan(
    base_year: int,
    yearly_plans: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    多年度運転資金計画を作成
    
    Args:
        base_year: 基準年度
        yearly_plans: 各年度の計画データのリスト
            各年度のデータには以下のキーを含む:
            - sales: 売上高
            - cost_of_sales: 売上原価
            - accounts_receivable_days: 売掛金回転期間（日）
            - inventory_days: 棚卸資産回転期間（日）
            - accounts_payable_days: 買掛金回転期間（日）
    
    Returns:
        dict: 多年度運転資金計画
    """
    multi_year_plan = {
        'base_year': base_year,
        'years': []
    }
    
    prev_net_working_capital = 0
    
    for year_offset, yearly_plan in enumerate(yearly_plans):
        year = base_year + year_offset
        
        # 運転資金を計算
        working_capital = calculate_working_capital_from_turnover(
            sales=yearly_plan.get('sales', 0),
            accounts_receivable_days=yearly_plan.get('accounts_receivable_days', 30),
            inventory_days=yearly_plan.get('inventory_days', 30),
            accounts_payable_days=yearly_plan.get('accounts_payable_days', 30),
            cost_of_sales=yearly_plan.get('cost_of_sales')
        )
        
        # 運転資金の増減
        working_capital_change = working_capital['net_working_capital'] - prev_net_working_capital
        
        year_plan_data = {
            'year': year,
            'year_offset': year_offset,
            'sales': yearly_plan.get('sales', 0),
            'cost_of_sales': yearly_plan.get('cost_of_sales', yearly_plan.get('sales', 0) * 0.7),
            'accounts_receivable_days': yearly_plan.get('accounts_receivable_days', 30),
            'inventory_days': yearly_plan.get('inventory_days', 30),
            'accounts_payable_days': yearly_plan.get('accounts_payable_days', 30),
            'accounts_receivable': working_capital['accounts_receivable'],
            'inventory': working_capital['inventory'],
            'accounts_payable': working_capital['accounts_payable'],
            'net_working_capital': working_capital['net_working_capital'],
            'working_capital_change': working_capital_change,
            'cash_conversion_cycle': working_capital['cash_conversion_cycle']
        }
        
        multi_year_plan['years'].append(year_plan_data)
        
        # 次年度の基準として今年度の正味運転資金を使用
        prev_net_working_capital = working_capital['net_working_capital']
    
    return multi_year_plan


def calculate_multi_year_working_capital_summary(multi_year_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    多年度運転資金計画のサマリーを計算
    
    Args:
        multi_year_plan: 多年度運転資金計画
    
    Returns:
        dict: サマリーデータ
    """
    summary = {
        'total_working_capital_change_3years': 0,
        'average_net_working_capital': 0,
        'average_cash_conversion_cycle': 0,
        'working_capital_efficiency_trend': ''
    }
    
    if not multi_year_plan['years']:
        return summary
    
    total_net_working_capital = 0
    total_cash_conversion_cycle = 0
    
    for year_plan in multi_year_plan['years']:
        summary['total_working_capital_change_3years'] += year_plan['working_capital_change']
        total_net_working_capital += year_plan['net_working_capital']
        total_cash_conversion_cycle += year_plan['cash_conversion_cycle']
    
    num_years = len(multi_year_plan['years'])
    summary['average_net_working_capital'] = total_net_working_capital / num_years
    summary['average_cash_conversion_cycle'] = total_cash_conversion_cycle / num_years
    
    # 効率性のトレンドを評価
    first_year = multi_year_plan['years'][0]
    last_year = multi_year_plan['years'][-1]
    
    if first_year['cash_conversion_cycle'] > last_year['cash_conversion_cycle']:
        summary['working_capital_efficiency_trend'] = '改善'
    elif first_year['cash_conversion_cycle'] < last_year['cash_conversion_cycle']:
        summary['working_capital_efficiency_trend'] = '悪化'
    else:
        summary['working_capital_efficiency_trend'] = '横ばい'
    
    return summary


def analyze_working_capital_efficiency(
    multi_year_plan: Dict[str, Any]
) -> Dict[str, Any]:
    """
    運転資金の効率性を分析
    
    Args:
        multi_year_plan: 多年度運転資金計画
    
    Returns:
        dict: 効率性分析結果
    """
    efficiency_analysis = {
        'years': []
    }
    
    for year_plan in multi_year_plan['years']:
        # 運転資金回転率
        working_capital_turnover = year_plan['sales'] / year_plan['net_working_capital'] if year_plan['net_working_capital'] > 0 else 0
        
        # 評価
        evaluation = evaluate_working_capital_efficiency(
            cash_conversion_cycle=year_plan['cash_conversion_cycle'],
            working_capital_turnover=working_capital_turnover
        )
        
        year_efficiency = {
            'year': year_plan['year'],
            'cash_conversion_cycle': year_plan['cash_conversion_cycle'],
            'working_capital_turnover': working_capital_turnover,
            'evaluation': evaluation
        }
        
        efficiency_analysis['years'].append(year_efficiency)
    
    return efficiency_analysis


def evaluate_working_capital_efficiency(
    cash_conversion_cycle: float,
    working_capital_turnover: float
) -> str:
    """
    運転資金効率性を評価
    
    Args:
        cash_conversion_cycle: キャッシュコンバージョンサイクル（日）
        working_capital_turnover: 運転資金回転率
    
    Returns:
        str: 評価コメント
    """
    comments = []
    
    if cash_conversion_cycle < 30:
        comments.append("キャッシュコンバージョンサイクルが短く、資金効率が良好です。")
    elif cash_conversion_cycle < 60:
        comments.append("キャッシュコンバージョンサイクルは適正範囲内です。")
    else:
        comments.append("キャッシュコンバージョンサイクルが長く、資金効率の改善が必要です。")
    
    if working_capital_turnover >= 10:
        comments.append("運転資金回転率が高く、効率的に運用されています。")
    elif working_capital_turnover >= 5:
        comments.append("運転資金回転率は適正範囲内です。")
    else:
        comments.append("運転資金回転率が低く、運転資金の削減を検討すべきです。")
    
    return " ".join(comments)


def format_multi_year_working_capital_plan_for_ui(multi_year_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    多年度運転資金計画をUI表示用に整形
    
    Args:
        multi_year_plan: 多年度運転資金計画
    
    Returns:
        dict: UI表示用の整形済みデータ
    """
    formatted_years = []
    
    for year_plan in multi_year_plan['years']:
        formatted_years.append({
            'year': year_plan['year'],
            'year_label': f"{year_plan['year']}年度",
            'sales': round(year_plan['sales'], 2),
            'sales_formatted': f"{year_plan['sales']:,.0f}円",
            'accounts_receivable_days': round(year_plan['accounts_receivable_days'], 1),
            'accounts_receivable_days_formatted': f"{year_plan['accounts_receivable_days']:.1f}日",
            'inventory_days': round(year_plan['inventory_days'], 1),
            'inventory_days_formatted': f"{year_plan['inventory_days']:.1f}日",
            'accounts_payable_days': round(year_plan['accounts_payable_days'], 1),
            'accounts_payable_days_formatted': f"{year_plan['accounts_payable_days']:.1f}日",
            'accounts_receivable': round(year_plan['accounts_receivable'], 2),
            'accounts_receivable_formatted': f"{year_plan['accounts_receivable']:,.0f}円",
            'inventory': round(year_plan['inventory'], 2),
            'inventory_formatted': f"{year_plan['inventory']:,.0f}円",
            'accounts_payable': round(year_plan['accounts_payable'], 2),
            'accounts_payable_formatted': f"{year_plan['accounts_payable']:,.0f}円",
            'net_working_capital': round(year_plan['net_working_capital'], 2),
            'net_working_capital_formatted': f"{year_plan['net_working_capital']:,.0f}円",
            'working_capital_change': round(year_plan['working_capital_change'], 2),
            'working_capital_change_formatted': f"{year_plan['working_capital_change']:+,.0f}円",
            'cash_conversion_cycle': round(year_plan['cash_conversion_cycle'], 1),
            'cash_conversion_cycle_formatted': f"{year_plan['cash_conversion_cycle']:.1f}日"
        })
    
    # サマリーを計算
    summary = calculate_multi_year_working_capital_summary(multi_year_plan)
    
    formatted_summary = {
        'total_working_capital_change_3years': round(summary['total_working_capital_change_3years'], 2),
        'total_working_capital_change_3years_formatted': f"{summary['total_working_capital_change_3years']:+,.0f}円",
        'average_net_working_capital': round(summary['average_net_working_capital'], 2),
        'average_net_working_capital_formatted': f"{summary['average_net_working_capital']:,.0f}円",
        'average_cash_conversion_cycle': round(summary['average_cash_conversion_cycle'], 1),
        'average_cash_conversion_cycle_formatted': f"{summary['average_cash_conversion_cycle']:.1f}日",
        'working_capital_efficiency_trend': summary['working_capital_efficiency_trend']
    }
    
    return {
        'base_year': multi_year_plan['base_year'],
        'years': formatted_years,
        'summary': formatted_summary
    }
