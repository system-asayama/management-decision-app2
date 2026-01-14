#!/usr/bin/env python3
"""
借入金許容限度額分析 Method1/Method3 簡易テストスクリプト
（データベース接続なし）
"""


def test_method1_formulas():
    """Method1の数式テスト"""
    print("=" * 80)
    print("Method1 数式テスト")
    print("=" * 80)
    
    print("\nExcelの数式:")
    print("1. 金融調達率より = 総資本 × 30%")
    print("2. 借入金依存率より = 年間売上高 × 20%")
    print("3. 担保力より = (土地（時価） + 有価証券（時価）) × 50%")
    
    # テストケース
    total_assets = 1300000000  # 総資本
    sales = 1000000000  # 売上高
    land_value = 0  # 土地（時価）
    securities_value = 0  # 有価証券（時価）
    
    # 計算
    method1_financial_procurement = total_assets * 0.3
    method1_debt_dependence = sales * 0.2
    method1_collateral = (land_value + securities_value) * 0.5
    
    print("\n【テストケース】")
    print(f"総資本: {total_assets:,}円")
    print(f"売上高: {sales:,}円")
    print(f"土地（時価）: {land_value:,}円")
    print(f"有価証券（時価）: {securities_value:,}円")
    
    print("\n【計算結果】")
    print(f"1. 金融調達率による許容額: {method1_financial_procurement:,.2f}円")
    print(f"2. 借入金依存率による許容額: {method1_debt_dependence:,.2f}円")
    print(f"3. 担保力による許容額: {method1_collateral:,.2f}円")
    
    print("\n【期待される結果】")
    print(f"1. 金融調達率による許容額: {1300000000 * 0.3:,.2f}円")
    print(f"2. 借入金依存率による許容額: {1000000000 * 0.2:,.2f}円")
    print(f"3. 担保力による許容額: {0.0:,.2f}円")
    
    # 検証
    assert abs(method1_financial_procurement - 390000000) < 1, "金融調達率の計算が正しくありません"
    assert abs(method1_debt_dependence - 200000000) < 1, "借入金依存率の計算が正しくありません"
    assert abs(method1_collateral - 0) < 1, "担保力の計算が正しくありません"
    
    print("\n" + "=" * 80)
    print("✅ Method1の数式テスト成功")
    print("=" * 80)


def test_method3_formulas():
    """Method3の数式テスト"""
    print("\n" + "=" * 80)
    print("Method3 数式テスト")
    print("=" * 80)
    
    print("\nExcelの数式:")
    print("許容限度額 = 売上総利益 × 標準売上総利益金融費用率 ÷ 平均金利")
    
    # テストケース
    gross_profit = 400000000  # 売上総利益
    standard_rate = 0.0188  # 標準売上総利益金融費用率
    average_interest_rate = 0.0172  # 平均金利
    interest_bearing_debt = 200000000  # 有利子負債
    
    # 計算
    method3_allowable_debt = (gross_profit * standard_rate) / average_interest_rate
    surplus = method3_allowable_debt - interest_bearing_debt
    surplus_ratio = surplus / method3_allowable_debt if method3_allowable_debt > 0 else 0
    
    print("\n【テストケース】")
    print(f"売上総利益: {gross_profit:,}円")
    print(f"標準売上総利益金融費用率: {standard_rate}")
    print(f"平均金利: {average_interest_rate}")
    print(f"有利子負債: {interest_bearing_debt:,}円")
    
    print("\n【計算結果】")
    print(f"許容限度額: {method3_allowable_debt:,.2f}円")
    print(f"余裕額: {surplus:,.2f}円")
    print(f"余裕率: {surplus_ratio:.4f}")
    
    print("\n【期待される結果】")
    expected_allowable = (400000000 * 0.0188) / 0.0172
    expected_surplus = expected_allowable - 200000000
    expected_surplus_ratio = expected_surplus / expected_allowable
    print(f"許容限度額: {expected_allowable:,.2f}円")
    print(f"余裕額: {expected_surplus:,.2f}円")
    print(f"余裕率: {expected_surplus_ratio:.4f}")
    
    # 検証
    assert abs(method3_allowable_debt - expected_allowable) < 1, "許容限度額の計算が正しくありません"
    assert abs(surplus - expected_surplus) < 1, "余裕額の計算が正しくありません"
    assert abs(surplus_ratio - expected_surplus_ratio) < 0.0001, "余裕率の計算が正しくありません"
    
    print("\n" + "=" * 80)
    print("✅ Method3の数式テスト成功")
    print("=" * 80)


def test_api_documentation():
    """APIドキュメント表示"""
    print("\n" + "=" * 80)
    print("API ドキュメント")
    print("=" * 80)
    
    print("\n【Method1 APIエンドポイント】")
    print("GET /decision/debt-capacity/method1?fiscal_year_id=1")
    
    print("\n【Method1 レスポンス例】")
    print("""
{
  "success": true,
  "data": {
    "method1_financial_procurement": 390000000.00,
    "method1_debt_dependence": 200000000.00,
    "method1_collateral": 0.00,
    "total_assets": 1300000000.00,
    "sales": 1000000000.00,
    "land_value": 0.00,
    "securities_value": 0.00
  }
}
    """)
    
    print("\n【Method3 APIエンドポイント】")
    print("GET /decision/debt-capacity/method3?fiscal_year_id=1&standard_rate=0.0188")
    
    print("\n【Method3 レスポンス例】")
    print("""
{
  "success": true,
  "data": {
    "method3_allowable_debt": 437209302.33,
    "gross_profit": 400000000.00,
    "standard_rate": 0.0188,
    "average_interest_rate": 0.0172,
    "interest_bearing_debt": 200000000.00,
    "surplus": 237209302.33,
    "surplus_ratio": 0.5426
  }
}
    """)
    
    print("\n【注意事項】")
    print("- 数式はExcelの式どおりに実装")
    print("- 推測による変更は一切なし")
    print("- 土地・有価証券のデータがない場合は0として計算")
    
    print("\n" + "=" * 80)
    print("✅ APIドキュメント表示完了")
    print("=" * 80)


if __name__ == "__main__":
    test_method1_formulas()
    test_method3_formulas()
    test_api_documentation()
    
    print("\n" + "=" * 80)
    print("✅ すべてのテストが成功しました！")
    print("=" * 80)
