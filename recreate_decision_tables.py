#!/usr/bin/env python3
"""
経営意思決定アプリのテーブルを削除して再作成するスクリプト
"""
import os
import sys

# アプリケーションのルートディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db import Base, engine
from app.models_decision import (
    Company, FiscalYear, ProfitLossStatement, BalanceSheet,
    RestructuredPL, RestructuredBS, LaborCost, FinancialIndicator,
    BusinessSegment, Budget, CashFlowPlan, LaborPlan, CapitalInvestmentPlan,
    Simulation, Loan, DifferentialAnalysis, Notification, AccountMapping
)

def recreate_tables():
    """経営意思決定アプリのテーブルを削除して再作成"""
    try:
        print("=" * 60)
        print("経営意思決定アプリ テーブル再作成スクリプト")
        print("=" * 60)
        
        # 削除するテーブルのリスト
        tables_to_drop = [
            'account_mappings',
            'notifications',
            'differential_analyses',
            'loans',
            'simulations',
            'capital_investment_plans',
            'labor_plans',
            'cash_flow_plans',
            'budgets',
            'business_segments',
            'financial_indicators',
            'labor_costs',
            'restructured_bs',
            'restructured_pl',
            'balance_sheets',
            'profit_loss_statements',
            'fiscal_years',
            'companies'
        ]
        
        print("\n1. テーブルを削除中...")
        with engine.connect() as conn:
            for table_name in tables_to_drop:
                try:
                    conn.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
                    conn.commit()
                    print(f"   ✓ {table_name} を削除しました")
                except Exception as e:
                    print(f"   ⚠ {table_name} の削除をスキップ: {e}")
        
        print("\n2. テーブルを再作成中...")
        Base.metadata.create_all(bind=engine)
        print("   ✓ 全テーブルを再作成しました")
        
        print("\n" + "=" * 60)
        print("✅ テーブル再作成完了！")
        print("=" * 60)
        
        # 作成されたテーブルの確認
        print("\n3. 作成されたテーブルを確認中...")
        with engine.connect() as conn:
            result = conn.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('companies', 'fiscal_years')
                ORDER BY table_name
            """)
            tables = [row[0] for row in result]
            
            if tables:
                print(f"   ✓ 確認されたテーブル: {', '.join(tables)}")
                
                # companiesテーブルのカラムを確認
                result = conn.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'companies' 
                    AND column_name IN ('tenant_id', 'capital', 'established_date', 'address', 'phone', 'email', 'website', 'notes')
                    ORDER BY column_name
                """)
                columns = [(row[0], row[1]) for row in result]
                
                if columns:
                    print("\n   companiesテーブルの新しいカラム:")
                    for col_name, col_type in columns:
                        print(f"     - {col_name} ({col_type})")
                else:
                    print("   ⚠ companiesテーブルに新しいカラムが見つかりません")
            else:
                print("   ⚠ テーブルが見つかりません")
        
        return True
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = recreate_tables()
    sys.exit(0 if success else 1)
