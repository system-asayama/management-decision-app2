# 複数年度財務諸表シリーズAPI ドキュメント

## 概要

複数年度のPL/BS/CF（実績＋予算）を並べて予実差異を返すAPIです。

## エンドポイント

### GET /decision/financial-series/get

複数年度の財務諸表データ（実績、予算、差異）を取得します。

## リクエスト

### クエリパラメータ

| パラメータ名      | 型      | 必須 | 説明                                                   |
| :---------------- | :------ | :--- | :----------------------------------------------------- |
| company_id        | integer | ✓    | 企業ID                                                 |
| fiscal_year_ids   | string  | ✓    | カンマ区切りの会計年度ID（例: "1,2,3"）                |
| include_budget    | string  |      | "true"または"false"（デフォルト: "false"）             |

### リクエスト例

```http
GET /decision/financial-series/get?company_id=1&fiscal_year_ids=1,2,3&include_budget=true
```

## レスポンス

### レスポンス構造

```json
{
  "success": true,
  "data": {
    "years": [
      {"fiscalYearId": 1, "label": "2024年度"},
      {"fiscalYearId": 2, "label": "2025年度"},
      {"fiscalYearId": 3, "label": "2026年度"}
    ],
    "actual": {
      "PL": [...],
      "BS": [...],
      "CF": [...]
    },
    "budget": {
      "PL": [...],
      "BS": [...],
      "CF": [...]
    },
    "variance": {
      "PL": [...],
      "BS": [...],
      "CF": [...]
    }
  }
}
```

### years配列

各年度の基本情報を含みます。

```json
{
  "fiscalYearId": 1,
  "label": "2024年度"
}
```

### actual.PL（損益計算書実績）

```json
{
  "fiscalYearId": 1,
  "sales": 1000000000,
  "costOfSales": 600000000,
  "grossProfit": 400000000,
  "operatingExpenses": 200000000,
  "operatingIncome": 200000000,
  "nonOperatingIncome": 10000000,
  "nonOperatingExpenses": 5000000,
  "ordinaryIncome": 205000000,
  "extraordinaryIncome": 0,
  "extraordinaryLoss": 0,
  "incomeBeforeTax": 205000000,
  "incomeTax": 61500000,
  "netIncome": 143500000
}
```

### actual.BS（貸借対照表実績）

```json
{
  "fiscalYearId": 1,
  "currentAssets": 500000000,
  "fixedAssets": 800000000,
  "totalAssets": 1300000000,
  "currentLiabilities": 300000000,
  "fixedLiabilities": 400000000,
  "totalLiabilities": 700000000,
  "capital": 100000000,
  "retainedEarnings": 500000000,
  "totalEquity": 600000000
}
```

### actual.CF（キャッシュフロー実績）

```json
{
  "fiscalYearId": 1,
  "totalReceipts": 960000000,
  "totalPayments": 840000000,
  "netCashFlow": 120000000,
  "closingBalance": 72000000
}
```

### budget（予算データ）

`include_budget=true`の場合のみ返されます。構造は`actual`と同じです。

### variance（差異データ）

`include_budget=true`の場合のみ返されます。実績 - 予算の差異を返します。

```json
{
  "fiscalYearId": 1,
  "sales": 50000000,  // 実績 - 予算
  "costOfSales": 30000000,
  "grossProfit": 20000000,
  ...
}
```

## エラーレスポンス

### 400 Bad Request

```json
{
  "error": "company_idは必須です"
}
```

### 403 Forbidden

```json
{
  "error": "テナントIDが見つかりません"
}
```

### 404 Not Found

```json
{
  "error": "企業が見つかりません"
}
```

### 500 Internal Server Error

```json
{
  "error": "データベースエラー: ..."
}
```

## 使用例

### JavaScript（フロントエンド）

```javascript
// 実績のみ取得
const response = await fetch(
  '/decision/financial-series/get?company_id=1&fiscal_year_ids=1,2,3'
);
const data = await response.json();

console.log(data.data.years);  // 年度一覧
console.log(data.data.actual.PL);  // PL実績

// 実績と予算を取得
const responseWithBudget = await fetch(
  '/decision/financial-series/get?company_id=1&fiscal_year_ids=1,2,3&include_budget=true'
);
const dataWithBudget = await responseWithBudget.json();

console.log(dataWithBudget.data.budget.PL);  // PL予算
console.log(dataWithBudget.data.variance.PL);  // PL差異
```

### Python

```python
import requests

# 実績のみ取得
response = requests.get(
    'http://localhost:5000/decision/financial-series/get',
    params={
        'company_id': 1,
        'fiscal_year_ids': '1,2,3'
    }
)
data = response.json()

# 実績と予算を取得
response_with_budget = requests.get(
    'http://localhost:5000/decision/financial-series/get',
    params={
        'company_id': 1,
        'fiscal_year_ids': '1,2,3',
        'include_budget': 'true'
    }
)
data_with_budget = response_with_budget.json()
```

### curl

```bash
# 実績のみ取得
curl "http://localhost:5000/decision/financial-series/get?company_id=1&fiscal_year_ids=1,2,3"

# 実績と予算を取得
curl "http://localhost:5000/decision/financial-series/get?company_id=1&fiscal_year_ids=1,2,3&include_budget=true"
```

## データソース

### PL（損益計算書）

- **実績**: `profit_loss_statements` テーブル
- **予算**: `annual_budgets` テーブル

### BS（貸借対照表）

- **実績**: `balance_sheets` テーブル
- **予算**: `annual_budgets` テーブル

### CF（キャッシュフロー）

- **実績**: `cash_flow_plans` テーブルの `actual_*` カラムを月次集計
- **予算**: `cash_flow_plans` テーブルの `planned_*` カラムを月次集計

## 注意事項

### 評価ロジックなし

このAPIは財務データの取得と差異計算のみを行います。評価（◎／○／△／×）は行いません。

### 集計の制限

勝手な集計は追加していません。既存のデータをそのまま返します。

### データがない場合

実績や予算データが存在しない会計年度については、すべての値が `0.0` で返されます。

### CF（キャッシュフロー）の集計

CFは月次データ（`cash_flow_plans`）を年次で集計します。

- **totalReceipts**: 12ヶ月分の `actual_total_receipts` の合計
- **totalPayments**: 12ヶ月分の `actual_total_payments` の合計
- **netCashFlow**: totalReceipts - totalPayments
- **closingBalance**: 最終月（12月）の `actual_closing_balance`

## セキュリティ

- テナント管理者またはシステム管理者のみアクセス可能
- テナントIDによるデータアクセス制限
- 企業の所有権確認

## テスト

テストスクリプト: `test_financial_series_api.py`

実行方法:
```bash
python3 test_financial_series_api.py
```

## 実装ファイル

- **Blueprint**: `app/blueprints/financial_series_bp.py`
- **登録**: `app/__init__.py`

## 作成日

2024年1月13日
