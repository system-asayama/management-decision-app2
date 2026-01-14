#!/bin/bash
# Herokuでマイグレーションを実行するスクリプト

echo "=== Herokuマイグレーション実行 ==="
echo ""
echo "このスクリプトは、Heroku環境でデータベースマイグレーションを実行します。"
echo ""
echo "実行コマンド:"
echo "  heroku run python migrations/add_tenant_admin_tenant_table.py --app management-decision-making-app"
echo ""
echo "または、Heroku CLIがインストールされていない場合:"
echo "  1. Herokuダッシュボードにアクセス"
echo "  2. アプリケーション 'management-decision-making-app' を選択"
echo "  3. 'More' > 'Run console' をクリック"
echo "  4. 以下のコマンドを実行:"
echo "     python migrations/add_tenant_admin_tenant_table.py"
echo ""
