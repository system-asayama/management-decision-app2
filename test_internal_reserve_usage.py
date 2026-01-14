"""
内部留保使途シミュレーションのテスト
"""
from app.utils.retained_earnings_simulation import (
    simulate_internal_reserve_usage,
    simulate_internal_reserve_scenarios
)

# テストデータ
current_net_assets = 1000000000  # 10億円
current_total_assets = 2000000000  # 20億円
current_liabilities = 1000000000  # 10億円
annual_net_income = 100000000  # 1億円
dividend_payout_ratio = 0.3  # 配当性向30%
years = 3  # 3年間
growth_rate = 0.0  # 成長率0%

print("=" * 80)
print("内部留保使途シミュレーションテスト")
print("=" * 80)

# 1. 単一シナリオ（再投資50%、返済50%）
print("\n【1. 単一シナリオ（再投資50%、返済50%）】")
result = simulate_internal_reserve_usage(
    current_net_assets=current_net_assets,
    current_total_assets=current_total_assets,
    current_liabilities=current_liabilities,
    annual_net_income=annual_net_income,
    dividend_payout_ratio=dividend_payout_ratio,
    reinvestment_ratio=0.5,
    years=years,
    growth_rate=growth_rate
)

print(f"\n初期状態:")
print(f"  純資産: {result['summary']['initial_net_assets']:,.0f}円")
print(f"  総資産: {result['summary']['initial_total_assets']:,.0f}円")
print(f"  負債: {result['summary']['initial_liabilities']:,.0f}円")

print(f"\n最終状態:")
print(f"  純資産: {result['summary']['final_net_assets']:,.0f}円")
print(f"  総資産: {result['summary']['final_total_assets']:,.0f}円")
print(f"  負債: {result['summary']['final_liabilities']:,.0f}円")

print(f"\n累積値:")
print(f"  内部留保総額: {result['summary']['total_retained_earnings']:,.0f}円")
print(f"  再投資総額: {result['summary']['total_reinvestment']:,.0f}円")
print(f"  返済総額: {result['summary']['total_debt_repayment']:,.0f}円")
print(f"  配当総額: {result['summary']['total_dividend']:,.0f}円")

print(f"\n増減:")
print(f"  純資産増加: {result['summary']['net_assets_increase']:,.0f}円 ({result['summary']['net_assets_increase_rate']:.2f}%)")
print(f"  負債減少: {result['summary']['liabilities_decrease']:,.0f}円 ({result['summary']['liabilities_decrease_rate']:.2f}%)")

print(f"\n年次推移:")
for year_data in result['simulation_results']:
    print(f"  {year_data['year']}年目: 純資産={year_data['net_assets']:,.0f}円, 負債={year_data['liabilities']:,.0f}円, 自己資本比率={year_data['equity_ratio']:.2f}%")

# 2. 複数シナリオ比較
print("\n" + "=" * 80)
print("【2. 複数シナリオ比較】")
print("=" * 80)

reinvestment_ratios = [0.3, 0.5, 0.7]  # 返済重視、バランス、再投資重視
scenarios_result = simulate_internal_reserve_scenarios(
    current_net_assets=current_net_assets,
    current_total_assets=current_total_assets,
    current_liabilities=current_liabilities,
    annual_net_income=annual_net_income,
    dividend_payout_ratio=dividend_payout_ratio,
    reinvestment_ratios=reinvestment_ratios,
    years=years,
    growth_rate=growth_rate
)

for scenario in scenarios_result['scenarios']:
    print(f"\n{scenario['scenario_name']}（再投資{scenario['reinvestment_ratio']*100:.0f}%、返済{scenario['debt_repayment_ratio']*100:.0f}%）:")
    print(f"  最終純資産: {scenario['summary']['final_net_assets']:,.0f}円")
    print(f"  最終総資産: {scenario['summary']['final_total_assets']:,.0f}円")
    print(f"  最終負債: {scenario['summary']['final_liabilities']:,.0f}円")
    print(f"  再投資総額: {scenario['summary']['total_reinvestment']:,.0f}円")
    print(f"  返済総額: {scenario['summary']['total_debt_repayment']:,.0f}円")
    print(f"  負債減少率: {scenario['summary']['liabilities_decrease_rate']:.2f}%")

print("\n" + "=" * 80)
print("テスト完了")
print("=" * 80)
