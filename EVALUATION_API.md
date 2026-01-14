# 評価API ドキュメント

## 概要

前年比較により評価記号（◎◯△×）を返すAPIです。

## 評価基準

| 前年比      | 評価記号 |
| :---------- | :------- |
| +10%以上    | ◎        |
| 0〜+10%     | ◯        |
| 0〜-10%     | △        |
| -10%未満    | ×        |

## エンドポイント

### GET /decision/evaluation/get

前年比較により評価記号を返します。

## リクエスト

### クエリパラメータ

| パラメータ名      | 型      | 必須 | 説明                     |
| :---------------- | :------ | :--- | :----------------------- |
| company_id        | integer | ✓    | 企業ID                   |
| fiscal_year_id    | integer | ✓    | 当年の会計年度ID         |

### リクエスト例

```http
GET /decision/evaluation/get?company_id=1&fiscal_year_id=2
```

## レスポンス

### レスポンス構造

```json
{
  "success": true,
  "data": {
    "fiscalYear": {
      "id": 2,
      "label": "2025年度"
    },
    "prevFiscalYear": {
      "id": 1,
      "label": "2024年度"
    },
    "pl": {
      "sales": {
        "thisYear": 1100000000,
        "prevYear": 1000000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "costOfSales": {
        "thisYear": 660000000,
        "prevYear": 600000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "grossProfit": {
        "thisYear": 440000000,
        "prevYear": 400000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "operatingExpenses": {
        "thisYear": 220000000,
        "prevYear": 200000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "operatingIncome": {
        "thisYear": 220000000,
        "prevYear": 200000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "nonOperatingIncome": {
        "thisYear": 10000000,
        "prevYear": 10000000,
        "ratio": 0.00,
        "grade": "◯"
      },
      "nonOperatingExpenses": {
        "thisYear": 5000000,
        "prevYear": 5000000,
        "ratio": 0.00,
        "grade": "◯"
      },
      "ordinaryIncome": {
        "thisYear": 225000000,
        "prevYear": 205000000,
        "ratio": 9.76,
        "grade": "◯"
      },
      "extraordinaryIncome": {
        "thisYear": 0,
        "prevYear": 0,
        "ratio": 0.00,
        "grade": "◯"
      },
      "extraordinaryLoss": {
        "thisYear": 0,
        "prevYear": 0,
        "ratio": 0.00,
        "grade": "◯"
      },
      "incomeBeforeTax": {
        "thisYear": 225000000,
        "prevYear": 205000000,
        "ratio": 9.76,
        "grade": "◯"
      },
      "incomeTax": {
        "thisYear": 67500000,
        "prevYear": 61500000,
        "ratio": 9.76,
        "grade": "◯"
      },
      "netIncome": {
        "thisYear": 157500000,
        "prevYear": 143500000,
        "ratio": 9.76,
        "grade": "◯"
      }
    },
    "bs": {
      "currentAssets": {
        "thisYear": 550000000,
        "prevYear": 500000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "fixedAssets": {
        "thisYear": 880000000,
        "prevYear": 800000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "totalAssets": {
        "thisYear": 1430000000,
        "prevYear": 1300000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "currentLiabilities": {
        "thisYear": 330000000,
        "prevYear": 300000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "fixedLiabilities": {
        "thisYear": 440000000,
        "prevYear": 400000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "totalLiabilities": {
        "thisYear": 770000000,
        "prevYear": 700000000,
        "ratio": 10.00,
        "grade": "◎"
      },
      "capital": {
        "thisYear": 100000000,
        "prevYear": 100000000,
        "ratio": 0.00,
        "grade": "◯"
      },
      "retainedEarnings": {
        "thisYear": 560000000,
        "prevYear": 500000000,
        "ratio": 12.00,
        "grade": "◎"
      },
      "totalEquity": {
        "thisYear": 660000000,
        "prevYear": 600000000,
        "ratio": 10.00,
        "grade": "◎"
      }
    }
  }
}
```

### データ項目

#### fiscalYear / prevFiscalYear

当年と前年の会計年度情報

```json
{
  "id": 2,
  "label": "2025年度"
}
```

#### pl（損益計算書）

各指標の評価結果

```json
{
  "sales": {
    "thisYear": 1100000000,
    "prevYear": 1000000000,
    "ratio": 10.00,
    "grade": "◎"
  }
}
```

**含まれる指標**:
- sales: 売上高
- costOfSales: 売上原価
- grossProfit: 売上総利益
- operatingExpenses: 販売費及び一般管理費
- operatingIncome: 営業利益
- nonOperatingIncome: 営業外収益
- nonOperatingExpenses: 営業外費用
- ordinaryIncome: 経常利益
- extraordinaryIncome: 特別利益
- extraordinaryLoss: 特別損失
- incomeBeforeTax: 税引前当期純利益
- incomeTax: 法人税等
- netIncome: 当期純利益

#### bs（貸借対照表）

各指標の評価結果

