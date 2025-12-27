# 財務諸表組換えAPI仕様書

## 概要
標準的な財務諸表を経営分析用の組換え財務諸表に変換するAPIです。Excelの「組換え手順」に基づいて実装されています。

## ベースURL
```
http://localhost:5000/api/restructuring
```

---

## 損益計算書（P/L）組換えAPI

### 1. P/Lを組換えて保存
**POST** `/api/restructuring/pl/{fiscal_year_id}`

標準的なP/Lデータから組換えP/Lを生成し、データベースに保存します。

**リクエストボディ:**
```json
{
  "additional_data": {
    "labor_cost_manufacturing": 5000000,
    "depreciation_manufacturing": 2000000,
    "repair_cost_manufacturing": 500000,
    "labor_cost_pl": 3000000,
    "personnel_expenses": 10000000,
    "executive_welfare": 200000,
    "depreciation_pl": 1500000,
    "repair_cost_pl": 300000,
    "variable_expenses": 5000000,
    "interest_income": 100000,
    "interest_expense": 500000
  }
}
```

**additional_dataの項目説明:**
- `labor_cost_manufacturing`: 製造原価報告書の労務費
- `depreciation_manufacturing`: 製造原価報告書の減価償却費
- `repair_cost_manufacturing`: 製造原価報告書の修繕費
- `labor_cost_pl`: P/Lの労務費（役員を除く）
- `personnel_expenses`: P/Lの人件費
- `executive_welfare`: 役員に関する法定福利費
- `depreciation_pl`: P/Lの減価償却費
- `repair_cost_pl`: P/Lの修繕費
- `variable_expenses`: 変動費（販売手数料、荷造発送費、運送費など）
- `interest_income`: 受取利息
- `interest_expense`: 支払利息

**レスポンス (201 Created):**
```json
{
  "restructured_pl": {
    "id": 1,
    "fiscal_year_id": 1,
    "sales": 100000000,
    "cost_of_sales": 60000000,
    "gross_profit": 40000000,
    "selling_general_admin_expenses": 25000000,
    "operating_income": 15000000,
    "non_operating_income": 1000000,
    "non_operating_expenses": 500000,
    "ordinary_income": 15500000,
    "extraordinary_income": 0,
    "extraordinary_loss": 0,
    "income_before_tax": 15500000,
    "income_taxes": 4650000,
    "net_income": 10850000
  },
  "added_value_components": {
    "gross_added_value": 47500000,
    "net_added_value": 43700000,
    "total_labor_cost": 18000000,
    "executive_compensation": 1200000,
    "capital_regeneration_cost": 3800000,
    "research_development_expenses": 0,
    "financial_profit_loss": -400000,
    "labor_distribution_ratio": 37.89,
    "executive_distribution_ratio": 2.53,
    "capital_distribution_ratio": 8.0
  },
  "detailed_restructuring": {
    "sales": 100000000,
    "cost_of_sales": 60000000,
    "gross_profit": 40000000,
    "gross_added_value": 47500000,
    "external_expense_adjustment": 7500000,
    "total_labor_cost": 18000000,
    "executive_compensation": 1200000,
    "capital_regeneration_cost": 3800000,
    "research_development_expenses": 0,
    "variable_expenses": 5000000,
    "fixed_expenses": 20000000,
    "selling_general_admin_expenses": 25000000,
    "operating_income": 15000000,
    "financial_profit_loss": -400000,
    "non_operating_income": 1000000,
    "non_operating_expenses": 500000,
    "ordinary_income": 15500000,
    "extraordinary_income": 0,
    "extraordinary_loss": 0,
    "income_before_tax": 15500000,
    "income_taxes": 4650000,
    "net_income": 10850000
  }
}
```

### 2. 組換えP/Lを取得
**GET** `/api/restructuring/pl/{fiscal_year_id}`

