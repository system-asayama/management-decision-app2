#!/usr/bin/env python3
"""
経営意思決定アプリのデータベーステーブルを作成するスクリプト
"""
import sys
import os

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db import Base, engine
from app.models_decision import (
    User, Company, FiscalYear, ProfitLossStatement, BalanceSheet,
    RestructuredPL, RestructuredBS, LaborCost, FinancialIndicator,
    BusinessSegment, Budget, CashFlowPlan, LaborPlan, CapitalInvestmentPlan,
    Simulation, SimulationYear, Loan, DifferentialAnalysis, Notification,
    AccountMapping, MultiYearPlan, WorkingCapitalAssumption, DebtRepaymentAssumption,
    MonthlyCashFlowPlan
)

def create_tables():
    """全テーブルを作成"""
    print("=" * 60)
    print("経営意思決定アプリ - データベーステーブル作成")
    print("=" * 60)
    
    try:
        print("\n📊 テーブル作成中...")
        Base.metadata.create_all(bind=engine)
        print("✅ テーブル作成成功！")
        
        # 作成されたテーブル一覧を表示
        print("\n📋 作成されたテーブル:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
        
        print(f"\n✅ 合計 {len(Base.metadata.tables)} 個のテーブルを作成しました")
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    create_tables()
