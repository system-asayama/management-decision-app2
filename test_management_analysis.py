"""
経営指標分析APIのテスト
"""
from app.services.analysis_service import AnalysisService
from app.utils.evaluation_helpers import evaluate_multiple_indicators

# テストデータ
current_data = {
    'sales': 100000000,
    'cost_of_sales': 60000000,
    'gross_profit': 40000000,
    'selling_general_admin_expenses': 25000000,
    'operating_income': 15000000,
    'ordinary_income': 14000000,
    'income_before_tax': 13000000,
    'net_income': 9000000,
    'total_assets': 150000000,
    'current_assets': 80000000,
    'fixed_assets': 70000000,
    'total_liabilities': 80000000,
    'current_liabilities': 40000000,
    'fixed_liabilities': 40000000,
    'net_assets': 70000000,
    'gross_added_value': 65000000,
    'total_labor_cost': 30000000,
    'executive_compensation': 5000000,
    'capital_regeneration_cost': 10000000,
    'research_development_expenses': 2000000,
    'general_expenses': 25000000,
    'number_of_employees': 50,
}

previous_data = {
    'sales': 90000000,
    'cost_of_sales': 55000000,
    'gross_profit': 35000000,
    'selling_general_admin_expenses': 22000000,
    'operating_income': 13000000,
    'ordinary_income': 12000000,
    'income_before_tax': 11000000,
    'net_income': 7500000,
    'total_assets': 140000000,
    'current_assets': 75000000,
    'fixed_assets': 65000000,
    'total_liabilities': 75000000,
    'current_liabilities': 38000000,
    'fixed_liabilities': 37000000,
    'net_assets': 65000000,
    'gross_added_value': 57000000,
    'total_labor_cost': 28000000,
    'executive_compensation': 4500000,
    'capital_regeneration_cost': 9000000,
    'research_development_expenses': 1800000,
    'general_expenses': 22000000,
    'number_of_employees': 48,
}

print("=" * 80)
print("経営指標分析テスト")
print("=" * 80)

# 1. 成長力指標
print("\n【1. 成長力指標】")
growth_indicators = AnalysisService.calculate_growth_indicators(current_data, previous_data)
for key, value in growth_indicators.items():
    if value >= 10.0:
        grade = '◎'
    elif value >= 0.0:
        grade = '◯'
    elif value >= -10.0:
        grade = '△'
    else:
        grade = '×'
    print(f"{key}: {value:.2f}% ({grade})")

# 2. 収益力指標
print("\n【2. 収益力指標】")
profitability_current = AnalysisService.calculate_profitability_indicators(current_data)
profitability_previous = AnalysisService.calculate_profitability_indicators(previous_data)
profitability_with_grades = evaluate_multiple_indicators(profitability_current, profitability_previous)
for key, value in profitability_with_grades.items():
    print(f"{key}: 当年={value['thisYear']:.2f}%, 前年={value['prevYear']:.2f}%, 増減率={value['ratio']:.2f}% ({value['grade']})")

# 3. 資金力指標
print("\n【3. 資金力指標】")
financial_strength_current = AnalysisService.calculate_financial_strength_indicators(current_data)
financial_strength_previous = AnalysisService.calculate_financial_strength_indicators(previous_data)
financial_strength_with_grades = evaluate_multiple_indicators(financial_strength_current, financial_strength_previous)
for key, value in financial_strength_with_grades.items():
    print(f"{key}: 当年={value['thisYear']:.2f}%, 前年={value['prevYear']:.2f}%, 増減率={value['ratio']:.2f}% ({value['grade']})")

# 4. 生産力指標
print("\n【4. 生産力指標】")
productivity_current = AnalysisService.calculate_productivity_indicators(current_data)
productivity_previous = AnalysisService.calculate_productivity_indicators(previous_data)
productivity_with_grades = evaluate_multiple_indicators(productivity_current, productivity_previous)
for key, value in productivity_with_grades.items():
    print(f"{key}: 当年={value['thisYear']:.2f}, 前年={value['prevYear']:.2f}, 増減率={value['ratio']:.2f}% ({value['grade']})")

print("\n" + "=" * 80)
print("テスト完了")
print("=" * 80)
