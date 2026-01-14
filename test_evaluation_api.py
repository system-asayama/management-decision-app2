#!/usr/bin/env python3
"""
評価API テストスクリプト
"""
import sys
import os

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.evaluation_helpers import evaluate_yoy, evaluate_multiple_indicators


def test_evaluate_yoy():
    """evaluate_yoy関数のテスト"""
    print("=" * 80)
    print("evaluate_yoy関数 テスト")
    print("=" * 80)
    
    test_cases = [
        # (当年, 前年, 期待される評価記号)
        (1100, 1000, '◎', '+10%以上'),
        (1200, 1000, '◎', '+20%'),
        (1050, 1000, '◯', '0〜+10%'),
        (1000, 1000, '◯', '0%'),
        (950, 1000, '△', '0〜-10%'),
        (900, 1000, '△', '-10%'),
        (850, 1000, '×', '-10%未満'),
        (800, 1000, '×', '-20%'),
        (100, 0, '◎', '前年0から増加'),
        (0, 0, '◯', '前年0で変化なし'),
        (-100, 0, '×', '前年0から減少'),
    ]
    
    print("\n【テストケース】")
    for this_year, prev_year, expected_grade, description in test_cases:
        result = evaluate_yoy(this_year, prev_year)
        status = '✓' if result['grade'] == expected_grade else '✗'
        print(f"{status} 当年: {this_year:>6}, 前年: {prev_year:>6} => "
              f"比率: {result['ratio']:>7.2f}%, 評価: {result['grade']} ({description})")
        
        if result['grade'] != expected_grade:
            print(f"  ❌ 期待: {expected_grade}, 実際: {result['grade']}")
    
    print("\n" + "=" * 80)
    print("✅ evaluate_yoy関数のテスト完了")
    print("=" * 80)


def test_evaluate_multiple_indicators():
    """evaluate_multiple_indicators関数のテスト"""
    print("\n" + "=" * 80)
    print("evaluate_multiple_indicators関数 テスト")
    print("=" * 80)
    
    indicators_this_year = {
        'sales': 1100000000,
        'operatingIncome': 220000000,
        'netIncome': 143500000,
        'totalAssets': 1300000000
    }
    
    indicators_prev_year = {
        'sales': 1000000000,
        'operatingIncome': 200000000,
        'netIncome': 130000000,
        'totalAssets': 1200000000
    }
    
    results = evaluate_multiple_indicators(indicators_this_year, indicators_prev_year)
    
    print("\n【評価結果】")
    for indicator_name, evaluation in results.items():
        print(f"\n指標: {indicator_name}")
        print(f"  当年: {evaluation['thisYear']:>15,.0f}")
        print(f"  前年: {evaluation['prevYear']:>15,.0f}")
        print(f"  比率: {evaluation['ratio']:>7.2f}%")
        print(f"  評価: {evaluation['grade']}")
    
    print("\n" + "=" * 80)
    print("✅ evaluate_multiple_indicators関数のテスト完了")
    print("=" * 80)


def test_api_simulation():
    """APIレスポンスのシミュレーション"""
    print("\n" + "=" * 80)
    print("APIレスポンス シミュレーション")
    print("=" * 80)
    
    print("\n【APIエンドポイント】")
    print("GET /decision/evaluation/get?company_id=1&fiscal_year_id=2")
    
    print("\n【期待されるレスポンス構造】")
    print("""
{
  "success": true,
  "data": {
    "fiscalYear": {
      "id": 2,
      "label": "2025年度"
    },
    "prevFiscalYear": {
      "id": 1,
      "label": "2024年度"
    },
    "pl": {
      "sales": {
        "thisYear": 1100000000,
        "prevYear": 1000000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "operatingIncome": {
        "thisYear": 220000000,
        "prevYear": 200000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "netIncome": {
        "thisYear": 157500000,
        "prevYear": 143500000,
        "ratio": 9.76,
        "grade": "◯"
      }
    },
    "bs": {
      "totalAssets": {
        "thisYear": 1430000000,
        "prevYear": 1300000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "totalEquity": {
        "thisYear": 660000000,
        "prevYear": 600000000,
        "ratio": 10.00,
        "grade": "◎"
      }
    }
  }
}
    """)
    
    print("\n【評価基準】")
    print("  ◎: +10%以上")
    print("  ◯: 0〜+10%")
    print("  △: 0〜-10%")
    print("  ×: -10%未満")
    
    print("\n" + "=" * 80)
    print("✅ APIシミュレーション完了")
    print("=" * 80)


if __name__ == "__main__":
    test_evaluate_yoy()
    test_evaluate_multiple_indicators()
    test_api_simulation()
    
    print("\n" + "=" * 80)
    print("✅ すべてのテストが完了しました！")
    print("=" * 80)
