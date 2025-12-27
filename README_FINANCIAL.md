# 経営意思決定支援システム（Management Decision Making App 2）

Excelベースの財務管理システムをPython（Flask）で完全再実装した、包括的な経営分析・シミュレーションシステムです。

## 📋 目次

- [概要](#概要)
- [主要機能](#主要機能)
- [技術スタック](#技術スタック)
- [セットアップ](#セットアップ)
- [使用方法](#使用方法)
- [API仕様](#api仕様)
- [データベース構造](#データベース構造)
- [開発ガイド](#開発ガイド)

---

## 概要

本システムは、中小企業の経営者や財務担当者向けに、財務データの入力から経営分析、将来予測まで一貫して行える統合的な経営支援ツールです。

### 元のExcelシステムとの対応

元のExcelファイル「簡易新エンジン3財務管理シミュレーション（個別計画あり）」の全49シートの機能を、Webアプリケーションとして再実装しました。

### 主な特徴

- **完全Web化**: ブラウザだけで利用可能、インストール不要
- **マルチユーザー対応**: 複数企業・複数年度のデータを一元管理
- **リアルタイム分析**: データ入力と同時に経営指標を自動計算
- **高度なシミュレーション**: 複数年度の経営計画を自動生成
- **視覚的なダッシュボード**: グラフとチャートで経営状況を可視化

---

## 主要機能

### 1. 財務データ管理

#### 企業マスタ管理
- 企業情報の登録・編集・削除
- 業種、従業員数などの基本情報管理

#### 会計年度管理
- 複数年度のデータ管理
- 実績・予算・予測の区分管理

#### 財務諸表入力
- **損益計算書（P/L）**: 売上高から当期純利益まで全項目入力
- **貸借対照表（B/S）**: 資産・負債・純資産の全項目入力
- 既存データの自動読込と更新機能

### 2. 財務諸表組換え

Excelの「組換え手順」を完全再現し、標準的な財務諸表を経営分析用に変換します。

#### P/L組換え
- 外部経費調整（製造原価報告書の統合）
- 粗付加価値の計算
- 人件費・役員報酬の分離
- 資本再生費の計算
- 金融損益の分離
- 固定費・変動費の区分

#### B/S組換え
- 手許現預金と運用預金の分離
- 売掛債権の集約
- 棚卸資産の集約
- 買掛債務の集約
- 短期借入金の集約
- 役員借入金の分離

### 3. 経営分析（4つの視点）

#### 成長力（12指標）
企業の成長性を評価します。

- 売上高成長率
- 売上原価成長率
- 付加価値成長率
- 人件費成長率
- 役員報酬成長率
- 資本再生費成長率
- 研究開発費成長率
- 一般経費成長率
- 固定資産成長率
- 他人資本成長率
- 税引前利益成長率
- 自己資本成長率

#### 収益力（8指標）
企業の収益性を多角的に評価します。

- 総資本経常利益率（ROA）
- 自己資本経常利益率（ROE）
- 経営資本営業利益率
- 売上高総利益率
- 売上高付加価値率
- 限界利益率
- 売上高売上原価率
- 各種回転率

#### 資金力（20指標）
資金調達・運用・返済能力を評価します。

**資金調達源泉の健全性:**
- 自己調達率（自己資本比率）
- 金融調達率
- 信用調達率

**資金調達余力:**
- 借入金依存率
- 担保余力
- 金融負担率

**資金運用能力:**
- 現預金回転期間
- 売掛債権回転率・回転期間
- 買掛債務回転率・回転期間
- 棚卸資産回転率・回転期間

**資金返済能力:**
- 流動比率
- 当座比率
- 現預金比率
- 長期適合率
- 非償却資産自己資本比率
- 償却資産長期負債比率

#### 生産力（6指標）
企業の生産性を評価します。

- 総資本付加価値率
- 付加価値労働生産性
- 利益生産性
- 労働分配率
- 設備投資効率
- 労働装備高

### 4. シミュレーション機能

#### 複数年度経営計画シミュレーション
基準年度のデータから3〜5年度の経営計画を自動生成します。

**設定可能な前提条件:**
- 売上成長率
- 売上原価率
- 販管費率
- 税率
- 配当性向

**予測項目:**
- 売上高、利益（営業利益、経常利益、当期純利益）
- 総資産、自己資本
- 自己資本比率、ROE、ROA
- 内部留保額

#### 内部留保シミュレーション
目標自己資本比率を達成するために必要な内部留保額を計算します。

**分析内容:**
- 現在の自己資本比率と目標値の比較
- 必要な内部留保総額
- 年間必要内部留保額
- 年度別の自己資本比率推移

#### 借入金許容限度額分析
企業が安全に借入できる限度額を3つの視点から計算します。

**分析視点:**
1. **自己資本比率から**: 目標自己資本比率を維持できる範囲
2. **担保余力から**: 有形固定資産を担保とした場合の借入可能額
3. **返済能力から**: 経常利益から算出した年間返済可能額

最も保守的な値を採用し、制約要因を明示します。

#### 損益分岐点分析
固定費と変動費を区分し、損益分岐点を計算します。

**計算指標:**
- 変動費率
- 限界利益率
- 損益分岐点売上高
- 損益分岐点比率
- 安全余裕率
- 経営安全率

#### 差額原価収益分析
2つのシナリオを比較し、意思決定を支援します。

**分析内容:**
- 差額売上高、差額原価、差額利益
- 差額利益率
- 投資回収期間
- 有利なシナリオの判定

### 5. ダッシュボード

#### 主要指標サマリー
- 売上高（前年比成長率付き）
- 経常利益（利益率付き）
- 総資産（ROA付き）
- 自己資本比率（評価コメント付き）

#### グラフ表示
- 売上高・利益推移グラフ（最新3年度）
- 財務構成グラフ（自己資本vs負債）

#### クイックアクション
主要機能へワンクリックでアクセスできるボタンを配置。

---

## 技術スタック

### バックエンド
- **Python 3.11**
- **Flask 3.0.0**: Webフレームワーク
- **SQLAlchemy 2.0.36**: ORM
- **PostgreSQL**: データベース（SQLiteも対応）
- **Alembic**: データベースマイグレーション

### フロントエンド
- **Jinja2**: テンプレートエンジン
- **Bootstrap 5.3**: UIフレームワーク
- **Bootstrap Icons**: アイコンライブラリ
- **Chart.js 4.3**: グラフライブラリ

### 認証システム
- **login-system-app**: マルチテナント対応の認証システム
- セッションベース認証
- ロールベースアクセス制御

---

## セットアップ

### 前提条件
- Python 3.11以上
- PostgreSQLまたはSQLite
- Git

### インストール手順

#### 1. リポジトリのクローン
```bash
git clone https://github.com/system-asayama/management-decision-app2.git
cd management-decision-app2
```

#### 2. 仮想環境の作成と有効化
```bash
python3 -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

#### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

#### 4. 環境変数の設定
`.env`ファイルを作成し、以下の内容を設定します：

```bash
# データベース接続
DATABASE_URL=postgresql://username:password@localhost:5432/financial_db
# または SQLite の場合
# DATABASE_URL=sqlite:///financial.db

# Flask設定
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# モック認証（開発環境のみ）
ENABLE_MOCK_AUTH=false
```

詳細は`ENV_TEMPLATE.md`を参照してください。

#### 5. データベースの初期化
```bash
python init_db.py
```

#### 6. アプリケーションの起動
```bash
python run.py
```

ブラウザで`http://localhost:5000`にアクセスします。

---

## 使用方法

### 1. ログイン
既存のlogin-system-appの認証システムを使用します。

### 2. 企業登録
1. サイドバーから「企業管理」をクリック
2. 「新規企業登録」ボタンをクリック
3. 企業名、業種、従業員数を入力

### 3. 会計年度登録
1. サイドバーから「会計年度管理」をクリック
2. 企業を選択
3. 「新規会計年度登録」ボタンをクリック
4. 年度、開始日、終了日を入力

### 4. 財務データ入力
1. サイドバーから「損益計算書入力」または「貸借対照表入力」をクリック
2. 企業と会計年度を選択
3. 各項目に金額を入力
4. 「保存」ボタンをクリック

### 5. 経営分析の実行
1. サイドバーから「経営分析」をクリック
2. 企業と会計年度を選択
3. 「分析実行」ボタンをクリック
4. 4つの視点（成長力、収益力、資金力、生産力）の指標が表示されます

### 6. シミュレーションの実行
1. サイドバーから「シミュレーション」をクリック
2. シミュレーションタイプを選択
3. 前提条件を入力
4. 「シミュレーション実行」ボタンをクリック
5. 結果がグラフと表で表示されます

---

## API仕様

### REST API エンドポイント

#### 企業管理
- `POST /api/company/` - 企業作成
- `GET /api/company/` - 企業一覧取得
- `GET /api/company/{id}` - 企業詳細取得
- `PUT /api/company/{id}` - 企業更新
- `DELETE /api/company/{id}` - 企業削除

#### 会計年度管理
- `POST /api/fiscal-year/` - 会計年度作成
- `GET /api/fiscal-year/company/{id}` - 企業別会計年度一覧
- `GET /api/fiscal-year/{id}` - 会計年度詳細取得
- `PUT /api/fiscal-year/{id}` - 会計年度更新
- `DELETE /api/fiscal-year/{id}` - 会計年度削除

#### 財務諸表
- `POST /api/profit-loss/` - P/L保存
- `GET /api/profit-loss/fiscal-year/{id}` - P/L取得
- `POST /api/balance-sheet/` - B/S保存
- `GET /api/balance-sheet/fiscal-year/{id}` - B/S取得

#### 財務諸表組換え
- `POST /api/restructuring/pl/{fiscal_year_id}` - P/L組換え
- `GET /api/restructuring/pl/{fiscal_year_id}` - 組換えP/L取得
- `POST /api/restructuring/bs/{fiscal_year_id}` - B/S組換え
- `GET /api/restructuring/bs/{fiscal_year_id}` - 組換えB/S取得

#### 経営分析
- `GET /api/analysis/growth/{fiscal_year_id}` - 成長力指標計算
- `GET /api/analysis/profitability/{fiscal_year_id}` - 収益力指標計算
- `GET /api/analysis/financial-strength/{fiscal_year_id}` - 資金力指標計算
- `GET /api/analysis/productivity/{fiscal_year_id}` - 生産力指標計算
- `GET /api/analysis/all/{fiscal_year_id}` - 全指標一括計算
- `POST /api/analysis/save/{fiscal_year_id}` - 指標保存

#### シミュレーション
- `POST /api/simulation/multi-year/{fiscal_year_id}` - 複数年度シミュレーション
- `POST /api/simulation/internal-reserve/{fiscal_year_id}` - 内部留保シミュレーション
- `POST /api/simulation/borrowing-capacity/{fiscal_year_id}` - 借入金許容限度額計算
- `POST /api/simulation/break-even/{fiscal_year_id}` - 損益分岐点分析
- `POST /api/simulation/differential-analysis` - 差額原価収益分析
- `GET /api/simulation/list/{fiscal_year_id}` - シミュレーション一覧
- `GET /api/simulation/{simulation_id}` - シミュレーション結果取得
- `DELETE /api/simulation/{simulation_id}` - シミュレーション削除

詳細なAPI仕様は以下のドキュメントを参照してください：
- `API_DOCUMENTATION.md` - 基本API
- `RESTRUCTURING_API_DOC.md` - 組換えAPI

---

## データベース構造

### 主要テーブル

#### マスタテーブル
- **users**: ユーザー情報
- **companies**: 企業マスタ
- **fiscal_years**: 会計年度

#### 財務諸表テーブル
- **profit_loss_statements**: 損益計算書（簡易版）
- **balance_sheets**: 貸借対照表（簡易版）
- **restructured_pl**: 組換え損益計算書
- **restructured_bs**: 組換え貸借対照表

#### 分析・計画テーブル
- **financial_indicators**: 経営指標計算結果
- **simulations**: シミュレーション設定
- **simulation_results**: シミュレーション結果
- **labor_costs**: 人件費データ
- **loans**: 借入金データ
- **loan_repayments**: 借入金返済計画

詳細なスキーマ定義は`app/models.py`を参照してください。

---

## 開発ガイド

### プロジェクト構造

```
management-decision-app2/
├── app/
│   ├── __init__.py              # Flaskアプリケーション初期化
│   ├── models.py                # SQLAlchemyモデル定義
│   ├── database.py              # データベースユーティリティ
│   ├── blueprints/              # Flask Blueprints
│   │   ├── auth.py              # 認証API
│   │   ├── company_bp.py        # 企業管理API
│   │   ├── fiscal_year_bp.py   # 会計年度管理API
│   │   ├── profit_loss_bp.py   # P/L管理API
│   │   ├── balance_sheet_bp.py # B/S管理API
│   │   ├── restructuring_bp.py # 組換えAPI
│   │   ├── analysis_bp.py      # 経営分析API
│   │   ├── simulation_bp.py    # シミュレーションAPI
│   │   └── financial_ui_bp.py  # UI Blueprint
│   ├── services/                # ビジネスロジック
│   │   ├── restructuring_service.py  # 組換えサービス
│   │   ├── analysis_service.py       # 経営分析サービス
│   │   └── simulation_service.py     # シミュレーションサービス
│   ├── templates/               # Jinja2テンプレート
│   │   ├── financial_base.html       # ベーステンプレート
│   │   ├── financial_dashboard.html  # ダッシュボード
│   │   └── ...
│   └── utils/                   # ユーティリティ
│       ├── db.py
│       ├── security.py
│       └── decorators.py
├── init_db.py                   # データベース初期化スクリプト
├── run.py                       # アプリケーション起動スクリプト
├── requirements.txt             # Python依存関係
├── .env.example                 # 環境変数テンプレート
└── README_FINANCIAL.md          # このファイル
```

### 新機能の追加方法

#### 1. モデルの追加
`app/models.py`に新しいSQLAlchemyモデルを追加します。

#### 2. サービスの追加
`app/services/`に新しいサービスクラスを作成します。

#### 3. APIエンドポイントの追加
`app/blueprints/`に新しいBlueprintを作成し、`app/__init__.py`で登録します。

#### 4. UIの追加
`app/templates/`に新しいテンプレートを作成し、`financial_ui_bp.py`にルートを追加します。

### テスト

```bash
# 単体テストの実行
pytest

# カバレッジレポート
pytest --cov=app
```

---

## トラブルシューティング

### データベース接続エラー
- `DATABASE_URL`が正しく設定されているか確認
- PostgreSQLサーバーが起動しているか確認
- データベースが作成されているか確認

### 認証エラー
- `SECRET_KEY`が設定されているか確認
- セッションCookieが有効か確認
- ログイン画面からログインし直す

### 計算結果が表示されない
- 財務データが正しく入力されているか確認
- 会計年度が正しく選択されているか確認
- ブラウザのコンソールでエラーを確認

---

## ライセンス

このプロジェクトは非公開プロジェクトです。

---

## お問い合わせ

問題や質問がある場合は、GitHubのIssuesで報告してください。

---

## 更新履歴

### v1.0.0 (2024-01-XX)
- 初回リリース
- 基本的な財務管理機能
- 経営分析機能（4つの視点）
- シミュレーション機能
- ダッシュボードUI
