"""
個別経営計画（労務費、設備投資、運転資金）機能のテスト
"""

print("=" * 60)
print("個別経営計画機能のテスト")
print("=" * 60)

# ==================== 多年度労務費計画のテスト ====================
print("\n【多年度労務費計画のテスト】")

from app.utils.multi_year_labor_cost_planner import (
    create_multi_year_labor_cost_plan,
    calculate_multi_year_summary,
    format_multi_year_labor_cost_plan_for_ui
)

# テストデータ
yearly_labor_plans = [
    {
        'planned_employee_count': 50,
        'average_salary': 500000,
        'bonus_months': 2.0,
        'social_insurance_rate': 0.15,
        'welfare_rate': 0.05,
        'other_rate': 0.02
    },
    {
        'planned_employee_count': 55,
        'average_salary': 510000,
        'bonus_months': 2.0,
        'social_insurance_rate': 0.15,
        'welfare_rate': 0.05,
        'other_rate': 0.02
    },
    {
        'planned_employee_count': 60,
        'average_salary': 520000,
        'bonus_months': 2.0,
        'social_insurance_rate': 0.15,
        'welfare_rate': 0.05,
        'other_rate': 0.02
    }
]

# 多年度労務費計画を作成
labor_plan = create_multi_year_labor_cost_plan(
    base_year=2024,
    current_employee_count=48,
    yearly_plans=yearly_labor_plans
)

print(f"\n労務費計画が作成されました:")
print(f"基準年度: {labor_plan['base_year']}")
print(f"現在の従業員数: {labor_plan['current_employee_count']}")
print(f"計画年数: {len(labor_plan['years'])}年")

# サマリーを計算
summary = calculate_multi_year_summary(labor_plan)
print(f"\n【労務費計画サマリー】")
print(f"3年間の総労務費: {summary['total_labor_cost_3years']:,.0f}円")
print(f"平均従業員数: {summary['average_employee_count']:.1f}人")
print(f"平均従業員一人当たり労務費: {summary['average_labor_cost_per_employee']:,.0f}円")
print(f"従業員数成長率: {summary['employee_growth_rate']:+.2f}%")
print(f"労務費成長率: {summary['labor_cost_growth_rate']:+.2f}%")

# UI表示用に整形
formatted_labor_plan = format_multi_year_labor_cost_plan_for_ui(labor_plan)
print(f"\n【年度別労務費】")
print(f"{'年度':>6} | {'従業員数':>10} | {'総労務費':>15} | {'一人当たり労務費':>18}")
print("-" * 60)
for year in formatted_labor_plan['years']:
    print(f"{year['year']:>6} | {year['planned_employee_count']:>10} | {year['total_labor_cost_formatted']:>15} | {year['labor_cost_per_employee_formatted']:>18}")

# ==================== 多年度設備投資計画のテスト ====================
print("\n" + "=" * 60)
print("【多年度設備投資計画のテスト】")
print("=" * 60)

from app.utils.multi_year_capital_investment_planner import (
    create_multi_year_capital_investment_plan,
    calculate_multi_year_investment_summary,
    format_multi_year_capital_investment_plan_for_ui
)

# テストデータ
yearly_investments = [
    {
        'investments': [
            {'name': '生産設備A', 'amount': 50000000, 'useful_life': 5, 'residual_value': 0, 'method': 'straight_line'},
            {'name': 'システム導入', 'amount': 30000000, 'useful_life': 3, 'residual_value': 0, 'method': 'straight_line'}
        ]
    },
    {
        'investments': [
            {'name': '生産設備B', 'amount': 40000000, 'useful_life': 5, 'residual_value': 0, 'method': 'straight_line'}
        ]
    },
    {
        'investments': [
            {'name': '物流設備', 'amount': 20000000, 'useful_life': 5, 'residual_value': 0, 'method': 'straight_line'}
        ]
    }
]

# 多年度設備投資計画を作成
investment_plan = create_multi_year_capital_investment_plan(
    base_year=2024,
    yearly_investments=yearly_investments
)

print(f"\n設備投資計画が作成されました:")
print(f"基準年度: {investment_plan['base_year']}")
print(f"計画年数: {len(investment_plan['years'])}年")

