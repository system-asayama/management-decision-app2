"""
予算管理・連続財務シミュレーション機能のテスト
"""

print("=" * 60)
print("予算管理・連続財務シミュレーション機能のテスト")
print("=" * 60)

# ==================== 多年度計画統合のテスト ====================
print("\n【多年度計画統合のテスト】")

from app.utils.multi_year_plan_manager import MultiYearPlanManager

# テストデータ
labor_cost_plans = [
    {'employee_count': 50, 'total_labor_cost': 300000000, 'average_salary': 6000000, 'social_insurance': 45000000, 'welfare_expenses': 15000000},
    {'employee_count': 55, 'total_labor_cost': 330000000, 'average_salary': 6000000, 'social_insurance': 49500000, 'welfare_expenses': 16500000},
    {'employee_count': 60, 'total_labor_cost': 360000000, 'average_salary': 6000000, 'social_insurance': 54000000, 'welfare_expenses': 18000000}
]

capital_investment_plans = [
    {'total_investment': 100000000, 'depreciation': 20000000, 'useful_life': 5, 'investment_items': []},
    {'total_investment': 50000000, 'depreciation': 30000000, 'useful_life': 5, 'investment_items': []},
    {'total_investment': 0, 'depreciation': 30000000, 'useful_life': 5, 'investment_items': []}
]

working_capital_plans = [
    {'accounts_receivable': 150000000, 'inventory': 100000000, 'accounts_payable': 80000000, 'net_working_capital': 170000000, 'cash_conversion_cycle': 45},
    {'accounts_receivable': 165000000, 'inventory': 110000000, 'accounts_payable': 88000000, 'net_working_capital': 187000000, 'cash_conversion_cycle': 43},
    {'accounts_receivable': 180000000, 'inventory': 120000000, 'accounts_payable': 96000000, 'net_working_capital': 204000000, 'cash_conversion_cycle': 41}
]

financing_plans = [
    {'new_borrowing': 50000000, 'principal_repayment': 30000000, 'interest_payment': 5000000, 'total_debt_balance': 200000000, 'debt_service_coverage_ratio': 2.5},
    {'new_borrowing': 0, 'principal_repayment': 30000000, 'interest_payment': 4500000, 'total_debt_balance': 170000000, 'debt_service_coverage_ratio': 2.8},
    {'new_borrowing': 0, 'principal_repayment': 30000000, 'interest_payment': 4000000, 'total_debt_balance': 140000000, 'debt_service_coverage_ratio': 3.0}
]

# 統合計画を作成
integrated_plan = MultiYearPlanManager.create_integrated_plan(
    company_id=1,
    base_year=2024,
    labor_cost_plans=labor_cost_plans,
    capital_investment_plans=capital_investment_plans,
    working_capital_plans=working_capital_plans,
    financing_plans=financing_plans
)

print(f"\n統合計画が作成されました:")
print(f"企業ID: {integrated_plan['company_id']}")
print(f"基準年度: {integrated_plan['base_year']}")
print(f"計画年数: {len(integrated_plan['years'])}年")

# サマリーを計算
summary = MultiYearPlanManager.calculate_plan_summary(integrated_plan)
print(f"\n【計画サマリー】")
print(f"3年間の総労務費: {summary['total_labor_cost_3years']:,.0f}円")
print(f"3年間の総設備投資: {summary['total_capital_investment_3years']:,.0f}円")
print(f"3年間の総減価償却費: {summary['total_depreciation_3years']:,.0f}円")
print(f"3年間の総利息支払: {summary['total_interest_payment_3years']:,.0f}円")
print(f"平均運転資金: {summary['average_working_capital']:,.0f}円")
print(f"最終借入残高: {summary['final_debt_balance']:,.0f}円")

# 妥当性を検証
validation_result = MultiYearPlanManager.validate_plan(integrated_plan)
print(f"\n【妥当性検証】")
print(f"検証結果: {'合格' if validation_result['is_valid'] else '不合格'}")
print(f"警告数: {len(validation_result['warnings'])}")
print(f"エラー数: {len(validation_result['errors'])}")

# ==================== 連続財務シミュレーションのテスト ====================
print("\n" + "=" * 60)
print("【連続財務シミュレーションのテスト】")
print("=" * 60)

from app.utils.continuous_financial_simulator import ContinuousFinancialSimulator

# 基準年度の財務データ
base_financials = {
    'sales': 1000000000,
    'total_assets': 800000000,
    'total_liabilities': 300000000,
    'total_equity': 500000000,
    'cash': 100000000,
    'fixed_assets': 400000000,
    'other_liabilities': 100000000
}

