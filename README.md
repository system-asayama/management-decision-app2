# 経営意思決定支援システム (Python版)

management-decision-making-app（Node.js/TypeScript版）をPythonで再実装したプロジェクトです。

## 技術スタック

- **バックエンド**: Python 3.12 + Flask
- **データベース**: PostgreSQL + SQLAlchemy
- **認証**: JWT + セッション管理
- **デプロイ**: Heroku対応

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/system-asayama/management-decision-app2.git
cd management-decision-app2
```

### 2. 仮想環境の作成と依存関係のインストール

```bash
python3 -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env.example`を`.env`にコピーして編集：

```bash
cp .env.example .env
```

**重要な設定:**

```env
# モック認証を有効化（ローカル開発用）
ENABLE_MOCK_AUTH=true

# データベース接続文字列
DATABASE_URL=postgresql://user:password@localhost:5432/management_decision_making

# JWT秘密鍵
JWT_SECRET=your-secret-key-here
```

### 4. データベースのセットアップ

```bash
# PostgreSQLデータベースを作成
createdb management_decision_making

# マイグレーションを実行（TODO: 実装予定）
# python manage.py db upgrade
```

### 5. 開発サーバーの起動

```bash
python wsgi.py
```

ブラウザで `http://localhost:5000` にアクセスします。

## 認証システム

### モック認証（ローカル開発用）

`.env`ファイルに`ENABLE_MOCK_AUTH=true`を設定することで、認証をスキップできます。

モックユーザー情報:
- openId: `local-dev-user`
- name: `Local Developer`
- email: `dev@localhost`
- role: `admin`

### APIエンドポイント

#### 現在のユーザー情報を取得
```
GET /api/auth/me
```

#### ログイン
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "user",
  "password": "password"
}
```

#### ログアウト
```
POST /api/auth/logout
```

## プロジェクト構造

```
management-decision-app2/
├── app/
│   ├── __init__.py          # Flaskアプリケーション初期化
│   ├── auth.py              # 認証サービス
│   ├── config.py            # 設定ファイル
│   ├── logging.py           # ロギング設定
│   └── blueprints/
│       ├── __init__.py
│       ├── health.py        # ヘルスチェック
│       └── auth_bp.py       # 認証エンドポイント
├── requirements.txt         # Python依存関係
├── wsgi.py                  # WSGIエントリーポイント
├── Procfile                 # Herokuデプロイ設定
└── .env.example             # 環境変数テンプレート
```

## 移植状況

### ✅ 完了
- [x] プロジェクト初期セットアップ
- [x] 認証システム（モック認証対応）
- [x] セッション管理
- [x] JWT トークン生成・検証
- [x] 認証APIエンドポイント

### 🚧 進行中
- [ ] データベーススキーマ
- [ ] 財務データ管理API
- [ ] 経営分析機能
- [ ] シミュレーション機能
- [ ] フロントエンド

### 📋 予定
- [ ] 通知機能
- [ ] PDF出力
- [ ] Excelインポート/エクスポート
- [ ] テスト
- [ ] ドキュメント

## ライセンス

MIT License

## 元プロジェクト

このプロジェクトは[management-decision-making-app](https://github.com/system-asayama/management-decision-making-app)（Node.js/TypeScript版）をベースにしています。