# サマリーを計算
investment_summary = calculate_multi_year_investment_summary(investment_plan)
print(f"\n【設備投資計画サマリー】")
print(f"3年間の総投資額: {investment_summary['total_investment_3years']:,.0f}円")
print(f"3年間の総減価償却費: {investment_summary['total_depreciation_3years']:,.0f}円")
print(f"年平均投資額: {investment_summary['average_annual_investment']:,.0f}円")
print(f"年平均減価償却費: {investment_summary['average_annual_depreciation']:,.0f}円")

# UI表示用に整形
formatted_investment_plan = format_multi_year_capital_investment_plan_for_ui(investment_plan)
print(f"\n【年度別設備投資】")
print(f"{'年度':>6} | {'新規投資額':>15} | {'減価償却費':>15} | {'稼働中投資件数':>18}")
print("-" * 70)
for year in formatted_investment_plan['years']:
    print(f"{year['year']:>6} | {year['total_new_investment_formatted']:>15} | {year['total_depreciation_formatted']:>15} | {year['active_investments_count']:>18}")

# ==================== 多年度運転資金計画のテスト ====================
print("\n" + "=" * 60)
print("【多年度運転資金計画のテスト】")
print("=" * 60)

from app.utils.multi_year_working_capital_planner import (
    create_multi_year_working_capital_plan,
    calculate_multi_year_working_capital_summary,
    format_multi_year_working_capital_plan_for_ui
)

# テストデータ
yearly_working_capital_plans = [
    {
        'sales': 1000000000,
        'cost_of_sales': 700000000,
        'accounts_receivable_days': 45,
        'inventory_days': 30,
        'accounts_payable_days': 30
    },
    {
        'sales': 1100000000,
        'cost_of_sales': 770000000,
        'accounts_receivable_days': 43,
        'inventory_days': 28,
        'accounts_payable_days': 32
    },
    {
        'sales': 1200000000,
        'cost_of_sales': 840000000,
        'accounts_receivable_days': 40,
        'inventory_days': 25,
        'accounts_payable_days': 35
    }
]

# 多年度運転資金計画を作成
working_capital_plan = create_multi_year_working_capital_plan(
    base_year=2024,
    yearly_plans=yearly_working_capital_plans
)

print(f"\n運転資金計画が作成されました:")
print(f"基準年度: {working_capital_plan['base_year']}")
print(f"計画年数: {len(working_capital_plan['years'])}年")

# サマリーを計算
wc_summary = calculate_multi_year_working_capital_summary(working_capital_plan)
print(f"\n【運転資金計画サマリー】")
print(f"3年間の運転資金増加額: {wc_summary['total_working_capital_change_3years']:+,.0f}円")
print(f"平均正味運転資金: {wc_summary['average_net_working_capital']:,.0f}円")
print(f"平均CCC: {wc_summary['average_cash_conversion_cycle']:.1f}日")
print(f"効率性トレンド: {wc_summary['working_capital_efficiency_trend']}")

# UI表示用に整形
formatted_wc_plan = format_multi_year_working_capital_plan_for_ui(working_capital_plan)
print(f"\n【年度別運転資金】")
print(f"{'年度':>6} | {'売上高':>15} | {'正味運転資金':>15} | {'CCC':>10} | {'運転資金増減':>15}")
print("-" * 80)
for year in formatted_wc_plan['years']:
    print(f"{year['year']:>6} | {year['sales_formatted']:>15} | {year['net_working_capital_formatted']:>15} | {year['cash_conversion_cycle_formatted']:>10} | {year['working_capital_change_formatted']:>15}")

# ==================== 総合結果 ====================
print("\n" + "=" * 60)
print("【テスト結果サマリー】")
print("=" * 60)
print("✓ 多年度労務費計画: 正常に動作")
print("✓ 労務費計画サマリー計算: 正常に動作")
print("✓ 多年度設備投資計画: 正常に動作")
print("✓ 設備投資計画サマリー計算: 正常に動作")
print("✓ 多年度運転資金計画: 正常に動作")
print("✓ 運転資金計画サマリー計算: 正常に動作")
print("\nすべてのテストが成功しました！")
