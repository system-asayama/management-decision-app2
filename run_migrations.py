#!/usr/bin/env python3
"""
Heroku releaseフェーズで実行されるマイグレーションスクリプト
"""
import os
import sys

# アプリケーションのルートディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.db import get_db_connection, _is_pg

def run_migrations():
    """マイグレーションを実行"""
    print("=" * 60)
    print("マイグレーション開始")
    print("=" * 60)
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # マイグレーション1: T_管理者テーブルにactiveカラムを追加
        print("\n[マイグレーション] T_管理者テーブルにactiveカラムを追加...")
        
        try:
            if _is_pg(conn):
                # PostgreSQL: カラムが存在するか確認
                cur.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'T_管理者' AND column_name = 'active'
                """)
                if not cur.fetchone():
                    print("  - activeカラムが存在しません。追加します...")
                    cur.execute('ALTER TABLE "T_管理者" ADD COLUMN active INTEGER DEFAULT 1')
                    cur.execute('UPDATE "T_管理者" SET active = 1 WHERE active IS NULL')
                    conn.commit()
                    print("  ✅ T_管理者テーブルにactiveカラムを追加しました")
                else:
                    print("  ℹ️  activeカラムは既に存在します（スキップ）")
            else:
                # SQLite: PRAGMAでカラムを確認
                cur.execute('PRAGMA table_info("T_管理者")')
                columns = [row[1] for row in cur.fetchall()]
                if 'active' not in columns:
                    print("  - activeカラムが存在しません。追加します...")
                    cur.execute('ALTER TABLE "T_管理者" ADD COLUMN active INTEGER DEFAULT 1')
                    cur.execute('UPDATE "T_管理者" SET active = 1 WHERE active IS NULL')
                    conn.commit()
                    print("  ✅ T_管理者テーブルにactiveカラムを追加しました")
                else:
                    print("  ℹ️  activeカラムは既に存在します（スキップ）")
        except Exception as e:
            print(f"  ⚠️  マイグレーションエラー: {e}")
            conn.rollback()
            raise
        
        # マイグレーション2: T_従業員テーブルにactiveカラムを追加
        print("\n[マイグレーション] T_従業員テーブルにactiveカラムを追加...")
        
        try:
            if _is_pg(conn):
                # PostgreSQL: カラムが存在するか確認
                cur.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'T_従業員' AND column_name = 'active'
                """)
                if not cur.fetchone():
                    print("  - activeカラムが存在しません。追加します...")
                    cur.execute('ALTER TABLE "T_従業員" ADD COLUMN active INTEGER DEFAULT 1')
                    cur.execute('UPDATE "T_従業員" SET active = 1 WHERE active IS NULL')
                    conn.commit()
                    print("  ✅ T_従業員テーブルにactiveカラムを追加しました")
                else:
                    print("  ℹ️  activeカラムは既に存在します（スキップ）")
            else:
                # SQLite: PRAGMAでカラムを確認
                cur.execute('PRAGMA table_info("T_従業員")')
                columns = [row[1] for row in cur.fetchall()]
                if 'active' not in columns:
                    print("  - activeカラムが存在しません。追加します...")
                    cur.execute('ALTER TABLE "T_従業員" ADD COLUMN active INTEGER DEFAULT 1')
                    cur.execute('UPDATE "T_従業員" SET active = 1 WHERE active IS NULL')
                    conn.commit()
                    print("  ✅ T_従業員テーブルにactiveカラムを追加しました")
                else:
                    print("  ℹ️  activeカラムは既に存在します（スキップ）")
        except Exception as e:
            print(f"  ⚠️  マイグレーションエラー: {e}")
            conn.rollback()
            raise
        
        # マイグレーション3: T_テナント管理者_テナントテーブルにcan_manage_tenant_adminsカラムを追加
        print("\n[マイグレーション] T_テナント管理者_テナントテーブルにcan_manage_tenant_adminsカラムを追加...")
        
        try:
            if _is_pg(conn):
                # PostgreSQL: カラムが存在するか確認
                cur.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'T_テナント管理者_テナント' AND column_name = 'can_manage_tenant_admins'
                """)
                if not cur.fetchone():
                    print("  - can_manage_tenant_adminsカラムが存在しません。追加します...")
                    cur.execute('ALTER TABLE "T_テナント管理者_テナント" ADD COLUMN can_manage_tenant_admins INTEGER DEFAULT 0')
                    conn.commit()
                    print("  ✅ T_テナント管理者_テナントテーブルにcan_manage_tenant_adminsカラムを追加しました")
                else:
                    print("  ℹ️  can_manage_tenant_adminsカラムは既に存在します（スキップ）")
            else:
                # SQLite: PRAGMAでカラムを確認
                cur.execute('PRAGMA table_info("T_テナント管理者_テナント")')
                columns = [row[1] for row in cur.fetchall()]
                if 'can_manage_tenant_admins' not in columns:
                    print("  - can_manage_tenant_adminsカラムが存在しません。追加します...")
                    cur.execute('ALTER TABLE "T_テナント管理者_テナント" ADD COLUMN can_manage_tenant_admins INTEGER DEFAULT 0')
                    conn.commit()
                    print("  ✅ T_テナント管理者_テナントテーブルにcan_manage_tenant_adminsカラムを追加しました")
                else:
                    print("  ℹ️  can_manage_tenant_adminsカラムは既に存在します（スキップ）")
        except Exception as e:
            print(f"  ⚠️  マイグレーションエラー: {e}")
            conn.rollback()
            raise
        
        # マイグレーション4: T_管理者テーブルにemailカラムを追加
        print("\n[マイグレーション] T_管理者テーブルにemailカラムを追加...")
        
        try:
            if _is_pg(conn):
                # PostgreSQL: カラムが存在するか確認
                cur.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'T_管理者' AND column_name = 'email'
                """)
                if not cur.fetchone():
                    print("  - emailカラムが存在しません。追加します...")
                    cur.execute('ALTER TABLE "T_管理者" ADD COLUMN email TEXT')
                    conn.commit()
                    print("  ✅ T_管理者テーブルにemailカラムを追加しました")
                else:
                    print("  ℹ️  emailカラムは既に存在します（スキップ）")
            else:
                # SQLite: PRAGMAでカラムを確認
                cur.execute('PRAGMA table_info("T_管理者")')
                columns = [row[1] for row in cur.fetchall()]
                if 'email' not in columns:
                    print("  - emailカラムが存在しません。追加します...")
                    cur.execute('ALTER TABLE "T_管理者" ADD COLUMN email TEXT')
                    conn.commit()
                    print("  ✅ T_管理者テーブルにemailカラムを追加しました")
                else:
                    print("  ℹ️  emailカラムは既に存在します（スキップ）")
        except Exception as e:
            print(f"  ⚠️  マイグレーションエラー: {e}")
            conn.rollback()
            raise
        
        # マイグレーション5: T_管理者テーブルにopenai_api_keyカラムを追加
        print("\n[マイグレーション] T_管理者テーブルにopenai_api_keyカラムを追加...")
        
        try:
            if _is_pg(conn):
                # PostgreSQL: カラムが存在するか確認
                cur.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'T_管理者' AND column_name = 'openai_api_key'
                """)
                if not cur.fetchone():
                    print("  - openai_api_keyカラムが存在しません。追加します...")
                    cur.execute('ALTER TABLE "T_管理者" ADD COLUMN openai_api_key TEXT DEFAULT NULL')
                    conn.commit()
                    print("  ✅ T_管理者テーブルにopenai_api_keyカラムを追加しました")
                else:
                    print("  ℹ️  openai_api_keyカラムは既に存在します（スキップ）")
            else:
                # SQLite: PRAGMAでカラムを確認
                cur.execute('PRAGMA table_info("T_管理者")')
                columns = [row[1] for row in cur.fetchall()]
                if 'openai_api_key' not in columns:
                    print("  - openai_api_keyカラムが存在しません。追加します...")
                    cur.execute('ALTER TABLE "T_管理者" ADD COLUMN openai_api_key TEXT DEFAULT NULL')
                    conn.commit()
                    print("  ✅ T_管理者テーブルにopenai_api_keyカラムを追加しました")
                else:
                    print("  ℹ️  openai_api_keyカラムは既に存在します（スキップ）")
        except Exception as e:
            print(f"  ⚠️  マイグレーションエラー: {e}")
            conn.rollback()
            raise
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("マイグレーション完了")
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"\n❌ マイグレーション失敗: {e}")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(run_migrations())
