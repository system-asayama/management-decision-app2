# 複数年度計画統合管理機能 実装ドキュメント

## 概要

3期（複数年度）の個別計画を「1つの統合オブジェクト」として取得・保存できる機能を実装しました。

## 実装内容

### 1. データベーステーブル（multi_year_plans）

**ファイル**: `app/models_decision.py`

```python
class MultiYearPlan(Base):
    """複数年度計画統合テーブル（3期分の個別計画を統合管理）"""
    __tablename__ = 'multi_year_plans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    base_fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    years = Column(JSON, nullable=False)  # 3年分の計画データ
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
```

**テーブル構造**:
- `company_id`: 企業ID（外部キー）
- `base_fiscal_year_id`: 基準となる会計年度ID（外部キー）
- `years`: JSON型で3年分の計画データを格納
  - `year1`, `year2`, `year3`の各年度に以下の計画を含む：
    - `laborPlan`: 労務費計画
    - `capexPlan`: 設備投資計画
    - `workingCapitalPlan`: 運転資金計画
    - `financingPlan`: 資金調達計画
    - `repaymentPlan`: 返済計画

### 2. APIエンドポイント

**ファイル**: `app/blueprints/multi_year_plan_bp.py`

#### 2.1. 複数年度計画の作成または更新

**エンドポイント**: `POST /decision/multi-year-plan/create-or-update`

**リクエストボディ**:
```json
{
  "company_id": 1,
  "base_fiscal_year_id": 1,
  "years": {
    "year1": {
      "laborPlan": {...},
      "capexPlan": {...},
      "workingCapitalPlan": {...},
      "financingPlan": {...},
      "repaymentPlan": {...}
    },
    "year2": {...},
    "year3": {...}
  },
  "notes": "備考（オプション）"
}
```

**レスポンス**:
```json
{
  "success": true,
  "message": "複数年度計画を作成しました",
  "data": {
    "id": 1,
    "company_id": 1,
    "base_fiscal_year_id": 1,
    "years": {...},
    "notes": "...",
    "created_at": "2024-01-13T12:00:00",
    "updated_at": "2024-01-13T12:00:00"
  }
}
```

**機能**:
- 既存の計画がある場合は更新、ない場合は新規作成
- テナント権限チェックを実施
- 企業と会計年度の存在確認

#### 2.2. 企業IDで複数年度計画を取得

**エンドポイント**: `GET /decision/multi-year-plan/get-by-company`

**クエリパラメータ**:
- `company_id` (必須): 企業ID
- `base_fiscal_year_id` (オプション): 特定の会計年度の計画のみ取得

**レスポンス**:
```json
{
  "success": true,
  "count": 1,
  "data": [
    {
      "id": 1,
      "company_id": 1,
      "base_fiscal_year_id": 1,
      "years": {...},
      "notes": "...",
      "created_at": "2024-01-13T12:00:00",
      "updated_at": "2024-01-13T12:00:00"
    }
  ]
}
```

#### 2.3. 複数年度計画を削除

**エンドポイント**: `DELETE /decision/multi-year-plan/delete/<plan_id>`

**レスポンス**:
```json
{
  "success": true,
  "message": "複数年度計画を削除しました"
}
```

### 3. Blueprint登録

**ファイル**: `app/__init__.py`

```python
try:
    from .blueprints.multi_year_plan_bp import bp as multi_year_plan_bp
    app.register_blueprint(multi_year_plan_bp)
except Exception as e:
    print(f"⚠️ multi_year_plan blueprint 登録エラー: {e}")
```

## データ構造例

```json
{
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
  "year2": {...},
  "year3": {...}
}
```

## セキュリティ

- すべてのエンドポイントで `@require_roles` デコレータによる権限チェックを実施
- テナントIDによるデータアクセス制限
- 企業と会計年度の所有権確認

## 制約事項

以下の制約を遵守して実装しました：

✅ **実施済み**:
- 新規テーブル `multi_year_plans` の追加
- API エンドポイントの実装（create-or-update, get-by-company, delete）
- Blueprint の登録

❌ **実施していない（禁止事項）**:
- 計算ロジックの追加
- 既存計算式の変更
- 既存テーブルの破壊的変更

## テスト

テストスクリプト: `test_multi_year_plan_api.py`

実行方法:
```bash
python3 test_multi_year_plan_api.py
```

テスト内容:
1. テストデータの準備（企業、会計年度の作成）
2. 複数年度計画の作成
3. データの取得
4. データの更新
5. リレーションの確認
6. テストデータのクリーンアップ

## 使用方法

### フロントエンドからの呼び出し例

```javascript
// 複数年度計画の作成/更新
const response = await fetch('/decision/multi-year-plan/create-or-update', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    company_id: 1,
    base_fiscal_year_id: 1,
    years: {
      year1: { /* ... */ },
      year2: { /* ... */ },
      year3: { /* ... */ }
    },
    notes: '3期計画'
  })
});

// 複数年度計画の取得
const plans = await fetch('/decision/multi-year-plan/get-by-company?company_id=1');
const data = await plans.json();
```

## 今後の拡張可能性

- 年数を3期以外にも対応（4期、5期など）
- 計画のバージョン管理機能
- 計画の承認ワークフロー
- 計画と実績の比較分析機能
- 複数シナリオの並行管理

## 変更ファイル一覧

1. `app/models_decision.py` - MultiYearPlanモデルの追加
2. `app/blueprints/multi_year_plan_bp.py` - 新規Blueprint作成
3. `app/__init__.py` - Blueprint登録
4. `create_decision_tables.py` - モデルインポートに追加
5. `test_multi_year_plan_api.py` - テストスクリプト作成（新規）
6. `MULTI_YEAR_PLAN_IMPLEMENTATION.md` - 本ドキュメント（新規）

## 作成日

2024年1月13日
