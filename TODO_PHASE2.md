# Phase 2: 経営意思決定アプリ統合 TODO

## 統合作業

### ステップ1: company_bp.py修正
- [x] インポート文を修正 (app.database → app.db)
- [x] インポート文を修正 (app.models → app.models_decision)
- [x] セッション管理を統一
- [ ] 動作確認

### ステップ2: 残り8個のblueprint修正
- [x] fiscal_year_bp.py - インポート修正
- [x] profit_loss_bp.py - インポート修正
- [x] balance_sheet_bp.py - インポート修正
- [x] dashboard_bp.py - インポート修正
- [x] restructuring_bp.py - インポート修正
- [x] analysis_bp.py - インポート修正
- [x] simulation_bp.py - インポート修正
- [x] financial_ui_bp.py - インポート修正

### ステップ3: データベーステーブル作成
- [x] テーブル作成スクリプト作成
- [ ] Heroku Postgresで実行
- [ ] テーブル作成確認

### ステップ4: 各機能の動作確認
- [ ] 企業管理 (company_bp.py)
- [ ] 会計年度管理 (fiscal_year_bp.py)
- [ ] 損益計算書 (profit_loss_bp.py)
- [ ] 貸借対照表 (balance_sheet_bp.py)
- [ ] 財務UI (financial_ui_bp.py)
- [ ] ダッシュボード (dashboard_bp.py)
- [ ] 財務諸表組換え (restructuring_bp.py)
- [ ] 経営分析 (analysis_bp.py)
- [ ] 経営シミュレーション (simulation_bp.py)

### ステップ5: UI更新
- [ ] decision_index.htmlにリンク追加
- [ ] 各機能へのナビゲーション確認

### ステップ6: デプロイ
- [x] GitHub にプッシュ
- [x] Heroku にデプロイ
- [x] 本番環境で動作確認

## 完了条件
- [ ] 全9個のblueprintが正常にインポート・登録される
- [ ] 企業管理機能が動作する（CRUD操作）
- [ ] 会計年度管理機能が動作する
- [ ] 財務データ入力機能が動作する（PL・BS）
- [ ] ダッシュボードが財務データを表示する
- [ ] エラーハンドリングが適切に実装されている
