# Phase 6: 経営シミュレーション機能の実装計画

## 目標
複数年度の財務予測、シナリオ分析、成長率・利益率の調整機能を実装し、経営意思決定を支援する。

## 実装する機能

### 1. 基本シミュレーション機能
- [ ] ベース年度の選択（過去の実績データから開始）
- [ ] 予測年数の設定（1〜10年）
- [ ] 成長率の設定（売上高成長率）
- [ ] 利益率の設定（営業利益率、経常利益率、当期純利益率）
- [ ] 予測結果の計算と表示

### 2. シナリオ分析機能
- [ ] 楽観シナリオ（高成長率）
- [ ] 標準シナリオ（通常成長率）
- [ ] 悲観シナリオ（低成長率）
- [ ] 3つのシナリオの比較表示

### 3. 詳細パラメータ調整
- [ ] 売上原価率の調整
- [ ] 販管費率の調整
- [ ] 営業外収支の調整
- [ ] 特別損益の調整
- [ ] 税率の調整

### 4. 資産・負債の予測
- [ ] 総資産の予測（売上高との連動）
- [ ] 流動資産・固定資産の比率設定
- [ ] 負債比率の設定
- [ ] 自己資本比率の維持

### 5. グラフ表示
- [ ] 売上高推移グラフ
- [ ] 利益推移グラフ（営業利益、経常利益、当期純利益）
- [ ] 総資産・純資産推移グラフ
- [ ] 財務指標推移グラフ（ROA、ROE、自己資本比率）

### 6. シミュレーション結果の保存
- [ ] シミュレーション結果をデータベースに保存
- [ ] 過去のシミュレーション履歴の閲覧
- [ ] シミュレーション結果のエクスポート（CSV、PDF）

## 実装ファイル

### バックエンド
- `app/utils/simulation_calculator.py` - シミュレーション計算ロジック
- `app/models_decision.py` - Simulationモデルの追加
- `app/blueprints/decision.py` - シミュレーションルートの追加

### フロントエンド
- `app/templates/simulation.html` - シミュレーションページ
- `app/templates/simulation_result.html` - シミュレーション結果表示ページ

## データベーススキーマ

```sql
CREATE TABLE simulations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL,
    company_id INT NOT NULL,
    base_fiscal_year_id INT NOT NULL,
    simulation_name VARCHAR(200),
    forecast_years INT NOT NULL,
    sales_growth_rate DECIMAL(5,2),
    operating_margin DECIMAL(5,2),
    ordinary_margin DECIMAL(5,2),
    net_margin DECIMAL(5,2),
    scenario_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (base_fiscal_year_id) REFERENCES fiscal_years(id)
);

CREATE TABLE simulation_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    simulation_id INT NOT NULL,
    year_offset INT NOT NULL,
    sales DECIMAL(15,2),
    operating_income DECIMAL(15,2),
    ordinary_income DECIMAL(15,2),
    net_income DECIMAL(15,2),
    total_assets DECIMAL(15,2),
    total_liabilities DECIMAL(15,2),
    total_equity DECIMAL(15,2),
    FOREIGN KEY (simulation_id) REFERENCES simulations(id)
);
```

## 実装順序

1. **Phase 6.1: 計画立案とシミュレーション設計** ✓
   - TODO_PHASE6.mdの作成
   - データベーススキーマの設計

2. **Phase 6.2: シミュレーション計算ロジックの実装**
   - `simulation_calculator.py`の作成
   - 基本的な予測計算関数の実装

3. **Phase 6.3: シミュレーションUIの実装**
   - `simulation.html`の作成
   - パラメータ入力フォームの実装

4. **Phase 6.4: シナリオ分析機能の実装**
   - 楽観・標準・悲観シナリオの実装
   - シナリオ比較グラフの実装

5. **Phase 6.5: Herokuへのデプロイと本番環境テスト**
   - GitHubにプッシュ
   - Herokuにデプロイ
   - 本番環境でテスト

6. **Phase 6.6: Phase 6完了報告とユーザーへの結果提示**
   - テスト結果のまとめ
   - ユーザーへの報告

## 注意事項
- シミュレーションはあくまで予測であり、実際の結果を保証するものではないことを明記する
- パラメータの妥当性チェックを実装する（例: 成長率が-100%〜+1000%の範囲内）
- 複雑な計算は`simulation_calculator.py`に集約し、ルートはシンプルに保つ
