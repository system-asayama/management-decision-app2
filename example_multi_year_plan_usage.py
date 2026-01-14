#!/usr/bin/env python3
"""
複数年度計画API 使用例
実際のアプリケーションでの使用方法を示すサンプルコード
"""

import requests
import json

# ベースURL（実際の環境に合わせて変更してください）
BASE_URL = "http://localhost:5000"

# セッション（認証済みと仮定）
session = requests.Session()


def example_create_multi_year_plan():
    """複数年度計画の作成例"""
    
    url = f"{BASE_URL}/decision/multi-year-plan/create-or-update"
    
    # 3期分の計画データ
    data = {
        "company_id": 1,
        "base_fiscal_year_id": 1,
        "years": {
            "year1": {
                "laborPlan": {
                    "totalEmployees": 50,
                    "averageSalary": 5000000,
                    "totalLaborCost": 250000000,
                    "breakdown": {
                        "management": 10,
                        "sales": 15,
                        "production": 20,
                        "support": 5
                    }
                },
                "capexPlan": {
                    "equipment": 50000000,
                    "facilities": 30000000,
                    "software": 10000000,
                    "vehicles": 5000000,
                    "total": 95000000,
                    "description": "生産設備の更新と新工場建設"
                },
                "workingCapitalPlan": {
                    "accountsReceivable": 100000000,
                    "inventory": 80000000,
                    "accountsPayable": 60000000,
                    "netWorkingCapital": 120000000,
                    "cashConversionCycle": 45
                },
                "financingPlan": {
                    "newLoans": 100000000,
                    "interestRate": 0.02,
                    "loanTerm": 10,
                    "lender": "○○銀行",
                    "purpose": "設備投資資金"
                },
                "repaymentPlan": {
                    "principalRepayment": 20000000,
                    "interestPayment": 2000000,
                    "totalPayment": 22000000,
                    "remainingBalance": 80000000
                }
            },
            "year2": {
                "laborPlan": {
                    "totalEmployees": 55,
                    "averageSalary": 5100000,
                    "totalLaborCost": 280500000,
                    "breakdown": {
                        "management": 11,
                        "sales": 17,
                        "production": 22,
                        "support": 5
                    }
                },
                "capexPlan": {
                    "equipment": 60000000,
                    "facilities": 40000000,
                    "software": 15000000,
                    "vehicles": 5000000,
                    "total": 120000000,
                    "description": "新工場稼働に伴う追加設備投資"
                },
                "workingCapitalPlan": {
                    "accountsReceivable": 110000000,
                    "inventory": 90000000,
                    "accountsPayable": 70000000,
                    "netWorkingCapital": 130000000,
                    "cashConversionCycle": 43
                },
                "financingPlan": {
                    "newLoans": 50000000,
                    "interestRate": 0.02,
                    "loanTerm": 5,
                    "lender": "△△銀行",
                    "purpose": "運転資金"
                },
                "repaymentPlan": {
                    "principalRepayment": 25000000,
                    "interestPayment": 2500000,
                    "totalPayment": 27500000,
                    "remainingBalance": 105000000
                }
            },
            "year3": {
                "laborPlan": {
                    "totalEmployees": 60,
                    "averageSalary": 5200000,
                    "totalLaborCost": 312000000,
                    "breakdown": {
                        "management": 12,
                        "sales": 18,
                        "production": 25,
                        "support": 5
                    }
                },
                "capexPlan": {
                    "equipment": 70000000,
                    "facilities": 50000000,
                    "software": 20000000,
                    "vehicles": 10000000,
                    "total": 150000000,
                    "description": "生産能力拡大とDX推進"
                },
                "workingCapitalPlan": {
                    "accountsReceivable": 120000000,
                    "inventory": 100000000,
                    "accountsPayable": 80000000,
                    "netWorkingCapital": 140000000,
                    "cashConversionCycle": 40
                },
                "financingPlan": {
                    "newLoans": 0,
                    "interestRate": 0.02,
                    "loanTerm": 0,
                    "lender": "",
                    "purpose": "新規借入なし"
                },
                "repaymentPlan": {
                    "principalRepayment": 30000000,
                    "interestPayment": 3000000,
                    "totalPayment": 33000000,
                    "remainingBalance": 75000000
                }
            }
        },
        "notes": "中期経営計画（2024-2026年度）\n新工場建設と生産能力拡大を柱とした成長戦略"
    }
    
    try:
        response = session.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        print("=" * 80)
        print("複数年度計画の作成/更新 成功")
        print("=" * 80)
        print(f"計画ID: {result['data']['id']}")
        print(f"企業ID: {result['data']['company_id']}")
        print(f"基準会計年度ID: {result['data']['base_fiscal_year_id']}")
        print(f"作成日時: {result['data']['created_at']}")
        print(f"メッセージ: {result['message']}")
        print("=" * 80)
        
        return result['data']['id']
        
    except requests.exceptions.RequestException as e:
        print(f"エラー: {e}")
        return None


