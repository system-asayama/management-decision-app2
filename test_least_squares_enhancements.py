"""
最小二乗法機能の拡張テスト
"""
from app.utils.least_squares_forecaster import (
    analyze_cost_structure,
    forecast_costs
)

print("=" * 80)
print("最小二乗法機能の拡張テスト")
print("=" * 80)

# テストデータ（3年分の売上高と原価）
historical_data = [
    {'year': 1, 'sales': 1000000000, 'cost_of_sales': 600000000, 'operating_expenses': 250000000},
    {'year': 2, 'sales': 1100000000, 'cost_of_sales': 660000000, 'operating_expenses': 260000000},
    {'year': 3, 'sales': 1200000000, 'cost_of_sales': 720000000, 'operating_expenses': 270000000},
]

# 1. 費用構造分析（固定費と変動費率）
print("\n【1. 費用構造分析（原価）】")
sales_data = [d['sales'] for d in historical_data]
cost_data = [d['cost_of_sales'] for d in historical_data]

cost_structure = analyze_cost_structure(sales_data, cost_data)

print(f"\n回帰式: {cost_structure['equation']}")
print(f"変動費率: {cost_structure['variable_cost_ratio']:.4f} ({cost_structure['interpretation']['variable_cost_ratio_percent']:.2f}%)")
print(f"固定費: {cost_structure['fixed_cost']:,.0f}円")
print(f"貢献利益率: {cost_structure['interpretation']['contribution_margin_ratio']:.2f}%")
print(f"決定係数（R²）: {cost_structure['r_squared']:.4f}")

if cost_structure['break_even_sales']:
    print(f"損益分岐点売上高: {cost_structure['break_even_sales']:,.0f}円")
else:
    print("損益分岐点売上高: 計算不可（変動費率が100%以上）")

# 2. 費用の予測
print("\n" + "=" * 80)
print("【2. 費用の予測（原価）】")
print("=" * 80)

cost_forecast = forecast_costs(historical_data, 'cost_of_sales', forecast_years=3)

print(f"\n費用構造:")
print(f"  変動費率: {cost_forecast['cost_structure']['variable_cost_ratio']:.4f}")
print(f"  固定費: {cost_forecast['cost_structure']['fixed_cost']:,.0f}円")

print(f"\n過去データの予測値:")
for pred in cost_forecast['historical_cost_predictions']:
    print(f"  {pred['year']}年目: 実績={pred['actual_cost']:,.0f}円, 予測={pred['predicted_cost']:,.0f}円, 誤差={pred['error']:,.0f}円")

print(f"\n将来の予測:")
for pred in cost_forecast['future_cost_predictions']:
    print(f"  {pred['year']}年目: 売上予測={pred['predicted_sales']:,.0f}円, 原価予測={pred['predicted_cost']:,.0f}円")

# 3. 販管費の予測
print("\n" + "=" * 80)
print("【3. 費用の予測（販管費）】")
print("=" * 80)

operating_expenses_forecast = forecast_costs(historical_data, 'operating_expenses', forecast_years=3)

print(f"\n費用構造:")
print(f"  変動費率: {operating_expenses_forecast['cost_structure']['variable_cost_ratio']:.4f}")
print(f"  固定費: {operating_expenses_forecast['cost_structure']['fixed_cost']:,.0f}円")

print(f"\n過去データの予測値:")
for pred in operating_expenses_forecast['historical_cost_predictions']:
    print(f"  {pred['year']}年目: 実績={pred['actual_cost']:,.0f}円, 予測={pred['predicted_cost']:,.0f}円, 誤差={pred['error']:,.0f}円")

print(f"\n将来の予測:")
for pred in operating_expenses_forecast['future_cost_predictions']:
    print(f"  {pred['year']}年目: 売上予測={pred['predicted_sales']:,.0f}円, 販管費予測={pred['predicted_cost']:,.0f}円")

print("\n" + "=" * 80)
print("テスト完了")
print("=" * 80)
