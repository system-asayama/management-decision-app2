# 環境変数テンプレート

プロジェクトルートに `.env` ファイルを作成し、以下の内容をコピーしてください。

```env
# Flask Secret Key
SECRET_KEY=your-secret-key-here-change-in-production

# Database URL (PostgreSQL)
# 優先順位: .env → 環境変数 → デフォルト(accounting_dev) → SQLite
DATABASE_URL=postgresql://postgres:password@localhost:5432/management_decision_making

# Application Settings
APP_NAME=management-decision-app
ENV=dev
DEBUG=1
APP_VERSION=0.1.0
TZ=Asia/Tokyo
```

## 設定項目の説明

### SECRET_KEY
Flaskのセッション暗号化に使用される秘密鍵です。本番環境では必ず変更してください。

### DATABASE_URL
PostgreSQLデータベースの接続文字列です。形式: `postgresql://ユーザー名:パスワード@ホスト:ポート/データベース名`

### APP_NAME
アプリケーション名です。

### ENV
実行環境です。`dev`（開発）または`production`（本番）を指定します。

### DEBUG
デバッグモードの有効/無効です。`1`で有効、`0`で無効になります。

### APP_VERSION
アプリケーションのバージョン番号です。

### TZ
タイムゾーンです。デフォルトは`Asia/Tokyo`（日本時間）です。
