#!/usr/bin/env python3
"""
データ検証機能のテストスクリプト
"""
import sys
import os

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.data_validation import (
    validate_working_capital_assumption,
    validate_debt_repayment_assumption,
    validate_all_assumptions
)


def test_working_capital_validation():
    """運転資金前提の検証テスト"""
    print("=" * 80)
    print("運転資金前提 検証テスト")
    print("=" * 80)
    
    # 正常なデータ
    print("\n【テスト1: 正常なデータ】")
    data = {
        'cash_turnover_period': 0.033,
        'receivables_turnover_period': 2.4,
        'inventory_turnover_period': 0.73,
        'payables_turnover_period': 1.33,
        'cash_increase': 687.35,
        'receivables_increase': 43247.65,
        'inventory_increase': 13582.57,
        'payables_increase': -33508.62
    }
    
    result = validate_working_capital_assumption(data)
    print(f"検証結果: {'✅ 成功' if result['valid'] else '❌ 失敗'}")
    if result['errors']:
        print(f"エラー: {result['errors']}")
    if result['warnings']:
        print(f"警告: {result['warnings']}")
    
    # 負の値
    print("\n【テスト2: 負の回転期間】")
    data = {
        'cash_turnover_period': -0.1,
        'receivables_turnover_period': 2.4,
        'inventory_turnover_period': 0.73,
        'payables_turnover_period': 1.33,
        'cash_increase': 0,
        'receivables_increase': 0,
        'inventory_increase': 0,
        'payables_increase': 0
    }
    
    result = validate_working_capital_assumption(data)
    print(f"検証結果: {'✅ 成功' if result['valid'] else '❌ 失敗'}")
    if result['errors']:
        print(f"エラー: {result['errors']}")
    if result['warnings']:
        print(f"警告: {result['warnings']}")
    
    # 異常に大きい値
    print("\n【テスト3: 異常に大きい回転期間】")
    data = {
        'cash_turnover_period': 15,
        'receivables_turnover_period': 2.4,
        'inventory_turnover_period': 0.73,
        'payables_turnover_period': 1.33,
        'cash_increase': 0,
        'receivables_increase': 0,
        'inventory_increase': 0,
        'payables_increase': 0
    }
    
    result = validate_working_capital_assumption(data)
    print(f"検証結果: {'✅ 成功' if result['valid'] else '❌ 失敗'}")
    if result['errors']:
        print(f"エラー: {result['errors']}")
    if result['warnings']:
        print(f"警告: {result['warnings']}")
    
    # 債務債権回転期間差異が負
    print("\n【テスト4: 債務債権回転期間差異が負】")
    data = {
        'cash_turnover_period': 0.033,
        'receivables_turnover_period': 3.0,  # 売掛債権回転期間が長い
        'inventory_turnover_period': 0.73,
        'payables_turnover_period': 1.0,  # 買掛債務回転期間が短い
        'cash_increase': 0,
        'receivables_increase': 0,
        'inventory_increase': 0,
        'payables_increase': 0
    }
    
    result = validate_working_capital_assumption(data)
    print(f"検証結果: {'✅ 成功' if result['valid'] else '❌ 失敗'}")
    if result['errors']:
        print(f"エラー: {result['errors']}")
    if result['warnings']:
        print(f"警告: {result['warnings']}")
    
    print("\n" + "=" * 80)
    print("✅ 運転資金前提の検証テスト完了")
    print("=" * 80)


