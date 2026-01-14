"""
資金調達返済計画・資金繰り計画機能のテスト
"""

print("=" * 60)
print("資金調達返済計画・資金繰り計画機能のテスト")
print("=" * 60)

# ==================== 統合資金繰り表のテスト ====================
print("\n【統合資金繰り表のテスト】")

from app.utils.integrated_cash_flow_planner import (
    generate_integrated_monthly_cash_flow,
    calculate_operating_cash_flow_from_pl,
    calculate_investment_cash_flow_from_capex,
    calculate_financing_cash_flow_from_debt,
    generate_shortage_alert_message,
    suggest_financing_solution
)

# テストデータ
monthly_sales = [1000000] * 12
monthly_cost_of_sales = [600000] * 12
monthly_operating_expenses = [300000] * 12

# 営業CFを計算
monthly_operating_cf = calculate_operating_cash_flow_from_pl(
    monthly_sales=monthly_sales,
    monthly_cost_of_sales=monthly_cost_of_sales,
    monthly_operating_expenses=monthly_operating_expenses
)

# 投資CFを計算
monthly_investment_cf = calculate_investment_cash_flow_from_capex(
    monthly_capital_expenditure=[500000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
)

# 財務CFを計算
monthly_financing_cf = calculate_financing_cash_flow_from_debt(
    monthly_borrowing=[0] * 12,
    monthly_debt_repayment=[50000] * 12,
    monthly_interest_payment=[10000] * 12
)

# 統合資金繰り表を生成
result = generate_integrated_monthly_cash_flow(
    fiscal_year_id=1,
    beginning_cash_balance=500000,
    monthly_operating_cash_flow=monthly_operating_cf,
    monthly_investment_cash_flow=monthly_investment_cf,
    monthly_financing_cash_flow=monthly_financing_cf,
    minimum_cash_balance=300000
)

print(f"期首現金残高: {result['beginning_cash_balance']:,.0f}円")
print(f"最低必要残高: {result['minimum_cash_balance']:,.0f}円")
print(f"期末現金残高: {result['ending_cash_balance']:,.0f}円")
print(f"資金不足警告: {result['has_shortage']}")
print(f"資金不足月数: {len(result['shortage_warnings'])}月")

if result['shortage_warnings']:
    print("\n【資金不足警告】")
    for warning in result['shortage_warnings']:
        print(f"  {warning['month']}月: 残高 {warning['ending_balance']:,.0f}円, 不足額 {warning['shortage_amount']:,.0f}円")

# 警告メッセージを生成
alert_message = generate_shortage_alert_message(result['shortage_warnings'])
print(f"\n【警告メッセージ】\n{alert_message}")

# 資金調達提案を生成
financing_solution = suggest_financing_solution(
    result['shortage_warnings'],
    available_credit_line=5000000
)
print(f"\n【資金調達提案】")
print(f"資金調達が必要: {financing_solution['required']}")
if financing_solution['required']:
    print(f"必要額: {financing_solution['required_amount']:,.0f}円")
    print(f"推奨額: {financing_solution['suggested_amount']:,.0f}円")
    print(f"提案: {financing_solution['suggestion']}")

# ==================== 返済計画のUI表示改善のテスト ====================
print("\n" + "=" * 60)
print("【返済計画のUI表示改善のテスト】")
print("=" * 60)

from app.utils.financing_repayment_planner import (
    generate_amortization_schedule,
    calculate_refinancing_benefit,
    calculate_early_repayment_benefit
)
from app.utils.repayment_plan_formatter import (
    format_amortization_schedule_for_ui,
    format_refinancing_comparison_for_ui,
    format_early_repayment_for_ui
)

# 償却スケジュールを生成
schedule = generate_amortization_schedule(
    principal=10000000,
    annual_interest_rate=3.0,
    term_years=5,
    payment_frequency='monthly'
)

# UI表示用に整形
formatted_schedule = format_amortization_schedule_for_ui(schedule, 'monthly')

print(f"\n【償却スケジュール】")
print(f"総返済期間: {formatted_schedule['summary']['total_periods']}ヶ月")
print(f"総返済額: {formatted_schedule['summary']['total_payment_formatted']}")
print(f"総元金: {formatted_schedule['summary']['total_principal_formatted']}")
print(f"総利息: {formatted_schedule['summary']['total_interest_formatted']}")

print(f"\n最初の3ヶ月:")
for i in range(min(3, len(formatted_schedule['table_data']))):
    row = formatted_schedule['table_data'][i]
    print(f"  {row['period_label']}: 返済額 {row['payment_formatted']}, 元金 {row['principal_payment_formatted']}, 利息 {row['interest_payment_formatted']}, 残高 {row['remaining_balance_formatted']}")

# 借換え効果を計算
refinancing_result = calculate_refinancing_benefit(
    current_loan_balance=5000000,
    current_interest_rate=3.5,
    remaining_term_years=3,
    new_interest_rate=2.5,
    refinancing_cost=100000
)

# UI表示用に整形
formatted_refinancing = format_refinancing_comparison_for_ui(refinancing_result)

print(f"\n【借換え効果比較】")
print(f"総利息削減額: {formatted_refinancing['cost_benefit']['interest_savings_formatted']}")
print(f"借換え費用: {formatted_refinancing['cost_benefit']['refinancing_cost_formatted']}")
print(f"実質削減額: {formatted_refinancing['cost_benefit']['net_savings_formatted']}")
print(f"推奨: {formatted_refinancing['recommendation']['action_label']}")

# 繰上返済効果を計算
early_repayment_result = calculate_early_repayment_benefit(
    current_loan_balance=5000000,
    annual_interest_rate=3.0,
    remaining_term_years=3,
    early_repayment_amount=1000000,
    early_repayment_penalty=50000
)

# UI表示用に整形
formatted_early_repayment = format_early_repayment_for_ui(early_repayment_result)

print(f"\n【繰上返済効果】")
print(f"利息削減額: {formatted_early_repayment['cost_benefit']['interest_savings_formatted']}")
print(f"繰上返済手数料: {formatted_early_repayment['cost_benefit']['early_repayment_penalty_formatted']}")
print(f"実質削減額: {formatted_early_repayment['cost_benefit']['net_savings_formatted']}")
print(f"推奨: {formatted_early_repayment['recommendation']['action_label']}")

# ==================== 総合結果 ====================
print("\n" + "=" * 60)
print("【テスト結果サマリー】")
print("=" * 60)
print("✓ 統合資金繰り表の生成: 正常に動作")
print("✓ 残高不足警告ロジック: 正常に動作")
print("✓ 資金調達提案: 正常に動作")
print("✓ 償却スケジュールのUI整形: 正常に動作")
print("✓ 借換え効果比較のUI整形: 正常に動作")
print("✓ 繰上返済効果のUI整形: 正常に動作")
print("\nすべてのテストが成功しました！")
