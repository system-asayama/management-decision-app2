#!/usr/bin/env python3
"""
複数年度計画API テストスクリプト
"""
import sys
import os

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db import SessionLocal
from app.models_decision import MultiYearPlan, Company, FiscalYear
from datetime import datetime, date


def test_multi_year_plan_model():
    """MultiYearPlanモデルの動作確認"""
    print("=" * 80)
    print("複数年度計画モデル テスト")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        # テストデータの準備
        print("\n1. テストデータの準備...")
        
        # テスト用企業を作成
        test_company = Company(
            tenant_id=1,
            name="テスト企業（複数年度計画）",
            industry="製造業",
            capital=10000000,
            employee_count=50
        )
        db.add(test_company)
        db.commit()
        db.refresh(test_company)
        print(f"✓ テスト企業作成: ID={test_company.id}, 名前={test_company.name}")
        
        # テスト用会計年度を作成
        test_fiscal_year = FiscalYear(
            company_id=test_company.id,
            year_name="2024年度",
            start_date=date(2024, 4, 1),
            end_date=date(2025, 3, 31),
            months=12
        )
        db.add(test_fiscal_year)
        db.commit()
        db.refresh(test_fiscal_year)
        print(f"✓ テスト会計年度作成: ID={test_fiscal_year.id}, 年度名={test_fiscal_year.year_name}")
        
        # 複数年度計画データの作成
        print("\n2. 複数年度計画の作成...")
        
        years_data = {
            "year1": {
                "laborPlan": {
                    "totalEmployees": 50,
                    "averageSalary": 5000000,
                    "totalLaborCost": 250000000
                },
                "capexPlan": {
                    "equipment": 50000000,
                    "facilities": 30000000,
                    "total": 80000000
                },
                "workingCapitalPlan": {
                    "accountsReceivable": 100000000,
                    "inventory": 80000000,
                    "accountsPayable": 60000000
                },
                "financingPlan": {
                    "newLoans": 100000000,
                    "interestRate": 0.02
                },
                "repaymentPlan": {
                    "principalRepayment": 20000000,
                    "interestPayment": 2000000
                }
            },
            "year2": {
                "laborPlan": {
                    "totalEmployees": 55,
                    "averageSalary": 5100000,
                    "totalLaborCost": 280500000
                },
                "capexPlan": {
                    "equipment": 60000000,
                    "facilities": 40000000,
                    "total": 100000000
                },
                "workingCapitalPlan": {
                    "accountsReceivable": 110000000,
                    "inventory": 90000000,
                    "accountsPayable": 70000000
                },
                "financingPlan": {
                    "newLoans": 50000000,
                    "interestRate": 0.02
                },
                "repaymentPlan": {
                    "principalRepayment": 25000000,
                    "interestPayment": 2500000
                }
            },
            "year3": {
                "laborPlan": {
                    "totalEmployees": 60,
                    "averageSalary": 5200000,
                    "totalLaborCost": 312000000
                },
                "capexPlan": {
                    "equipment": 70000000,
                    "facilities": 50000000,
                    "total": 120000000
                },
                "workingCapitalPlan": {
                    "accountsReceivable": 120000000,
                    "inventory": 100000000,
                    "accountsPayable": 80000000
                },
                "financingPlan": {
                    "newLoans": 0,
                    "interestRate": 0.02
                },
                "repaymentPlan": {
                    "principalRepayment": 30000000,
                    "interestPayment": 3000000
                }
            }
        }
        
        multi_year_plan = MultiYearPlan(
            company_id=test_company.id,
            base_fiscal_year_id=test_fiscal_year.id,
            years=years_data,
            notes="3期計画のテストデータ"
        )
        
        db.add(multi_year_plan)
        db.commit()
        db.refresh(multi_year_plan)
        
        print(f"✓ 複数年度計画作成成功: ID={multi_year_plan.id}")
        print(f"  - 企業ID: {multi_year_plan.company_id}")
        print(f"  - 基準会計年度ID: {multi_year_plan.base_fiscal_year_id}")
        print(f"  - 作成日時: {multi_year_plan.created_at}")
        
        # データの取得テスト
        print("\n3. データの取得テスト...")
        
        retrieved_plan = db.query(MultiYearPlan).filter(
            MultiYearPlan.id == multi_year_plan.id
        ).first()
        
        if retrieved_plan:
            print(f"✓ データ取得成功: ID={retrieved_plan.id}")
            print(f"  - 年度データ: {list(retrieved_plan.years.keys())}")
            print(f"  - Year1労務費計画: {retrieved_plan.years['year1']['laborPlan']}")
        else:
            print("✗ データ取得失敗")
        
        # データの更新テスト
        print("\n4. データの更新テスト...")
        
        retrieved_plan.years['year1']['laborPlan']['totalEmployees'] = 52
        retrieved_plan.notes = "更新されたテストデータ"
        retrieved_plan.updated_at = datetime.now()
        
        db.commit()
        db.refresh(retrieved_plan)
        
        print(f"✓ データ更新成功")
        print(f"  - 更新後の従業員数: {retrieved_plan.years['year1']['laborPlan']['totalEmployees']}")
        print(f"  - 更新日時: {retrieved_plan.updated_at}")
        
        # リレーションのテスト
        print("\n5. リレーションのテスト...")
        
        print(f"✓ 企業情報: {retrieved_plan.company.name}")
        print(f"✓ 基準会計年度: {retrieved_plan.base_fiscal_year.year_name}")
        
        # クリーンアップ
        print("\n6. テストデータのクリーンアップ...")
        
        db.delete(retrieved_plan)
        db.delete(test_fiscal_year)
        db.delete(test_company)
        db.commit()
        
        print("✓ テストデータ削除完了")
        
        print("\n" + "=" * 80)
        print("✅ すべてのテストが成功しました！")
        print("=" * 80)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    test_multi_year_plan_model()