**レスポンス (200 OK):**
```json
{
  "id": 1,
  "fiscal_year_id": 1,
  "sales": 100000000,
  "cost_of_sales": 60000000,
  "gross_profit": 40000000,
  "selling_general_admin_expenses": 25000000,
  "operating_income": 15000000,
  "non_operating_income": 1000000,
  "non_operating_expenses": 500000,
  "ordinary_income": 15500000,
  "extraordinary_income": 0,
  "extraordinary_loss": 0,
  "income_before_tax": 15500000,
  "income_taxes": 4650000,
  "net_income": 10850000,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

## 貸借対照表（B/S）組換えAPI

### 1. B/Sを組換えて保存
**POST** `/api/restructuring/bs/{fiscal_year_id}`

標準的なB/Sデータから組換えB/Sを生成し、データベースに保存します。

**リクエストボディ:**
```json
{
  "additional_data": {
    "cash_and_deposits": 10000000,
    "time_deposits": 5000000,
    "accounts_receivable": 15000000,
    "notes_receivable": 8000000,
    "other_receivables": 2000000,
    "merchandise_inventory": 12000000,
    "work_in_process": 5000000,
    "raw_materials": 3000000,
    "supplies": 500000,
    "allowance_for_doubtful_accounts": 500000,
    "tangible_fixed_assets": 25000000,
    "intangible_fixed_assets": 2000000,
    "investments_and_other_assets": 3000000,
    "accounts_payable": 10000000,
    "notes_payable": 5000000,
    "other_payables": 3000000,
    "short_term_borrowings": 8000000,
    "current_portion_of_long_term_debt": 2000000,
    "other_current_liabilities": 2000000,
    "long_term_borrowings": 15000000,
    "executive_borrowings": 3000000,
    "other_fixed_liabilities": 1000000
  }
}
```

**additional_dataの項目説明:**

**流動資産:**
- `cash_and_deposits`: 現金及び預金
- `time_deposits`: 定期預金（運用預金）
- `accounts_receivable`: 売掛金
- `notes_receivable`: 受取手形
- `other_receivables`: 未収金
- `merchandise_inventory`: 製品（商品）
- `work_in_process`: 仕掛品
- `raw_materials`: 材料
- `supplies`: 貯蔵品
- `allowance_for_doubtful_accounts`: 貸倒引当金

**固定資産:**
- `tangible_fixed_assets`: 有形固定資産
- `intangible_fixed_assets`: 無形固定資産
- `investments_and_other_assets`: 投資その他の資産

**流動負債:**
- `accounts_payable`: 買掛金
- `notes_payable`: 支払手形
- `other_payables`: 未払金
- `short_term_borrowings`: 短期借入金
- `current_portion_of_long_term_debt`: 1年以内返済長期借入金
- `other_current_liabilities`: その他流動負債

**固定負債:**
- `long_term_borrowings`: 長期借入金
- `executive_borrowings`: 役員借入金
- `other_fixed_liabilities`: その他固定負債

**レスポンス (201 Created):**
```json
{
  "restructured_bs": {
    "id": 1,
    "fiscal_year_id": 1,
    "current_assets": 50000000,
    "fixed_assets": 30000000,
    "total_assets": 80000000,
    "current_liabilities": 20000000,
    "fixed_liabilities": 10000000,
    "total_liabilities": 30000000,
    "net_assets": 50000000,
    "total_liabilities_and_net_assets": 80000000
  },
  "detailed_restructuring": {
    "cash_on_hand": 5000000,
    "investment_deposits": 5000000,
    "trade_receivables": 25000000,
    "inventory_assets": 20500000,
    "allowance_for_doubtful_accounts": 500000,
    "current_assets": 50000000,
    "tangible_fixed_assets": 25000000,
    "intangible_fixed_assets": 2000000,
    "investments_and_other_assets": 3000000,
    "fixed_assets": 30000000,
    "total_assets": 80000000,
    "trade_payables": 18000000,
    "total_short_term_debt": 10000000,
    "other_current_liabilities": 2000000,
    "current_liabilities": 20000000,
    "long_term_debt_excluding_executive": 12000000,
    "executive_borrowings": 3000000,
    "other_fixed_liabilities": 1000000,
    "fixed_liabilities": 10000000,
    "total_liabilities": 30000000,
    "capital": 30000000,
    "retained_earnings": 20000000,
    "net_assets": 50000000,
    "total_liabilities_and_net_assets": 80000000
  }
}
```

### 2. 組換えB/Sを取得
**GET** `/api/restructuring/bs/{fiscal_year_id}`

**レスポンス (200 OK):**
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
  "net_assets": 50000000,
  "total_liabilities_and_net_assets": 80000000,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

## 組換えロジックの詳細

### P/L組換えの主要計算

1. **外部経費調整** = 労務費（製造） + 減価償却費（製造） + 修繕費（製造）
2. **粗付加価値** = 売上総利益 + 外部経費調整
3. **人件費** = 労務費（製造） + 労務費（P/L） + 人件費
4. **役員報酬** = 役員報酬 + 法定福利費（役員）
5. **資本再生費** = 減価償却費（製造） + 修繕費（製造） + 減価償却費（P/L） + 修繕費（P/L）
6. **金融損益** = 受取利息 - 支払利息
7. **一般経費** = 固定費 + 変動費

### B/S組換えの主要計算

1. **手許現預金** = 現金及び預金 - 定期預金
2. **運用預金** = 定期預金
3. **売掛債権** = 売掛金 + 受取手形 + 未収金
4. **棚卸資産** = 製品 + 仕掛品 + 材料 + 貯蔵品
5. **買掛債務** = 買掛金 + 支払手形 + 未払金
6. **短期借入金** = 短期借入金 + 1年以内返済長期借入金
7. **長期借入金** = 長期借入金 - 役員借入金

### 付加価値の構成要素

1. **純付加価値** = 粗付加価値 - 減価償却費
2. **労働分配率** = 人件費 / 粗付加価値 × 100
3. **役員報酬配分率** = 役員報酬 / 粗付加価値 × 100
4. **資本再生費配分率** = 資本再生費 / 粗付加価値 × 100

---

## エラーレスポンス

**404 Not Found:**
```json
{
  "error": "会計年度が見つかりません"
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

### P/Lを組換えて保存
```bash
curl -X POST http://localhost:5000/api/restructuring/pl/1 \
  -H "Content-Type: application/json" \
  -d '{
    "additional_data": {
      "labor_cost_manufacturing": 5000000,
      "depreciation_manufacturing": 2000000,
      "repair_cost_manufacturing": 500000,
      "labor_cost_pl": 3000000,
      "personnel_expenses": 10000000,
      "executive_welfare": 200000,
      "depreciation_pl": 1500000,
      "repair_cost_pl": 300000,
      "variable_expenses": 5000000,
      "interest_income": 100000,
      "interest_expense": 500000
    }
  }'
```

### 組換えP/Lを取得
```bash
curl http://localhost:5000/api/restructuring/pl/1
```

### B/Sを組換えて保存
```bash
curl -X POST http://localhost:5000/api/restructuring/bs/1 \
  -H "Content-Type: application/json" \
  -d '{
    "additional_data": {
      "cash_and_deposits": 10000000,
      "time_deposits": 5000000,
      "accounts_receivable": 15000000,
      "notes_receivable": 8000000,
      "other_receivables": 2000000,
      "merchandise_inventory": 12000000,
      "work_in_process": 5000000,
      "raw_materials": 3000000,
      "supplies": 500000,
      "allowance_for_doubtful_accounts": 500000,
      "tangible_fixed_assets": 25000000,
      "intangible_fixed_assets": 2000000,
      "investments_and_other_assets": 3000000,
      "accounts_payable": 10000000,
      "notes_payable": 5000000,
      "other_payables": 3000000,
      "short_term_borrowings": 8000000,
      "current_portion_of_long_term_debt": 2000000,
      "other_current_liabilities": 2000000,
      "long_term_borrowings": 15000000,
      "executive_borrowings": 3000000,
      "other_fixed_liabilities": 1000000
    }
  }'
```

### 組換えB/Sを取得
```bash
curl http://localhost:5000/api/restructuring/bs/1
```