def example_get_multi_year_plan(company_id):
    """複数年度計画の取得例"""
    
    url = f"{BASE_URL}/decision/multi-year-plan/get-by-company"
    params = {"company_id": company_id}
    
    try:
        response = session.get(url, params=params)
        response.raise_for_status()
        
        result = response.json()
        print("\n" + "=" * 80)
        print("複数年度計画の取得 成功")
        print("=" * 80)
        print(f"取得件数: {result['count']}")
        
        for plan in result['data']:
            print(f"\n計画ID: {plan['id']}")
            print(f"基準会計年度ID: {plan['base_fiscal_year_id']}")
            print(f"備考: {plan['notes']}")
            
            # Year1の概要を表示
            year1 = plan['years']['year1']
            print(f"\n【Year1 概要】")
            print(f"  労務費: {year1['laborPlan']['totalLaborCost']:,}円")
            print(f"  設備投資: {year1['capexPlan']['total']:,}円")
            print(f"  新規借入: {year1['financingPlan']['newLoans']:,}円")
            print(f"  返済額: {year1['repaymentPlan']['totalPayment']:,}円")
        
        print("=" * 80)
        
        return result['data']
        
    except requests.exceptions.RequestException as e:
        print(f"エラー: {e}")
        return None


def example_update_multi_year_plan(company_id, base_fiscal_year_id):
    """複数年度計画の更新例"""
    
    url = f"{BASE_URL}/decision/multi-year-plan/create-or-update"
    
    # 既存の計画を取得
    plans = example_get_multi_year_plan(company_id)
    
    if not plans:
        print("更新対象の計画が見つかりません")
        return
    
    # 最初の計画を更新
    plan = plans[0]
    
    # Year1の従業員数を更新
    plan['years']['year1']['laborPlan']['totalEmployees'] = 52
    plan['years']['year1']['laborPlan']['totalLaborCost'] = 260000000
    plan['notes'] = "更新: 採用計画の見直しにより従業員数を増加"
    
    data = {
        "company_id": company_id,
        "base_fiscal_year_id": base_fiscal_year_id,
        "years": plan['years'],
        "notes": plan['notes']
    }
    
    try:
        response = session.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        print("\n" + "=" * 80)
        print("複数年度計画の更新 成功")
        print("=" * 80)
        print(f"メッセージ: {result['message']}")
        print(f"更新日時: {result['data']['updated_at']}")
        print("=" * 80)
        
    except requests.exceptions.RequestException as e:
        print(f"エラー: {e}")


def example_delete_multi_year_plan(plan_id):
    """複数年度計画の削除例"""
    
    url = f"{BASE_URL}/decision/multi-year-plan/delete/{plan_id}"
    
    try:
        response = session.delete(url)
        response.raise_for_status()
        
        result = response.json()
        print("\n" + "=" * 80)
        print("複数年度計画の削除 成功")
        print("=" * 80)
        print(f"メッセージ: {result['message']}")
        print("=" * 80)
        
    except requests.exceptions.RequestException as e:
        print(f"エラー: {e}")


if __name__ == "__main__":
    print("複数年度計画API 使用例")
    print("=" * 80)
    print("注意: このスクリプトは使用例を示すものです。")
    print("実際に実行するには、認証とデータベース接続が必要です。")
    print("=" * 80)
    
    # 使用例の表示
    print("\n【使用例1】複数年度計画の作成")
    print("plan_id = example_create_multi_year_plan()")
    
    print("\n【使用例2】複数年度計画の取得")
    print("plans = example_get_multi_year_plan(company_id=1)")
    
    print("\n【使用例3】複数年度計画の更新")
    print("example_update_multi_year_plan(company_id=1, base_fiscal_year_id=1)")
    
    print("\n【使用例4】複数年度計画の削除")
    print("example_delete_multi_year_plan(plan_id=1)")
