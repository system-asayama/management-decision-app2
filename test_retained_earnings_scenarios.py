#!/usr/bin/env python3
"""
内部留保シミュレーション シナリオ分析 テストスクリプト
"""
import sys
import os

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.retained_earnings_simulation import (
    simulate_retained_earnings,
    simulate_retained_earnings_scenarios
)


def test_single_scenario():
    """単一シナリオのテスト（既存機能）"""
    print("=" * 80)
    print("単一シナリオ テスト（既存機能）")
    print("=" * 80)
    
    result = simulate_retained_earnings(
        current_net_assets=1000000000,  # 10億円
        annual_net_income=100000000,    # 1億円
        dividend_payout_ratio=0.3,      # 配当性向30%
        years=3,                         # 3年間
        growth_rate=0.0                  # 成長率0%
    )
    
    print("\n【パラメータ】")
    print(f"現在の純資産: {1000000000:,}円")
    print(f"年間当期純利益: {100000000:,}円")
    print(f"配当性向: 30%")
    print(f"シミュレーション年数: 3年")
    print(f"利益成長率: 0%")
    
    print("\n【年次結果】")
    for year_result in result['simulation_results']:
        print(f"Year {year_result['year']}: "
              f"純利益={year_result['net_income']:,.0f}, "
              f"配当={year_result['dividend']:,.0f}, "
              f"内部留保={year_result['retained_earnings']:,.0f}, "
              f"純資産={year_result['net_assets']:,.0f}")
    
    print("\n【サマリー】")
    summary = result['summary']
    print(f"初期純資産: {summary['initial_net_assets']:,}円")
    print(f"最終純資産: {summary['final_net_assets']:,}円")
    print(f"累積内部留保: {summary['total_retained_earnings']:,}円")
    print(f"累積配当: {summary['total_dividend']:,}円")
    print(f"純資産増加額: {summary['net_assets_increase']:,}円")
    print(f"純資産増加率: {summary['net_assets_increase_rate']}%")
    
    print("\n" + "=" * 80)
    print("✅ 単一シナリオのテスト完了")
    print("=" * 80)


def test_multiple_scenarios():
    """複数シナリオのテスト（新機能）"""
    print("\n" + "=" * 80)
    print("複数シナリオ テスト（新機能）")
    print("=" * 80)
    
    result = simulate_retained_earnings_scenarios(
        current_net_assets=1000000000,  # 10億円
        annual_net_income=100000000,    # 1億円
        dividend_payout_ratios=[0.2, 0.3, 0.4],  # 配当性向20%, 30%, 40%
        years=3,                         # 3年間
        growth_rate=0.0                  # 成長率0%
    )
    
    print("\n【パラメータ】")
    params = result['parameters']
    print(f"現在の純資産: {params['current_net_assets']:,}円")
    print(f"年間当期純利益: {params['annual_net_income']:,}円")
    print(f"シミュレーション年数: {params['years']}年")
    print(f"利益成長率: {params['growth_rate']*100}%")
    
    print("\n【シナリオ比較】")
    for scenario in result['scenarios']:
        print(f"\n{scenario['scenario_name']} (配当性向: {scenario['dividend_payout_ratio']*100}%)")
        summary = scenario['summary']
        print(f"  最終純資産: {summary['final_net_assets']:,}円")
        print(f"  累積内部留保: {summary['total_retained_earnings']:,}円")
        print(f"  累積配当: {summary['total_dividend']:,}円")
        print(f"  純資産増加率: {summary['net_assets_increase_rate']}%")
    
    print("\n【検証】")
    # 配当性向が低いほど内部留保が多く、純資産が増える
    scenario1 = result['scenarios'][0]  # 配当性向20%
    scenario2 = result['scenarios'][1]  # 配当性向30%
    scenario3 = result['scenarios'][2]  # 配当性向40%
    
    assert scenario1['summary']['total_retained_earnings'] > scenario2['summary']['total_retained_earnings']
    assert scenario2['summary']['total_retained_earnings'] > scenario3['summary']['total_retained_earnings']
    
    assert scenario1['summary']['total_dividend'] < scenario2['summary']['total_dividend']
    assert scenario2['summary']['total_dividend'] < scenario3['summary']['total_dividend']
    
    print("✓ 配当性向が低いほど内部留保が多い")
    print("✓ 配当性向が高いほど配当が多い")
    
    print("\n" + "=" * 80)
    print("✅ 複数シナリオのテスト成功")
    print("=" * 80)


def test_api_documentation():
    """APIドキュメント表示"""
    print("\n" + "=" * 80)
    print("API ドキュメント")
    print("=" * 80)
    
    print("\n【既存API（変更なし）】")
    print("GET /decision/retained-earnings-simulation/simulate")
    print("パラメータ:")
    print("  - company_id: 企業ID")
    print("  - fiscal_year_id: 会計年度ID")
    print("  - years: シミュレーション年数（デフォルト: 10）")
    print("  - dividend_payout_ratio: 配当性向（デフォルト: 0.3）")
    print("  - growth_rate: 利益成長率（デフォルト: 0.0）")
    
    print("\n【新規API】")
    print("GET /decision/retained-earnings-simulation/scenarios")
    print("パラメータ:")
    print("  - company_id: 企業ID")
    print("  - fiscal_year_id: 会計年度ID")
    print("  - payout_ratios: 配当性向のリスト（カンマ区切り、例: 0.2,0.3,0.4）")
    print("  - years: シミュレーション年数（デフォルト: 10）")
    print("  - growth_rate: 利益成長率（デフォルト: 0.0）")
    
    print("\n【レスポンス例】")
    print("""
{
  "scenarios": [
    {
      "scenario_id": 1,
      "scenario_name": "シナリオ1",
      "dividend_payout_ratio": 0.2,
      "simulation_results": [
        {
          "year": 1,
          "net_income": 100000000.0,
          "dividend": 20000000.0,
          "retained_earnings": 80000000.0,
          "net_assets": 1080000000.0,
          "net_assets_growth_rate": 8.0
        },
        ...
      ],
      "summary": {
        "initial_net_assets": 1000000000.0,
        "final_net_assets": 1240000000.0,
        "total_retained_earnings": 240000000.0,
        "total_dividend": 60000000.0,
        "net_assets_increase": 240000000.0,
        "net_assets_increase_rate": 24.0
      }
    },
    {
      "scenario_id": 2,
      "scenario_name": "シナリオ2",
      "dividend_payout_ratio": 0.3,
      ...
    },
    {
      "scenario_id": 3,
      "scenario_name": "シナリオ3",
      "dividend_payout_ratio": 0.4,
      ...
    }
  ],
  "parameters": {
    "current_net_assets": 1000000000.0,
    "annual_net_income": 100000000.0,
    "years": 3,
    "growth_rate": 0.0
  }
}
    """)
    
    print("\n【使用例】")
    print("curl 'http://localhost:5000/decision/retained-earnings-simulation/scenarios?company_id=1&fiscal_year_id=1&payout_ratios=0.2,0.3,0.4&years=3'")
    
    print("\n【注意事項】")
    print("- 既存のsimulate_retained_earnings関数は変更していません")
    print("- 計算式は既存と同じです")
    print("- 年数の変更はありません")
    
    print("\n" + "=" * 80)
    print("✅ APIドキュメント表示完了")
    print("=" * 80)


if __name__ == "__main__":
    test_single_scenario()
    test_multiple_scenarios()
    test_api_documentation()
    
    print("\n" + "=" * 80)
    print("✅ すべてのテストが成功しました！")
    print("=" * 80)