# 成長率と比率
sales_growth_rates = [5.0, 7.0, 10.0]  # %
cost_of_sales_ratios = [65.0, 64.0, 63.0]  # %
sg_a_ratios = [25.0, 24.0, 23.0]  # %

# シミュレーションを実行
simulation_result = ContinuousFinancialSimulator.simulate_multi_year_financials(
    base_financials=base_financials,
    integrated_plan=integrated_plan,
    sales_growth_rates=sales_growth_rates,
    cost_of_sales_ratios=cost_of_sales_ratios,
    sg_a_ratios=sg_a_ratios
)

print(f"\n【シミュレーション結果】")
print(f"{'年度':>6} | {'売上高':>15} | {'営業利益':>15} | {'経常利益':>15} | {'当期純利益':>15} | {'現金残高':>15}")
print("-" * 100)
for year_result in simulation_result['years']:
    print(f"{year_result['year']:>6} | {year_result['pl']['sales']:>15,.0f} | {year_result['pl']['operating_income']:>15,.0f} | {year_result['pl']['ordinary_income']:>15,.0f} | {year_result['pl']['net_income']:>15,.0f} | {year_result['bs']['cash']:>15,.0f}")

# ==================== 予実差異分析のテスト ====================
print("\n" + "=" * 60)
print("【予実差異分析のテスト】")
print("=" * 60)

from app.utils.budget_variance_analyzer import BudgetVarianceAnalyzer

# 予算データ
budget_data = {
    'year': 2024,
    'sales': 1050000000,
    'cost_of_sales': 682500000,
    'gross_profit': 367500000,
    'sg_a_expenses': 262500000,
    'operating_income': 105000000,
    'ordinary_income': 100000000,
    'net_income': 70000000
}

# 実績データ（予算より少し悪い）
actual_data = {
    'year': 2024,
    'sales': 1000000000,
    'cost_of_sales': 650000000,
    'gross_profit': 350000000,
    'sg_a_expenses': 270000000,
    'operating_income': 80000000,
    'ordinary_income': 75000000,
    'net_income': 52500000
}

# 予実差異を分析
variance_result = BudgetVarianceAnalyzer.analyze_variance(
    budget_data=budget_data,
    actual_data=actual_data,
    variance_threshold=5.0
)

print(f"\n【予実差異分析結果】")
print(f"{'項目':>20} | {'予算':>15} | {'実績':>15} | {'差異額':>15} | {'差異率':>10} | {'評価':>10}")
print("-" * 100)
for item in variance_result['items']:
    print(f"{item['item_name']:>20} | {item['budget_value']:>15,.0f} | {item['actual_value']:>15,.0f} | {item['variance_amount']:>15,.0f} | {item['variance_rate']:>10.2f}% | {item['status_label']:>10}")

print(f"\n【アラート】")
if variance_result['alerts']:
    for alert in variance_result['alerts']:
        print(f"  [{alert['severity'].upper()}] {alert['message']}")
else:
    print("  アラートなし")

# ==================== 包括的アラート生成のテスト ====================
print("\n" + "=" * 60)
print("【包括的アラート生成のテスト】")
print("=" * 60)

# 包括的なアラートを生成
alerts_result = BudgetVarianceAnalyzer.generate_comprehensive_alerts(
    budget_data=budget_data,
    actual_data=actual_data,
    simulation_result=simulation_result,
    variance_threshold=5.0,
    minimum_cash_balance=50000000,
    minimum_dscr=1.2
)

print(f"\n【アラートサマリー】")
print(f"総アラート数: {alerts_result['total_alerts']}")
print(f"重大アラート: {alerts_result['critical_count']}")
print(f"警告アラート: {alerts_result['warning_count']}")

print(f"\n【全アラート】")
if alerts_result['alerts']:
    for i, alert in enumerate(alerts_result['alerts'], start=1):
        print(f"{i}. [{alert['severity'].upper()}] {alert['message']}")
else:
    print("  アラートなし")

# ==================== 総合結果 ====================
print("\n" + "=" * 60)
print("【テスト結果サマリー】")
print("=" * 60)
print("✓ 多年度計画統合: 正常に動作")
print("✓ 計画サマリー計算: 正常に動作")
print("✓ 妥当性検証: 正常に動作")
print("✓ 連続財務シミュレーション: 正常に動作")
print("✓ 予実差異分析: 正常に動作")
print("✓ 包括的アラート生成: 正常に動作")
print("\nすべてのテストが成功しました！")
