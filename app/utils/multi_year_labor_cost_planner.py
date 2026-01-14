"""
多年度労務費計画モジュール

3年間の労務費計画を統合的に管理します。
"""

from typing import Dict, List, Any
from .labor_cost_planner import plan_labor_cost, analyze_labor_cost_efficiency


def create_multi_year_labor_cost_plan(
    base_year: int,
    current_employee_count: int,
    yearly_plans: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    多年度労務費計画を作成
    
    Args:
        base_year: 基準年度
        current_employee_count: 現在の従業員数
        yearly_plans: 各年度の計画データのリスト
            各年度のデータには以下のキーを含む:
            - planned_employee_count: 計画従業員数
            - average_salary: 平均月額給与
            - bonus_months: 賞与月数
            - social_insurance_rate: 社会保険料率
            - welfare_rate: 福利厚生費率
            - other_rate: その他人件費率
    
    Returns:
        dict: 多年度労務費計画
    """
    multi_year_plan = {
        'base_year': base_year,
        'current_employee_count': current_employee_count,
        'years': []
    }
    
    prev_employee_count = current_employee_count
    
    for year_offset, yearly_plan in enumerate(yearly_plans):
        year = base_year + year_offset
        
        # 年度別労務費計画を作成
        year_plan = plan_labor_cost(
            current_employee_count=prev_employee_count,
            planned_employee_count=yearly_plan.get('planned_employee_count', prev_employee_count),
            average_salary=yearly_plan.get('average_salary', 0),
            bonus_months=yearly_plan.get('bonus_months', 2.0),
            social_insurance_rate=yearly_plan.get('social_insurance_rate', 0.15),
            welfare_rate=yearly_plan.get('welfare_rate', 0.05),
            other_rate=yearly_plan.get('other_rate', 0.02)
        )
        
        year_plan['year'] = year
        year_plan['year_offset'] = year_offset
        
        multi_year_plan['years'].append(year_plan)
        
        # 次年度の基準として今年度の計画従業員数を使用
        prev_employee_count = year_plan['planned_employee_count']
    
    return multi_year_plan


def calculate_multi_year_summary(multi_year_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    多年度労務費計画のサマリーを計算
    
    Args:
        multi_year_plan: 多年度労務費計画
    
    Returns:
        dict: サマリーデータ
    """
    summary = {
        'total_labor_cost_3years': 0,
        'average_employee_count': 0,
        'average_labor_cost_per_employee': 0,
        'employee_growth_rate': 0,
        'labor_cost_growth_rate': 0
    }
    
    if not multi_year_plan['years']:
        return summary
    
    # 3年間の合計
    total_employees = 0
    total_labor_cost_per_employee = 0
    
    for year_plan in multi_year_plan['years']:
        summary['total_labor_cost_3years'] += year_plan['total_labor_cost']
        total_employees += year_plan['planned_employee_count']
        total_labor_cost_per_employee += year_plan['labor_cost_per_employee']
    
    # 平均値を計算
    num_years = len(multi_year_plan['years'])
    summary['average_employee_count'] = total_employees / num_years
    summary['average_labor_cost_per_employee'] = total_labor_cost_per_employee / num_years
    
    # 成長率を計算
    first_year = multi_year_plan['years'][0]
    last_year = multi_year_plan['years'][-1]
    
    if first_year['planned_employee_count'] > 0:
        summary['employee_growth_rate'] = (
            (last_year['planned_employee_count'] - first_year['planned_employee_count']) /
            first_year['planned_employee_count'] * 100
        )
    
    if first_year['total_labor_cost'] > 0:
        summary['labor_cost_growth_rate'] = (
            (last_year['total_labor_cost'] - first_year['total_labor_cost']) /
            first_year['total_labor_cost'] * 100
        )
    
    return summary


def analyze_multi_year_labor_cost_efficiency(
    multi_year_plan: Dict[str, Any],
    sales_data: List[Dict[str, float]],
    operating_income_data: List[Dict[str, float]]
) -> Dict[str, Any]:
    """
    多年度労務費の効率性を分析
    
    Args:
        multi_year_plan: 多年度労務費計画
        sales_data: 各年度の売上高データのリスト
        operating_income_data: 各年度の営業利益データのリスト
    
    Returns:
        dict: 効率性分析結果
    """
    efficiency_analysis = {
        'years': []
    }
    
    for year_offset, year_plan in enumerate(multi_year_plan['years']):
        if year_offset < len(sales_data) and year_offset < len(operating_income_data):
            sales = sales_data[year_offset].get('sales', 0)
            operating_income = operating_income_data[year_offset].get('operating_income', 0)
            
            year_efficiency = analyze_labor_cost_efficiency(
                total_labor_cost=year_plan['total_labor_cost'],
                sales=sales,
                operating_income=operating_income,
                employee_count=year_plan['planned_employee_count']
            )
            
            year_efficiency['year'] = year_plan['year']
            efficiency_analysis['years'].append(year_efficiency)
    
    return efficiency_analysis


def format_multi_year_labor_cost_plan_for_ui(multi_year_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    多年度労務費計画をUI表示用に整形
    
    Args:
        multi_year_plan: 多年度労務費計画
    
    Returns:
        dict: UI表示用の整形済みデータ
    """
    formatted_years = []
    
    for year_plan in multi_year_plan['years']:
        formatted_years.append({
            'year': year_plan['year'],
            'year_label': f"{year_plan['year']}年度",
            'planned_employee_count': year_plan['planned_employee_count'],
            'employee_change': year_plan['employee_change'],
            'employee_change_rate': round(year_plan['employee_change_rate'], 2),
            'employee_change_rate_formatted': f"{year_plan['employee_change_rate']:+.2f}%",
            'average_salary': round(year_plan['average_salary'], 2),
            'average_salary_formatted': f"{year_plan['average_salary']:,.0f}円",
            'annual_base_salary': round(year_plan['annual_base_salary'], 2),
            'annual_base_salary_formatted': f"{year_plan['annual_base_salary']:,.0f}円",
            'annual_bonus': round(year_plan['annual_bonus'], 2),
            'annual_bonus_formatted': f"{year_plan['annual_bonus']:,.0f}円",
            'social_insurance': round(year_plan['social_insurance'], 2),
            'social_insurance_formatted': f"{year_plan['social_insurance']:,.0f}円",
            'welfare_expense': round(year_plan['welfare_expense'], 2),
            'welfare_expense_formatted': f"{year_plan['welfare_expense']:,.0f}円",
            'other_expense': round(year_plan['other_expense'], 2),
            'other_expense_formatted': f"{year_plan['other_expense']:,.0f}円",
            'total_labor_cost': round(year_plan['total_labor_cost'], 2),
            'total_labor_cost_formatted': f"{year_plan['total_labor_cost']:,.0f}円",
            'labor_cost_per_employee': round(year_plan['labor_cost_per_employee'], 2),
            'labor_cost_per_employee_formatted': f"{year_plan['labor_cost_per_employee']:,.0f}円"
        })
    
    # サマリーを計算
    summary = calculate_multi_year_summary(multi_year_plan)
    
    formatted_summary = {
        'total_labor_cost_3years': round(summary['total_labor_cost_3years'], 2),
        'total_labor_cost_3years_formatted': f"{summary['total_labor_cost_3years']:,.0f}円",
        'average_employee_count': round(summary['average_employee_count'], 1),
        'average_employee_count_formatted': f"{summary['average_employee_count']:.1f}人",
        'average_labor_cost_per_employee': round(summary['average_labor_cost_per_employee'], 2),
        'average_labor_cost_per_employee_formatted': f"{summary['average_labor_cost_per_employee']:,.0f}円",
        'employee_growth_rate': round(summary['employee_growth_rate'], 2),
        'employee_growth_rate_formatted': f"{summary['employee_growth_rate']:+.2f}%",
        'labor_cost_growth_rate': round(summary['labor_cost_growth_rate'], 2),
        'labor_cost_growth_rate_formatted': f"{summary['labor_cost_growth_rate']:+.2f}%"
    }
    
    return {
        'base_year': multi_year_plan['base_year'],
        'current_employee_count': multi_year_plan['current_employee_count'],
        'years': formatted_years,
        'summary': formatted_summary
    }