```json
{
  "totalAssets": {
    "thisYear": 1430000000,
    "prevYear": 1300000000,
    "ratio": 10.00,
    "grade": "◎"
  }
}
```

**含まれる指標**:
- currentAssets: 流動資産
- fixedAssets: 固定資産
- totalAssets: 総資産
- currentLiabilities: 流動負債
- fixedLiabilities: 固定負債
- totalLiabilities: 総負債
- capital: 資本金
- retainedEarnings: 利益剰余金
- totalEquity: 純資産

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

```json
{
  "error": "前年の会計年度が見つかりません"
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
// 評価データを取得
const response = await fetch(
  '/decision/evaluation/get?company_id=1&fiscal_year_id=2'
);
const data = await response.json();

// 年度情報を表示
console.log(`当年: ${data.data.fiscalYear.label}`);
console.log(`前年: ${data.data.prevFiscalYear.label}`);

// PL評価を表示
Object.entries(data.data.pl).forEach(([key, value]) => {
  console.log(`${key}: ${value.grade} (${value.ratio}%)`);
});

// BS評価を表示
Object.entries(data.data.bs).forEach(([key, value]) => {
  console.log(`${key}: ${value.grade} (${value.ratio}%)`);
});
```

### Python

```python
import requests

response = requests.get(
    'http://localhost:5000/decision/evaluation/get',
    params={
        'company_id': 1,
        'fiscal_year_id': 2
    }
)

data = response.json()

# 年度情報
print(f"当年: {data['data']['fiscalYear']['label']}")
print(f"前年: {data['data']['prevFiscalYear']['label']}")

# PL評価
for key, value in data['data']['pl'].items():
    print(f"{key}: {value['grade']} ({value['ratio']}%)")

# BS評価
for key, value in data['data']['bs'].items():
    print(f"{key}: {value['grade']} ({value['ratio']}%)")
```

### curl

```bash
curl "http://localhost:5000/decision/evaluation/get?company_id=1&fiscal_year_id=2"
```

## ヘルパー関数

### evaluate_yoy(value_this_year, value_prev_year)

単一の指標を評価します。

**パラメータ**:
- `value_this_year`: 当年の値
- `value_prev_year`: 前年の値

**戻り値**:
```python
{
    'ratio': 10.00,  # 前年比（%）
    'grade': '◎'    # 評価記号
}
```

**使用例**:
```python
from app.utils.evaluation_helpers import evaluate_yoy

result = evaluate_yoy(1100, 1000)
print(result)  # {'ratio': 10.0, 'grade': '◎'}
```

### evaluate_multiple_indicators(indicators_this_year, indicators_prev_year)

複数の指標を一括評価します。

**パラメータ**:
- `indicators_this_year`: dict - 当年の指標（キー: 指標名、値: 数値）
- `indicators_prev_year`: dict - 前年の指標（キー: 指標名、値: 数値）

**戻り値**:
```python
{
    '指標名': {
        'thisYear': 1100000000,
        'prevYear': 1000000000,
        'ratio': 10.00,
        'grade': '◎'
    }
}
```

**使用例**:
```python
from app.utils.evaluation_helpers import evaluate_multiple_indicators

indicators_this_year = {
    'sales': 1100000000,
    'operatingIncome': 220000000
}

indicators_prev_year = {
    'sales': 1000000000,
    'operatingIncome': 200000000
}

results = evaluate_multiple_indicators(indicators_this_year, indicators_prev_year)
print(results['sales'])  # {'thisYear': 1100000000, 'prevYear': 1000000000, 'ratio': 10.0, 'grade': '◎'}
```

## データソース

- **PL（損益計算書）**: `profit_loss_statements` テーブル
- **BS（貸借対照表）**: `balance_sheets` テーブル

## 前年の判定ロジック

前年の会計年度は、以下の条件で自動的に判定されます。

1. 同じ企業（company_id）
2. 開始日が当年より前
3. 最も近い会計年度（開始日の降順で最初）

## 前年が0の場合の処理

前年の値が0の場合、以下のように処理されます。

| 当年の値 | 前年比  | 評価 |
| :------- | :------ | :--- |
| > 0      | +100%   | ◎    |
| = 0      | 0%      | ◯    |
| < 0      | -100%   | ×    |

## 注意事項

### 指標の意味解釈なし

このAPIは前年比の計算と評価記号の付与のみを行います。指標の意味解釈は行いません。

### 評価基準の固定

評価基準は以下の通り固定されており、変更できません。

- +10%以上: ◎
- 0〜+10%: ◯
- 0〜-10%: △
- -10%未満: ×

## セキュリティ

- テナント管理者またはシステム管理者のみアクセス可能
- テナントIDによるデータアクセス制限
- 企業の所有権確認

## テスト

テストスクリプト: `test_evaluation_api.py`

実行方法:
```bash
python3 test_evaluation_api.py
```

## 実装ファイル

- **ヘルパー関数**: `app/utils/evaluation_helpers.py`
- **Blueprint**: `app/blueprints/evaluation_bp.py`
- **登録**: `app/__init__.py`

## 作成日

2024年1月13日
