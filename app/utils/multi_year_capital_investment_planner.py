"""
多年度設備投資計画モジュール

3年間の設備投資計画を統合的に管理します。
"""

from typing import Dict, List, Any


def calculate_depreciation(
    investment_amount: float,
    useful_life: int,
    residual_value: float = 0,
    method: str = 'straight_line'
) -> float:
    """
    減価償却費を計算
    
    Args:
        investment_amount: 投資額
        useful_life: 耐用年数
        residual_value: 残存価値
        method: 償却方法（'straight_line': 定額法、'declining_balance': 定率法）
    
    Returns:
        float: 年間減価償却費
    """
    if method == 'straight_line':
        # 定額法
        if useful_life == 0:
            return 0
        return (investment_amount - residual_value) / useful_life
    elif method == 'declining_balance':
        # 定率法（簡易計算: 200%定率法）
        if useful_life == 0:
            return 0
        depreciation_rate = 2.0 / useful_life
        return investment_amount * depreciation_rate
    else:
        return 0


def create_multi_year_capital_investment_plan(
    base_year: int,
    yearly_investments: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    多年度設備投資計画を作成
    
    Args:
        base_year: 基準年度
        yearly_investments: 各年度の投資データのリスト
            各年度のデータには以下のキーを含む:
            - investments: 投資項目のリスト
                各投資項目には以下のキーを含む:
                - name: 投資項目名
                - amount: 投資額
                - useful_life: 耐用年数
                - residual_value: 残存価値
                - method: 償却方法
    
    Returns:
        dict: 多年度設備投資計画
    """
    multi_year_plan = {
        'base_year': base_year,
        'years': []
    }
    
    # 過去の投資を追跡（減価償却費の累積計算用）
    ongoing_investments = []
    
    for year_offset, yearly_investment in enumerate(yearly_investments):
        year = base_year + year_offset
        
        # 今年度の新規投資
        new_investments = yearly_investment.get('investments', [])
        total_new_investment = sum(inv.get('amount', 0) for inv in new_investments)
        
        # 今年度の新規投資を ongoing_investments に追加
        for inv in new_investments:
            ongoing_investments.append({
                'name': inv.get('name', ''),
                'amount': inv.get('amount', 0),
                'useful_life': inv.get('useful_life', 5),
                'residual_value': inv.get('residual_value', 0),
                'method': inv.get('method', 'straight_line'),
                'start_year': year,
                'remaining_life': inv.get('useful_life', 5)
            })
        
        # 今年度の減価償却費を計算
        total_depreciation = 0
        active_investments = []
        
        for inv in ongoing_investments:
            if inv['remaining_life'] > 0:
                depreciation = calculate_depreciation(
                    investment_amount=inv['amount'],
                    useful_life=inv['useful_life'],
                    residual_value=inv['residual_value'],
                    method=inv['method']
                )
                total_depreciation += depreciation
                inv['remaining_life'] -= 1
                active_investments.append(inv)
        
        # 残存期間がある投資のみを保持
        ongoing_investments = active_investments
        
        # 年度別計画を記録
        year_plan = {
            'year': year,
            'year_offset': year_offset,
            'new_investments': new_investments,
            'total_new_investment': total_new_investment,
            'total_depreciation': total_depreciation,
            'active_investments_count': len(ongoing_investments)
        }
        
        multi_year_plan['years'].append(year_plan)
    
    return multi_year_plan


def calculate_multi_year_investment_summary(multi_year_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    多年度設備投資計画のサマリーを計算
    
    Args:
        multi_year_plan: 多年度設備投資計画
    
    Returns:
        dict: サマリーデータ
    """
    summary = {
        'total_investment_3years': 0,
        'total_depreciation_3years': 0,
        'average_annual_investment': 0,
        'average_annual_depreciation': 0
    }
    
    if not multi_year_plan['years']:
        return summary
    
    for year_plan in multi_year_plan['years']:
        summary['total_investment_3years'] += year_plan['total_new_investment']
        summary['total_depreciation_3years'] += year_plan['total_depreciation']
    
    num_years = len(multi_year_plan['years'])
    summary['average_annual_investment'] = summary['total_investment_3years'] / num_years
    summary['average_annual_depreciation'] = summary['total_depreciation_3years'] / num_years
    
    return summary


def analyze_investment_efficiency(
    multi_year_plan: Dict[str, Any],
    sales_data: List[Dict[str, float]],
    fixed_assets_data: List[Dict[str, float]]
) -> Dict[str, Any]:
    """
    設備投資の効率性を分析
    
    Args:
        multi_year_plan: 多年度設備投資計画
        sales_data: 各年度の売上高データのリスト
        fixed_assets_data: 各年度の固定資産データのリスト
    
    Returns:
        dict: 効率性分析結果
    """
    efficiency_analysis = {
        'years': []
    }
    
    for year_offset, year_plan in enumerate(multi_year_plan['years']):
        if year_offset < len(sales_data) and year_offset < len(fixed_assets_data):
            sales = sales_data[year_offset].get('sales', 0)
            fixed_assets = fixed_assets_data[year_offset].get('fixed_assets', 0)
            
            # 固定資産回転率
            fixed_asset_turnover = sales / fixed_assets if fixed_assets > 0 else 0
            
            # 投資効率（売上高 / 新規投資額）
            investment_efficiency = sales / year_plan['total_new_investment'] if year_plan['total_new_investment'] > 0 else 0
            
            year_efficiency = {
                'year': year_plan['year'],
                'fixed_asset_turnover': fixed_asset_turnover,
                'investment_efficiency': investment_efficiency,
                'evaluation': evaluate_investment_efficiency(fixed_asset_turnover)
            }
            
            efficiency_analysis['years'].append(year_efficiency)
    
    return efficiency_analysis


def evaluate_investment_efficiency(fixed_asset_turnover: float) -> str:
    """
    投資効率性を評価
    
    Args:
        fixed_asset_turnover: 固定資産回転率
    
    Returns:
        str: 評価コメント
    """
    if fixed_asset_turnover >= 2.0:
        return "固定資産回転率が高く、設備投資の効率が良好です。"
    elif fixed_asset_turnover >= 1.0:
        return "固定資産回転率は適正範囲内です。"
    else:
        return "固定資産回転率が低く、設備投資の効率改善が必要です。"


def format_multi_year_capital_investment_plan_for_ui(multi_year_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    多年度設備投資計画をUI表示用に整形
    
    Args:
        multi_year_plan: 多年度設備投資計画
    
    Returns:
        dict: UI表示用の整形済みデータ
    """
    formatted_years = []
    
    for year_plan in multi_year_plan['years']:
        formatted_investments = []
        for inv in year_plan['new_investments']:
            formatted_investments.append({
                'name': inv.get('name', ''),
                'amount': round(inv.get('amount', 0), 2),
                'amount_formatted': f"{inv.get('amount', 0):,.0f}円",
                'useful_life': inv.get('useful_life', 0),
                'useful_life_formatted': f"{inv.get('useful_life', 0)}年"
            })
        
        formatted_years.append({
            'year': year_plan['year'],
            'year_label': f"{year_plan['year']}年度",
            'new_investments': formatted_investments,
            'total_new_investment': round(year_plan['total_new_investment'], 2),
            'total_new_investment_formatted': f"{year_plan['total_new_investment']:,.0f}円",
            'total_depreciation': round(year_plan['total_depreciation'], 2),
            'total_depreciation_formatted': f"{year_plan['total_depreciation']:,.0f}円",
            'active_investments_count': year_plan['active_investments_count']
        })
    
    # サマリーを計算
    summary = calculate_multi_year_investment_summary(multi_year_plan)
    
    formatted_summary = {
        'total_investment_3years': round(summary['total_investment_3years'], 2),
        'total_investment_3years_formatted': f"{summary['total_investment_3years']:,.0f}円",
        'total_depreciation_3years': round(summary['total_depreciation_3years'], 2),
        'total_depreciation_3years_formatted': f"{summary['total_depreciation_3years']:,.0f}円",
        'average_annual_investment': round(summary['average_annual_investment'], 2),
        'average_annual_investment_formatted': f"{summary['average_annual_investment']:,.0f}円",
        'average_annual_depreciation': round(summary['average_annual_depreciation'], 2),
        'average_annual_depreciation_formatted': f"{summary['average_annual_depreciation']:,.0f}円"
    }
    
    return {
        'base_year': multi_year_plan['base_year'],
        'years': formatted_years,
        'summary': formatted_summary
    }
