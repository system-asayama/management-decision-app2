# API仕様書

## 概要
management-decision-app2の財務管理API仕様書です。すべてのAPIはJSON形式でデータを送受信します。

## ベースURL
```
http://localhost:5000/api
```

## 認証
現在は認証なしでアクセス可能です。将来的にはJWT認証を実装予定です。

---

## 企業管理API

### 1. 企業を作成
**POST** `/api/company/`

**リクエストボディ:**
```json
{
  "name": "株式会社サンプル"
}
```

**レスポンス (201 Created):**
```json
{
  "id": 1,
  "name": "株式会社サンプル",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 2. 企業一覧を取得
**GET** `/api/company/`

**レスポンス (200 OK):**
```json
[
  {
    "id": 1,
    "name": "株式会社サンプル",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### 3. 企業詳細を取得
**GET** `/api/company/{company_id}`

**レスポンス (200 OK):**
```json
{
  "id": 1,
  "name": "株式会社サンプル",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 4. 企業情報を更新
**PUT** `/api/company/{company_id}`

**リクエストボディ:**
```json
{
  "name": "株式会社サンプル（更新）"
}
```

**レスポンス (200 OK):**
```json
{
  "id": 1,
  "name": "株式会社サンプル（更新）",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### 5. 企業を削除
**DELETE** `/api/company/{company_id}`

**レスポンス (200 OK):**
```json
{
  "message": "企業を削除しました"
}
```

---

## 会計年度管理API

### 1. 会計年度を作成
**POST** `/api/fiscal-year/`

**リクエストボディ:**
```json
{
  "company_id": 1,
  "year": 2023,
  "start_date": "2023-04-01T00:00:00",
  "end_date": "2024-03-31T23:59:59"
}
```

**レスポンス (201 Created):**
```json
{
  "id": 1,
  "company_id": 1,
  "year": 2023,
  "start_date": "2023-04-01T00:00:00",
  "end_date": "2024-03-31T23:59:59",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 2. 企業別の会計年度一覧を取得
**GET** `/api/fiscal-year/company/{company_id}`

**レスポンス (200 OK):**
```json
[
  {
    "id": 1,
    "company_id": 1,
    "year": 2023,
    "start_date": "2023-04-01T00:00:00",
    "end_date": "2024-03-31T23:59:59",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### 3. 会計年度詳細を取得
**GET** `/api/fiscal-year/{fiscal_year_id}`

### 4. 会計年度情報を更新
**PUT** `/api/fiscal-year/{fiscal_year_id}`

**リクエストボディ:**
```json
{
  "year": 2024,
  "start_date": "2024-04-01T00:00:00",
  "end_date": "2025-03-31T23:59:59"
}
```

### 5. 会計年度を削除
**DELETE** `/api/fiscal-year/{fiscal_year_id}`

---

## 損益計算書（P/L）管理API

### 1. 損益計算書を保存
**POST** `/api/profit-loss/`

**リクエストボディ:**
```json
{
  "fiscal_year_id": 1,
  "sales": 100000000,
  "cost_of_sales": 60000000,
  "gross_profit": 40000000,
  "operating_expenses": 25000000,
  "operating_income": 15000000,
  "non_operating_income": 1000000,
  "non_operating_expenses": 500000,
  "ordinary_income": 15500000,
  "extraordinary_income": 0,
  "extraordinary_loss": 0,
  "income_before_tax": 15500000,
  "income_tax": 4650000,
  "net_income": 10850000
}
```

**レスポンス (201 Created):**
```json
{
  "id": 1,
  "fiscal_year_id": 1,
  "sales": 100000000,
  "cost_of_sales": 60000000,
  "gross_profit": 40000000,
  "operating_expenses": 25000000,
  "operating_income": 15000000,
  "non_operating_income": 1000000,
  "non_operating_expenses": 500000,
  "ordinary_income": 15500000,
  "extraordinary_income": 0,
  "extraordinary_loss": 0,
  "income_before_tax": 15500000,
  "income_tax": 4650000,
  "net_income": 10850000,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 2. 会計年度別の損益計算書を取得
**GET** `/api/profit-loss/fiscal-year/{fiscal_year_id}`

### 3. 損益計算書を削除
**DELETE** `/api/profit-loss/{pl_id}`

---

## 貸借対照表（B/S）管理API

### 1. 貸借対照表を保存
**POST** `/api/balance-sheet/`

**リクエストボディ:**
```json
{
  "fiscal_year_id": 1,
  "current_assets": 50000000,
  "fixed_assets": 30000000,
  "total_assets": 80000000,
  "current_liabilities": 20000000,
  "fixed_liabilities": 10000000,
  "total_liabilities": 30000000,
  "capital": 30000000,
  "retained_earnings": 20000000,
  "total_equity": 50000000
}
```

**レスポンス (201 Created):**
```json
{
  "id": 1,
  "fiscal_year_id": 1,
  "current_assets": 50000000,
  "fixed_assets": 30000000,
  "total_assets": 80000000,
  "current_liabilities": 20000000,
  "fixed_liabilities": 10000000,
  "total_liabilities": 30000000,
  "capital": 30000000,
  "retained_earnings": 20000000,
  "total_equity": 50000000,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 2. 会計年度別の貸借対照表を取得
**GET** `/api/balance-sheet/fiscal-year/{fiscal_year_id}`

### 3. 貸借対照表を削除
**DELETE** `/api/balance-sheet/{bs_id}`

---

## ダッシュボードAPI

### 1. ダッシュボード用サマリーデータを取得
**GET** `/api/dashboard/summary/{company_id}`

**レスポンス (200 OK):**
```json
{
  "company": {
    "id": 1,
    "name": "株式会社サンプル"
  },
  "latest_fiscal_year": {
    "id": 1,
    "year": 2023,
    "start_date": "2023-04-01T00:00:00",
    "end_date": "2024-03-31T23:59:59"
  },
  "profit_loss": {
    "sales": 100000000,
    "operating_income": 15000000,
    "ordinary_income": 15500000,
    "net_income": 10850000
  },
  "balance_sheet": {
    "total_assets": 80000000,
    "total_liabilities": 30000000,
    "total_equity": 50000000
  },
  "fiscal_years_count": 3
}
```

### 2. 複数年度の財務データ比較を取得
**GET** `/api/dashboard/comparison/{company_id}`

**レスポンス (200 OK):**
```json
{
  "company_id": 1,
  "comparison_data": [
    {
      "fiscal_year": {
        "id": 3,
        "year": 2023,
        "start_date": "2023-04-01T00:00:00",
        "end_date": "2024-03-31T23:59:59"
      },
      "profit_loss": {
        "sales": 100000000,
        "cost_of_sales": 60000000,
        "gross_profit": 40000000,
        "operating_income": 15000000,
        "ordinary_income": 15500000,
        "net_income": 10850000
      },
      "balance_sheet": {
        "total_assets": 80000000,
        "total_liabilities": 30000000,
        "total_equity": 50000000
      }
    },
    {
      "fiscal_year": {
        "id": 2,
        "year": 2022,
        "start_date": "2022-04-01T00:00:00",
        "end_date": "2023-03-31T23:59:59"
      },
      "profit_loss": {
        "sales": 90000000,
        "cost_of_sales": 55000000,
        "gross_profit": 35000000,
        "operating_income": 12000000,
        "ordinary_income": 12500000,
        "net_income": 9000000
      },
      "balance_sheet": {
        "total_assets": 75000000,
        "total_liabilities": 28000000,
        "total_equity": 47000000
      }
    }
  ]
}
```

---

## エラーレスポンス

すべてのAPIで共通のエラーレスポンス形式を使用します。

**400 Bad Request:**
```json
{
  "error": "必須フィールドが不足しています"
}
```

**404 Not Found:**
```json
{
  "error": "リソースが見つかりません"
}
```

**500 Internal Server Error:**
```json
{
  "error": "内部サーバーエラーが発生しました"
}
```

---

## 使用例（curl）

### 企業を作成
```bash
curl -X POST http://localhost:5000/api/company/ \
  -H "Content-Type: application/json" \
  -d '{"name": "株式会社サンプル"}'
```

### 会計年度を作成
```bash
curl -X POST http://localhost:5000/api/fiscal-year/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": 1,
    "year": 2023,
    "start_date": "2023-04-01T00:00:00",
    "end_date": "2024-03-31T23:59:59"
  }'
```

### 損益計算書を保存
```bash
curl -X POST http://localhost:5000/api/profit-loss/ \
  -H "Content-Type: application/json" \
  -d '{
    "fiscal_year_id": 1,
    "sales": 100000000,
    "cost_of_sales": 60000000,
    "gross_profit": 40000000,
    "operating_expenses": 25000000,
    "operating_income": 15000000,
    "non_operating_income": 1000000,
    "non_operating_expenses": 500000,
    "ordinary_income": 15500000,
    "extraordinary_income": 0,
    "extraordinary_loss": 0,
    "income_before_tax": 15500000,
    "income_tax": 4650000,
    "net_income": 10850000
  }'
```

### ダッシュボードサマリーを取得
```bash
curl http://localhost:5000/api/dashboard/summary/1
```