def test_debt_repayment_validation():
    """返済スケジュール前提の検証テスト"""
    print("\n" + "=" * 80)
    print("返済スケジュール前提 検証テスト")
    print("=" * 80)
    
    # 正常なデータ
    print("\n【テスト1: 正常なデータ】")
    data = {
        'beginning_balance': 50000000,
        'borrowing_amount': 10000000,
        'principal_repayment': 5000000,
        'ending_balance': 55000000,
        'interest_payment': 1000000,
        'average_interest_rate': 0.02
    }
    
    result = validate_debt_repayment_assumption(data)
    print(f"検証結果: {'✅ 成功' if result['valid'] else '❌ 失敗'}")
    if result['errors']:
        print(f"エラー: {result['errors']}")
    if result['warnings']:
        print(f"警告: {result['warnings']}")
    
    # 負の値
    print("\n【テスト2: 負の借入金残高】")
    data = {
        'beginning_balance': -1000000,
        'borrowing_amount': 10000000,
        'principal_repayment': 5000000,
        'ending_balance': 4000000,
        'interest_payment': 100000,
        'average_interest_rate': 0.02
    }
    
    result = validate_debt_repayment_assumption(data)
    print(f"検証結果: {'✅ 成功' if result['valid'] else '❌ 失敗'}")
    if result['errors']:
        print(f"エラー: {result['errors']}")
    if result['warnings']:
        print(f"警告: {result['warnings']}")
    
    # 整合性エラー
    print("\n【テスト3: 借入金の整合性エラー】")
    data = {
        'beginning_balance': 50000000,
        'borrowing_amount': 10000000,
        'principal_repayment': 5000000,
        'ending_balance': 60000000,  # 正しくは55000000
        'interest_payment': 1000000,
        'average_interest_rate': 0.02
    }
    
    result = validate_debt_repayment_assumption(data)
    print(f"検証結果: {'✅ 成功' if result['valid'] else '❌ 失敗'}")
    if result['errors']:
        print(f"エラー: {result['errors']}")
    if result['warnings']:
        print(f"警告: {result['warnings']}")
    
    # 異常に高い金利
    print("\n【テスト4: 異常に高い金利】")
    data = {
        'beginning_balance': 50000000,
        'borrowing_amount': 10000000,
        'principal_repayment': 5000000,
        'ending_balance': 55000000,
        'interest_payment': 15000000,
        'average_interest_rate': 0.25  # 25%
    }
    
    result = validate_debt_repayment_assumption(data)
    print(f"検証結果: {'✅ 成功' if result['valid'] else '❌ 失敗'}")
    if result['errors']:
        print(f"エラー: {result['errors']}")
    if result['warnings']:
        print(f"警告: {result['warnings']}")
    
    # 支払利息と平均金利の不整合
    print("\n【テスト5: 支払利息と平均金利の不整合】")
    data = {
        'beginning_balance': 50000000,
        'borrowing_amount': 10000000,
        'principal_repayment': 5000000,
        'ending_balance': 55000000,
        'interest_payment': 5000000,  # 計算上は約1050000
        'average_interest_rate': 0.02
    }
    
    result = validate_debt_repayment_assumption(data)
    print(f"検証結果: {'✅ 成功' if result['valid'] else '❌ 失敗'}")
    if result['errors']:
        print(f"エラー: {result['errors']}")
    if result['warnings']:
        print(f"警告: {result['warnings']}")
    
    print("\n" + "=" * 80)
    print("✅ 返済スケジュール前提の検証テスト完了")
    print("=" * 80)


def test_all_validation():
    """一括検証テスト"""
    print("\n" + "=" * 80)
    print("一括検証テスト")
    print("=" * 80)
    
    working_capital_data = [
        {
            'cash_turnover_period': 0.033,
            'receivables_turnover_period': 2.4,
            'inventory_turnover_period': 0.73,
            'payables_turnover_period': 1.33,
            'cash_increase': 687.35,
            'receivables_increase': 43247.65,
            'inventory_increase': 13582.57,
            'payables_increase': -33508.62
        },
        {
            'cash_turnover_period': 0.033,
            'receivables_turnover_period': 2.2,
            'inventory_turnover_period': 0.72,
            'payables_turnover_period': 1.32,
            'cash_increase': 0,
            'receivables_increase': -18607.55,
            'inventory_increase': -930.38,
            'payables_increase': -272.63
        },
        {
            'cash_turnover_period': 0.033,
            'receivables_turnover_period': 2.0,
            'inventory_turnover_period': 0.7,
            'payables_turnover_period': 1.31,
            'cash_increase': 0,
            'receivables_increase': -18607.55,
            'inventory_increase': -1860.76,
            'payables_increase': 0
        }
    ]
    
    debt_repayment_data = [
        {
            'beginning_balance': 0,
            'borrowing_amount': 36420,
            'principal_repayment': 0,
            'ending_balance': 36420,
            'interest_payment': 866,
            'average_interest_rate': 0.0476
        },
        {
            'beginning_balance': 0,
            'borrowing_amount': 0,
            'principal_repayment': 0,
            'ending_balance': 0,
            'interest_payment': 0,
            'average_interest_rate': 0
        },
        {
            'beginning_balance': 0,
            'borrowing_amount': 0,
            'principal_repayment': 0,
            'ending_balance': 0,
            'interest_payment': 0,
            'average_interest_rate': 0
        }
    ]
    
    result = validate_all_assumptions(working_capital_data, debt_repayment_data)
    
    print(f"\n検証結果: {'✅ 成功' if result['valid'] else '❌ 失敗'}")
    print(f"エラー数: {len(result['errors'])}")
    print(f"警告数: {len(result['warnings'])}")
    
    if result['errors']:
        print("\nエラー:")
        for error in result['errors']:
            print(f"  - {error}")
    
    if result['warnings']:
        print("\n警告:")
        for warning in result['warnings']:
            print(f"  - {warning}")
    
    print("\n" + "=" * 80)
    print("✅ 一括検証テスト完了")
    print("=" * 80)


if __name__ == "__main__":
    test_working_capital_validation()
    test_debt_repayment_validation()
    test_all_validation()
    
    print("\n" + "=" * 80)
    print("✅ すべてのテストが完了しました！")
    print("=" * 80)
