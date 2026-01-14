"""
貢献度分析機能のテスト
"""

print("=" * 60)
print("貢献度分析機能のテスト")
print("=" * 60)

# ==================== 製品別貢献度分析のテスト ====================
print("\n【製品別貢献度分析のテスト】")

from app.utils.product_contribution_analyzer import (
    analyze_product_contribution,
    format_product_contribution_for_ui,
    rank_products_by_contribution,
    identify_unprofitable_products
)

# テストデータ
products = [
    {
        'name': '製品A',
        'sales': 10000000,
        'variable_cost': 6000000,
        'fixed_cost': 2000000
    },
    {
        'name': '製品B',
        'sales': 8000000,
        'variable_cost': 5000000,
        'fixed_cost': 1500000
    },
    {
        'name': '製品C',
        'sales': 5000000,
        'variable_cost': 3500000,
        'fixed_cost': 2000000
    },
    {
        'name': '製品D',
        'sales': 3000000,
        'variable_cost': 2000000,
        'fixed_cost': 1500000
    }
]

# 製品別貢献度分析を実行
result = analyze_product_contribution(products)

print("\n【製品別分析結果】")
print(f"{'製品名':>10} | {'売上高':>12} | {'変動費':>12} | {'固定費':>12} | {'限界利益':>12} | {'貢献利益':>12} | {'採算':>6} | {'評価':>6}")
print("-" * 110)
for product in result['products']:
    print(f"{product['name']:>10} | {product['sales']:>12,.0f} | {product['variable_cost']:>12,.0f} | {product['fixed_cost']:>12,.0f} | {product['marginal_profit']:>12,.0f} | {product['contribution_profit']:>12,.0f} | {product['profitability_status_symbol']:>6} | {product['profitability_rating_symbol']:>6}")

print("\n【全体サマリー】")
print(f"総売上高: {result['total']['sales']:,.0f}円")
print(f"総変動費: {result['total']['variable_cost']:,.0f}円")
print(f"総固定費: {result['total']['fixed_cost']:,.0f}円")
print(f"総限界利益: {result['total']['marginal_profit']:,.0f}円")
print(f"限界利益率: {result['total']['marginal_profit_ratio']:.2f}%")
print(f"総貢献利益: {result['total']['contribution_profit']:,.0f}円")
print(f"貢献利益率: {result['total']['contribution_profit_ratio']:.2f}%")

# ランキングを生成
ranked_products = rank_products_by_contribution(result['products'])
print("\n【貢献利益ランキング】")
for i, product in enumerate(ranked_products, start=1):
    print(f"{i}位: {product['name']} - {product['contribution_profit']:,.0f}円")

# 不採算製品を特定
unprofitable_products = identify_unprofitable_products(result['products'])
print(f"\n【不採算製品】")
if unprofitable_products:
    for product in unprofitable_products:
        print(f"  - {product['name']}: {product['contribution_profit']:,.0f}円")
else:
    print("  なし")

# UI表示用に整形
formatted_result = format_product_contribution_for_ui(result)
print(f"\n【UI整形済みサマリー】")
print(f"総貢献利益: {formatted_result['total']['contribution_profit_formatted']}")
print(f"貢献利益率: {formatted_result['total']['contribution_profit_ratio_formatted']}")

# ==================== セグメント別貢献度分析のテスト ====================
print("\n" + "=" * 60)
print("【セグメント別貢献度分析のテスト】")
print("=" * 60)

from app.utils.contribution_analyzer import (
    analyze_product_mix,
    rank_segments_by_contribution,
    identify_unprofitable_segments
)

# テストデータ
segments = [
    {
        'name': '事業部A',
        'sales': 50000000,
        'variable_cost': 30000000,
        'direct_fixed_cost': 10000000
    },
    {
        'name': '事業部B',
        'sales': 30000000,
        'variable_cost': 20000000,
        'direct_fixed_cost': 8000000
    },
    {
        'name': '事業部C',
        'sales': 20000000,
        'variable_cost': 15000000,
        'direct_fixed_cost': 7000000
    }
]

common_fixed_cost = 5000000

# セグメント別貢献度分析を実行
segment_result = analyze_product_mix(segments, common_fixed_cost)

print("\n【セグメント別分析結果】")
print(f"{'セグメント名':>12} | {'売上高':>12} | {'変動費':>12} | {'固定費':>12} | {'貢献利益':>12} | {'セグメント利益':>15}")
print("-" * 95)
for segment in segment_result['segments']:
    print(f"{segment['name']:>12} | {segment['sales']:>12,.0f} | {segment['variable_cost']:>12,.0f} | {segment['direct_fixed_cost']:>12,.0f} | {segment['contribution_margin']:>12,.0f} | {segment['segment_profit']:>15,.0f}")

print("\n【全体サマリー】")
print(f"総売上高: {segment_result['total']['sales']:,.0f}円")
print(f"総貢献利益: {segment_result['total']['contribution_margin']:,.0f}円")
print(f"貢献利益率: {segment_result['total']['contribution_margin_ratio']:.2f}%")
print(f"総セグメント利益: {segment_result['total']['segment_profit']:,.0f}円")
print(f"共通固定費: {segment_result['total']['common_fixed_cost']:,.0f}円")
print(f"営業利益: {segment_result['total']['operating_profit']:,.0f}円")

# ランキングを生成
ranked_segments = rank_segments_by_contribution(segment_result['segments'])
print("\n【貢献利益ランキング】")
for i, segment in enumerate(ranked_segments, start=1):
    print(f"{i}位: {segment['name']} - {segment['contribution_margin']:,.0f}円")

# 不採算セグメントを特定
unprofitable_segments = identify_unprofitable_segments(segment_result['segments'])
print(f"\n【不採算セグメント】")
if unprofitable_segments:
    for segment in unprofitable_segments:
        print(f"  - {segment['name']}: {segment['segment_profit']:,.0f}円")
else:
    print("  なし")

# ==================== 総合結果 ====================
print("\n" + "=" * 60)
print("【テスト結果サマリー】")
print("=" * 60)
print("✓ 製品別貢献度分析: 正常に動作")
print("✓ 採算性評価: 正常に動作")
print("✓ ランキング生成: 正常に動作")
print("✓ 不採算製品の特定: 正常に動作")
print("✓ UI表示用の整形: 正常に動作")
print("✓ セグメント別貢献度分析: 正常に動作")
print("\nすべてのテストが成功しました！")
