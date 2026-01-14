#!/usr/bin/env python3
"""
複数年度財務諸表シリーズAPI テストスクリプト
"""
import sys
import os

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db import SessionLocal
from app.models_decision import (
    Company, FiscalYear, ProfitLossStatement, BalanceSheet,
    CashFlowPlan, AnnualBudget
)
from datetime import datetime, date


def test_financial_series_api():
    """財務諸表シリーズAPIのテスト"""
    print("=" * 80)
    print("複数年度財務諸表シリーズAPI テスト")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        # テストデータの準備
        print("\n1. テストデータの準備...")
        
        # テスト用企業を作成
        test_company = Company(
            tenant_id=1,
            name="テスト企業（財務シリーズ）",
            industry="製造業",
            capital=10000000,
            employee_count=50
        )
        db.add(test_company)
        db.commit()
        db.refresh(test_company)
        print(f"✓ テスト企業作成: ID={test_company.id}")
        
        # 3期分の会計年度を作成
        fiscal_years = []
        for i in range(3):
            fy = FiscalYear(
                company_id=test_company.id,
                year_name=f"{2024+i}年度",
                start_date=date(2024+i, 4, 1),
                end_date=date(2025+i, 3, 31),
                months=12
            )
            db.add(fy)
            db.commit()
            db.refresh(fy)
            fiscal_years.append(fy)
            print(f"✓ 会計年度作成: ID={fy.id}, {fy.year_name}")
        
        # 各年度のPL実績を作成
        print("\n2. PL実績データの作成...")
        for i, fy in enumerate(fiscal_years):
            pl = ProfitLossStatement(
                fiscal_year_id=fy.id,
                sales=1000000000 + i * 100000000,
                cost_of_sales=600000000 + i * 60000000,
                gross_profit=400000000 + i * 40000000,
                operating_expenses=200000000 + i * 20000000,
                operating_income=200000000 + i * 20000000,
                non_operating_income=10000000,
                non_operating_expenses=5000000,
                ordinary_income=205000000 + i * 20000000,
                extraordinary_income=0,
                extraordinary_loss=0,
                income_before_tax=205000000 + i * 20000000,
                income_tax=61500000 + i * 6000000,
                net_income=143500000 + i * 14000000
            )
            db.add(pl)
            print(f"✓ PL実績作成: {fy.year_name} - 売上: {pl.sales:,}円")
        
        db.commit()
        
        # 各年度のBS実績を作成
        print("\n3. BS実績データの作成...")
        for i, fy in enumerate(fiscal_years):
            bs = BalanceSheet(
                fiscal_year_id=fy.id,
                current_assets=500000000 + i * 50000000,
                fixed_assets=800000000 + i * 80000000,
                total_assets=1300000000 + i * 130000000,
                current_liabilities=300000000 + i * 30000000,
                fixed_liabilities=400000000 + i * 40000000,
                total_liabilities=700000000 + i * 70000000,
                capital=100000000,
                retained_earnings=500000000 + i * 60000000,
                total_equity=600000000 + i * 60000000
            )
            db.add(bs)
            print(f"✓ BS実績作成: {fy.year_name} - 総資産: {bs.total_assets:,}円")
        
        db.commit()
        
        # 各年度のCF実績を作成（月次データ）
        print("\n4. CF実績データの作成...")
        for i, fy in enumerate(fiscal_years):
            for month in range(1, 13):
                cf = CashFlowPlan(
                    fiscal_year_id=fy.id,
                    month=month,
                    opening_balance=50000000 + month * 1000000,
                    actual_total_receipts=80000000 + i * 5000000,
                    actual_total_payments=70000000 + i * 4000000,
                    actual_closing_balance=60000000 + month * 1000000
                )
                db.add(cf)
            print(f"✓ CF実績作成: {fy.year_name} - 12ヶ月分")
        
        db.commit()
        
        # 各年度の予算を作成
        print("\n5. 予算データの作成...")
        for i, fy in enumerate(fiscal_years):
            budget = AnnualBudget(
                fiscal_year_id=fy.id,
                budget_sales=950000000 + i * 95000000,
                budget_cost_of_sales=570000000 + i * 57000000,
                budget_gross_profit=380000000 + i * 38000000,
                budget_operating_expenses=190000000 + i * 19000000,
                budget_operating_income=190000000 + i * 19000000,
                budget_non_operating_income=10000000,
                budget_non_operating_expenses=5000000,
                budget_ordinary_income=195000000 + i * 19000000,
                budget_extraordinary_income=0,
                budget_extraordinary_loss=0,
                budget_income_before_tax=195000000 + i * 19000000,
                budget_income_tax=58500000 + i * 5700000,
                budget_net_income=136500000 + i * 13300000,
                budget_current_assets=480000000 + i * 48000000,
                budget_fixed_assets=780000000 + i * 78000000,
                budget_total_assets=1260000000 + i * 126000000,
                budget_current_liabilities=290000000 + i * 29000000,
                budget_fixed_liabilities=390000000 + i * 39000000,
                budget_total_liabilities=680000000 + i * 68000000,
                budget_total_equity=580000000 + i * 58000000
            )
            db.add(budget)
            print(f"✓ 予算作成: {fy.year_name} - 予算売上: {budget.budget_sales:,}円")
        
        db.commit()
        
        # APIレスポンスのシミュレーション
        print("\n6. APIレスポンスのシミュレーション...")
        
        fiscal_year_ids = [fy.id for fy in fiscal_years]
        print(f"\n企業ID: {test_company.id}")
        print(f"会計年度IDs: {fiscal_year_ids}")
        
        print("\n【APIエンドポイント】")
        print(f"GET /decision/financial-series/get?company_id={test_company.id}&fiscal_year_ids={','.join(map(str, fiscal_year_ids))}&include_budget=true")
        
        print("\n【期待されるレスポンス構造】")
        print("""
{
  "success": true,
  "data": {
    "years": [
      {"fiscalYearId": 1, "label": "2024年度"},
      {"fiscalYearId": 2, "label": "2025年度"},
      {"fiscalYearId": 3, "label": "2026年度"}
    ],
    "actual": {
      "PL": [...],  // 3年分のPL実績
      "BS": [...],  // 3年分のBS実績
      "CF": [...]   // 3年分のCF実績
    },
    "budget": {
      "PL": [...],  // 3年分のPL予算
      "BS": [...],  // 3年分のBS予算
      "CF": [...]   // 3年分のCF予算
    },
    "variance": {
      "PL": [...],  // 3年分のPL差異（実績 - 予算）
      "BS": [...],  // 3年分のBS差異
      "CF": [...]   // 3年分のCF差異
    }
  }
}
        """)
        
        # クリーンアップ
        print("\n7. テストデータのクリーンアップ...")
        
        # 予算削除
        db.query(AnnualBudget).filter(
            AnnualBudget.fiscal_year_id.in_(fiscal_year_ids)
        ).delete(synchronize_session=False)
        
        # CF削除
        db.query(CashFlowPlan).filter(
            CashFlowPlan.fiscal_year_id.in_(fiscal_year_ids)
        ).delete(synchronize_session=False)
        
        # BS削除
        db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id.in_(fiscal_year_ids)
        ).delete(synchronize_session=False)
        
        # PL削除
        db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id.in_(fiscal_year_ids)
        ).delete(synchronize_session=False)
        
        # 会計年度削除
        for fy in fiscal_years:
            db.delete(fy)
        
        # 企業削除
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
    test_financial_series_api()
