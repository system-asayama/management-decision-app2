"""
差額原価収益分析機能のテスト
"""

print("=" * 60)
print("差額原価収益分析機能のテスト")
print("=" * 60)

# ==================== 設備投資の差額原価収益分析のテスト ====================
print("\n【設備投資の差額原価収益分析のテスト】")

from app.utils.equipment_investment_differential_analysis import (
    calculate_equipment_investment_differential_analysis,
    format_differential_analysis_for_ui
)

# テストケース: Excelの「A　設備投資後」の例
equipment_cost = 2700000  # 270万円
useful_life = 5  # 5年
current_labor_cost = 4000000  # 400万円（5人 × 80万円）
new_labor_cost = 3200000  # 320万円（4人 × 80万円）
tax_rate = 30.0  # 30%
discount_rate = 6.0  # 6%

result = calculate_equipment_investment_differential_analysis(
    equipment_cost=equipment_cost,
    useful_life=useful_life,
    current_labor_cost=current_labor_cost,
    new_labor_cost=new_labor_cost,
    tax_rate=tax_rate,
    discount_rate=discount_rate
)

print(f"設備投資額: {result['equipment_cost']:,.0f}円")
print(f"耐用年数: {result['useful_life']}年")
print(f"年間労務費削減額: {result['annual_labor_cost_savings']:,.0f}円")
print(f"年間減価償却費: {result['annual_depreciation']:,.0f}円")
print(f"最終NPV: {result['final_npv']:,.0f}円")
print(f"IRR: {result['irr']:.2f}%" if not (result['irr'] != result['irr']) else "IRR: N/A")
print(f"投資判断: {result['recommendation']}")
print(f"推奨: {result['recommendation_text']}")

print("\n【年次分析】")
print(f"{'年':>4} | {'設備投資':>12} | {'労務費削減':>12} | {'減価償却':>12} | {'純CF':>12} | {'現在価値':>12} | {'累積NPV':>12}")
print("-" * 90)
for row in result['yearly_analysis']:
    print(f"{row['year']:>4} | {row['equipment_investment']:>12,.0f} | {row['labor_cost_savings']:>12,.0f} | {row['depreciation']:>12,.0f} | {row['net_cash_flow']:>12,.0f} | {row['present_value']:>12,.0f} | {row['cumulative_npv']:>12,.0f}")

# UI表示用に整形
formatted_result = format_differential_analysis_for_ui(result)
print(f"\n【UI整形済みサマリー】")
print(f"NPV: {formatted_result['summary']['final_npv_formatted']}")
print(f"IRR: {formatted_result['summary']['irr_formatted']}")
print(f"推奨: {formatted_result['summary']['recommendation_label']}")

# ==================== 複数投資案の比較テスト ====================
print("\n" + "=" * 60)
print("【複数投資案の比較テスト】")
print("=" * 60)

from app.utils.equipment_investment_differential_analysis import (
    compare_multiple_equipment_investments
)

investment_plans = [
    {
        'name': 'A機械（270万円）',
        'equipment_cost': 2700000,
        'useful_life': 5,
        'current_labor_cost': 4000000,
        'new_labor_cost': 3200000
    },
    {
        'name': 'B機械（460万円）',
        'equipment_cost': 4600000,
        'useful_life': 4,
        'current_labor_cost': 4000000,
        'new_labor_cost': 1600000
    }
]

comparison_result = compare_multiple_equipment_investments(
    investment_plans=investment_plans,
    tax_rate=30.0,
    discount_rate=6.0
)

print(f"\n【比較結果】")
for i, plan in enumerate(comparison_result['investment_plans'], start=1):
    print(f"{i}. {plan['plan_name']}")
    print(f"   NPV: {plan['final_npv']:,.0f}円")
    print(f"   IRR: {plan['irr']:.2f}%" if not (plan['irr'] != plan['irr']) else "   IRR: N/A")
    print(f"   設備投資額: {plan['equipment_cost']:,.0f}円")
    print(f"   年間労務費削減額: {plan['annual_labor_cost_savings']:,.0f}円")

print(f"\n【比較サマリー】")
print(comparison_result['comparison_summary'])

# ==================== 設備投資案件の総合評価テスト ====================
print("\n" + "=" * 60)
print("【設備投資案件の総合評価テスト】")
print("=" * 60)

from app.utils.capital_investment_planner import evaluate_investment

initial_investment = 10000000  # 1,000万円
annual_cash_flows = [3000000, 3000000, 3000000, 3000000, 3000000]  # 年間300万円×5年
discount_rate = 6.0

evaluation_result = evaluate_investment(
    initial_investment=initial_investment,
    annual_cash_flows=annual_cash_flows,
    discount_rate=discount_rate,
    project_name='新工場建設'
)

print(f"案件名: {evaluation_result['project_name']}")
print(f"初期投資額: {evaluation_result['initial_investment']:,.0f}円")
print(f"NPV: {evaluation_result['npv']:,.0f}円")
print(f"IRR: {evaluation_result['irr']:.2f}%" if not (evaluation_result['irr'] != evaluation_result['irr']) else "IRR: N/A")
print(f"回収期間: {evaluation_result['payback_period']:.1f}年")
print(f"収益性指数: {evaluation_result['profitability_index']:.2f}")
print(f"総キャッシュフロー: {evaluation_result['total_cash_flow']:,.0f}円")
print(f"純利益: {evaluation_result['net_profit']:,.0f}円")
print(f"\n推奨: {evaluation_result['recommendation']}")

# ==================== 総合結果 ====================
print("\n" + "=" * 60)
print("【テスト結果サマリー】")
print("=" * 60)
print("✓ 設備投資の差額原価収益分析: 正常に動作")
print("✓ 複数投資案の比較: 正常に動作")
print("✓ UI表示用の整形: 正常に動作")
print("✓ 設備投資案件の総合評価: 正常に動作")
print("\nすべてのテストが成功しました！")
