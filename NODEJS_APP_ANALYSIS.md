# management-decision-making-app（Node.js版）分析結果

## 概要
Node.js + TypeScript + tRPC + Drizzle ORMで実装された経営意思決定支援システムの完全な分析結果です。

## データベーススキーマ（全20テーブル）

### 1. 基本マスタ
- **users**: ユーザー管理（Manus OAuth認証）
- **companies**: 企業マスタ
- **fiscalYears**: 会計年度管理

### 2. 財務諸表
- **profitLossStatements**: 損益計算書（簡易版）
- **balanceSheets**: 貸借対照表（簡易版）
- **restructuredPL**: 組換え損益計算書（詳細版）
- **restructuredBS**: 組換え貸借対照表（詳細版）

### 3. 人件費・労務管理
- **laborCosts**: 人件費データ
- **laborPlans**: 労務費管理計画（月次計画・実績）

### 4. 経営分析
- **financialIndicators**: 財務指標データ
- **businessSegments**: 事業セグメント（貢献度分析用）

### 5. 差額原価収益分析
- **differentialAnalyses**: 差額分析マスタ
- **differentialScenarios**: 差額分析シナリオ

### 6. 予算・計画管理
- **budgets**: 予算管理（月次予算・実績）
- **cashFlowPlans**: 資金繰り計画（月次計画・実績）
- **capitalInvestmentPlans**: 設備投資計画

### 7. 借入金管理
- **loans**: 借入金マスタ
- **loanRepayments**: 返済実績

### 8. シミュレーション
- **simulations**: シミュレーション設定
- **simulationResults**: シミュレーション結果

### 9. その他
- **notifications**: 通知管理
- **accountMappings**: 勘定科目マッピング（財務諸表組換え用）

## 実装済みAPI（tRPCルーター）

### 1. auth（認証）
- me: 現在のユーザー情報取得
- logout: ログアウト

### 2. company（企業管理）
- create: 企業作成
- list: 企業一覧取得
- getById: 企業詳細取得

### 3. fiscalYear（会計年度管理）
- create: 会計年度作成
- listByCompany: 企業別会計年度一覧
- getById: 会計年度詳細取得
- update: 会計年度更新
- delete: 会計年度削除

## Python移植の方針

### Phase 1: 基本機能（優先度：高）
1. 認証システム ✅ 完了（login-system-appをコピー済み）
2. 企業管理API
3. 会計年度管理API
4. 財務諸表入力API（P/L、B/S）
5. 基本的なダッシュボードUI

### Phase 2: 分析機能（優先度：中）
1. 財務諸表組換えロジック
2. 経営分析（4つの視点）の計算ロジック
3. 複数年度比較
4. グラフ表示（Matplotlib/Plotly）

## 技術スタック対応表

| Node.js版 | Python版 |
|-----------|----------|
| Express | Flask |
| tRPC | REST API（Flask Blueprint） |
| Drizzle ORM | SQLAlchemy |
| MySQL/TiDB | PostgreSQL |
| React | Jinja2テンプレート |
| TypeScript | Python 3.12 |
