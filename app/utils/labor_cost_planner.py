"""
労務費管理計画モジュール

人件費の計画と管理を行います。
"""

from typing import Dict, List, Any


def calculate_labor_cost(
    base_salary: float,
    bonus: float = 0,
    social_insurance: float = 0,
    welfare_expense: float = 0,
    other_expense: float = 0
) -> Dict[str, float]:
    """
    労務費を計算
    
    Args:
        base_salary: 基本給
        bonus: 賞与
        social_insurance: 社会保険料
        welfare_expense: 福利厚生費
        other_expense: その他人件費
    
    Returns:
        労務費の内訳と合計
    """
    total_labor_cost = base_salary + bonus + social_insurance + welfare_expense + other_expense
    
    return {
        'base_salary': base_salary,
        'bonus': bonus,
        'social_insurance': social_insurance,
        'welfare_expense': welfare_expense,
        'other_expense': other_expense,
        'total_labor_cost': total_labor_cost
    }


def calculate_labor_cost_per_employee(total_labor_cost: float, employee_count: int) -> float:
    """
    従業員一人当たりの労務費を計算
    
    Args:
        total_labor_cost: 総労務費
        employee_count: 従業員数
    
    Returns:
        従業員一人当たりの労務費
    """
    if employee_count == 0:
        return 0.0
    
    return total_labor_cost / employee_count


def calculate_labor_cost_ratio(total_labor_cost: float, sales: float) -> float:
    """
    労務費率を計算
    
    Args:
        total_labor_cost: 総労務費
        sales: 売上高
    
    Returns:
        労務費率（%）
    """
    if sales == 0:
        return 0.0
    
    return (total_labor_cost / sales) * 100


def calculate_labor_productivity(sales: float, employee_count: int) -> float:
    """
    労働生産性（従業員一人当たり売上高）を計算
    
    Args:
        sales: 売上高
        employee_count: 従業員数
    
    Returns:
        労働生産性
    """
    if employee_count == 0:
        return 0.0
    
    return sales / employee_count


def plan_labor_cost(
    current_employee_count: int,
    planned_employee_count: int,
    average_salary: float,
    bonus_months: float = 2.0,
    social_insurance_rate: float = 0.15,
    welfare_rate: float = 0.05,
    other_rate: float = 0.02
) -> Dict[str, Any]:
    """
    労務費計画を作成
    
    Args:
        current_employee_count: 現在の従業員数
        planned_employee_count: 計画従業員数
        average_salary: 平均月額給与
        bonus_months: 賞与月数
        social_insurance_rate: 社会保険料率
        welfare_rate: 福利厚生費率
        other_rate: その他人件費率
    
    Returns:
        労務費計画の辞書
    """
    # 年間基本給
    annual_base_salary = average_salary * 12 * planned_employee_count
    
    # 年間賞与
    annual_bonus = average_salary * bonus_months * planned_employee_count
    
    # 社会保険料
    social_insurance = (annual_base_salary + annual_bonus) * social_insurance_rate
    
    # 福利厚生費
    welfare_expense = (annual_base_salary + annual_bonus) * welfare_rate
    
    # その他人件費
    other_expense = (annual_base_salary + annual_bonus) * other_rate
    
    # 総労務費
    total_labor_cost = annual_base_salary + annual_bonus + social_insurance + welfare_expense + other_expense
    
    # 従業員一人当たり労務費
    labor_cost_per_employee = total_labor_cost / planned_employee_count if planned_employee_count > 0 else 0
    
    # 増減
    employee_change = planned_employee_count - current_employee_count
    employee_change_rate = (employee_change / current_employee_count * 100) if current_employee_count > 0 else 0
    
    return {
        'current_employee_count': current_employee_count,
        'planned_employee_count': planned_employee_count,
        'employee_change': employee_change,
        'employee_change_rate': employee_change_rate,
        'average_salary': average_salary,
        'annual_base_salary': annual_base_salary,
        'annual_bonus': annual_bonus,
        'social_insurance': social_insurance,
        'welfare_expense': welfare_expense,
        'other_expense': other_expense,
        'total_labor_cost': total_labor_cost,
        'labor_cost_per_employee': labor_cost_per_employee
    }


def analyze_labor_cost_efficiency(
    total_labor_cost: float,
    sales: float,
    operating_income: float,
    employee_count: int
) -> Dict[str, Any]:
    """
    労務費の効率性を分析
    
    Args:
        total_labor_cost: 総労務費
        sales: 売上高
        operating_income: 営業利益
        employee_count: 従業員数
    
    Returns:
        効率性分析結果の辞書
    """
    # 労務費率
    labor_cost_ratio = calculate_labor_cost_ratio(total_labor_cost, sales)
    
    # 労働生産性
    labor_productivity = calculate_labor_productivity(sales, employee_count)
    
    # 従業員一人当たり労務費
    labor_cost_per_employee = calculate_labor_cost_per_employee(total_labor_cost, employee_count)
    
    # 従業員一人当たり営業利益
    operating_income_per_employee = operating_income / employee_count if employee_count > 0 else 0
    
    # 労働分配率（労務費 / 付加価値）
    # 付加価値 = 営業利益 + 労務費（簡易計算）
    value_added = operating_income + total_labor_cost
    labor_share_ratio = (total_labor_cost / value_added * 100) if value_added > 0 else 0
    
    return {
        'labor_cost_ratio': labor_cost_ratio,
        'labor_productivity': labor_productivity,
        'labor_cost_per_employee': labor_cost_per_employee,
        'operating_income_per_employee': operating_income_per_employee,
        'labor_share_ratio': labor_share_ratio,
        'evaluation': evaluate_labor_cost_efficiency(labor_cost_ratio, labor_share_ratio)
    }


def evaluate_labor_cost_efficiency(labor_cost_ratio: float, labor_share_ratio: float) -> str:
    """
    労務費効率性を評価
    
    Args:
        labor_cost_ratio: 労務費率
        labor_share_ratio: 労働分配率
    
    Returns:
        評価コメント
    """
    comments = []
    
    if labor_cost_ratio < 20:
        comments.append("労務費率が低く、人件費効率が良好です。")
    elif labor_cost_ratio < 30:
        comments.append("労務費率は適正範囲内です。")
    else:
        comments.append("労務費率が高く、人件費削減の検討が必要です。")
    
    if labor_share_ratio < 50:
        comments.append("労働分配率が低く、利益率が高い状態です。")
    elif labor_share_ratio < 70:
        comments.append("労働分配率は適正範囲内です。")
    else:
        comments.append("労働分配率が高く、従業員への分配が多い状態です。")
    
    return " ".join(comments)


def simulate_labor_cost_scenarios(
    base_scenario: Dict[str, float],
    scenarios: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    複数の労務費シナリオをシミュレーション
    
    Args:
        base_scenario: ベースシナリオ
        scenarios: シナリオのリスト
    
    Returns:
        シミュレーション結果のリスト
    """
    results = []
    
    for scenario in scenarios:
        result = plan_labor_cost(
            current_employee_count=base_scenario.get('current_employee_count', 0),
            planned_employee_count=scenario.get('planned_employee_count', 0),
            average_salary=scenario.get('average_salary', 0),
            bonus_months=scenario.get('bonus_months', 2.0),
            social_insurance_rate=scenario.get('social_insurance_rate', 0.15),
            welfare_rate=scenario.get('welfare_rate', 0.05),
            other_rate=scenario.get('other_rate', 0.02)
        )
        result['scenario_name'] = scenario.get('name', 'シナリオ')
        results.append(result)
    
    return results
