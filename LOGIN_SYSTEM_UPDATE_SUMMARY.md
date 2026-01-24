# ログインシステムアップデート実装サマリー

## 実装日時
2026-01-24

## 概要
management-decision-app2のログインシステムをlogin-system-appの最新版にアップデートしました。システム管理者に全テナント管理権限の有無を設定できる機能と、PostgreSQL/MySQL両対応の自動マイグレーション機能を実装しました。

## 実装内容

### 1. データベースモデルの更新 (`app/models_login.py`)

#### T_管理者テーブル
- **追加カラム**: `can_manage_all_tenants` (INTEGER, DEFAULT 0)
  - 全テナント管理権限（1=全テナントにアクセス可能、0=作成/招待されたテナントのみ）

#### T_テナントテーブル
- **追加カラム**: `created_by_admin_id` (INTEGER, NULLABLE)
  - このテナントを作成したシステム管理者のID
  - 外部キー制約: `T_管理者.id`

#### T_システム管理者_テナントテーブル（新規作成）
- システム管理者とテナントの多対多関係を管理する中間テーブル
- **カラム**:
  - `id`: 主キー
  - `admin_id`: システム管理者のID（外部キー）
  - `tenant_id`: テナントID（外部キー）
  - `created_at`: 作成日時
- **制約**: ユニーク制約 (`admin_id`, `tenant_id`)

### 2. 自動マイグレーション機能 (`app/auto_migrations.py`)

PostgreSQLとMySQLの両方に対応した自動マイグレーション機能を実装：

- **データベース種類の自動判定**: SQLAlchemyのdialectから自動的に判定
- **PostgreSQL対応**: ダブルクォート、SERIAL型、COMMENT ON文など
- **MySQL対応**: バッククォート、AUTO_INCREMENT、COMMENT句など
- **冪等性**: カラム/テーブルが既に存在する場合はスキップ
- **エラー耐性**: マイグレーションでエラーが発生してもアプリケーションは起動を継続

### 3. ビジネスロジックの更新 (`app/blueprints/system_admin.py`)

#### 新規関数: `can_access_tenant(tenant_id)`
システム管理者が指定されたテナントにアクセスできるかどうかを判定：

**アクセス可能な条件**:
1. 全テナント管理権限を持つシステム管理者（`can_manage_all_tenants=1`）
2. オーナー権限を持つシステム管理者（`is_owner=1`）※後方互換性
3. 自分で作成したテナント（`created_by_admin_id`）
4. 招待されたテナント（中間テーブル）

#### システム管理者新規作成 (`system_admin_new`)
- フォームから`can_manage_all_tenants`の値を取得
- 最初のシステム管理者は自動的に全権限を付与
- 2人目以降はフォームの設定に従う

#### システム管理者編集 (`system_admin_edit`)
- フォームから`can_manage_all_tenants`の値を取得
- オーナーでない場合のみ権限を変更可能
- `hasattr()`で後方互換性を確保

### 4. UIテンプレートの更新

#### `sys_system_admin_new.html`
- 「全テナント管理権限」チェックボックスを追加
- オーナーの場合は自動的にチェックされ、無効化

#### `sys_system_admin_edit.html`
- 「全テナント管理権限」チェックボックスを追加
- オーナーの場合は自動的にチェックされ、無効化
- 現在の設定値を表示

### 5. アプリケーション起動時の統合 (`app/__init__.py`)

```python
# ログインシステムの自動マイグレーション実行
try:
    from .auto_migrations import run_auto_migrations
    run_auto_migrations()
    print("✅ ログインシステム自動マイグレーション完了")
except Exception as e:
    print(f"⚠️ ログインシステム自動マイグレーションエラー: {e}")
```

データベース初期化後、ブループリント登録前に自動マイグレーションが実行されます。

## アクセス制御ロジック

### システム管理者のテナントアクセス権限

```
全テナント管理権限あり (can_manage_all_tenants=1)
  → 全てのテナントにアクセス可能

オーナー権限あり (is_owner=1)
  → 全てのテナントにアクセス可能（後方互換性）

上記以外
  → 自分で作成したテナント + 招待されたテナントのみアクセス可能
```

### 権限の優先順位

1. **オーナー権限** (`is_owner=1`)
   - 最高権限
   - 全ての設定を変更可能
   - 全テナントにアクセス可能

2. **全テナント管理権限** (`can_manage_all_tenants=1`)
   - 全テナントにアクセス可能
   - オーナーでない場合は権限変更可能

3. **システム管理者管理権限** (`can_manage_admins=1`)
   - 他のシステム管理者を管理可能
   - テナントアクセスは制限される場合あり

4. **通常のシステム管理者**
   - 自分で作成したテナントのみアクセス可能
   - 招待されたテナントにもアクセス可能

## 後方互換性

- 既存の`is_owner`権限は引き続き全テナントにアクセス可能
- `hasattr()`を使用してカラムの存在を確認
- マイグレーション実行前でも既存機能は動作

## マイグレーション実行

### 自動実行
アプリケーション起動時に自動的に実行されます。

### 手動実行（必要な場合）
```bash
cd /path/to/management-decision-app2
python3 -c "from app.auto_migrations import run_auto_migrations; run_auto_migrations()"
```

## デプロイ後の確認事項

1. ✅ Herokuログで自動マイグレーションの成功を確認
   ```
   自動マイグレーション開始... (データベース: postgresql)
   ✓ can_manage_all_tenants カラムを追加しました
   ✓ created_by_admin_id カラムを追加しました
   ✓ T_システム管理者_テナント テーブルを作成しました
   ✓ 自動マイグレーションが正常に完了しました
   ✅ ログインシステム自動マイグレーション完了
   ```

2. ✅ システム管理者のマイページが正常に表示される

3. ✅ システム管理者の新規作成画面で「全テナント管理権限」チェックボックスが表示される

4. ✅ システム管理者の編集画面で「全テナント管理権限」チェックボックスが表示される

5. ✅ 既存のシステム管理者のデフォルト値は`can_manage_all_tenants=0`となる

## 既存データへの影響

- **T_管理者**: `can_manage_all_tenants`カラムが追加され、既存レコードはデフォルト値0が設定される
- **T_テナント**: `created_by_admin_id`カラムが追加され、既存レコードはNULLが設定される
- **T_システム管理者_テナント**: 新規テーブルが作成される（既存データへの影響なし）

## 注意事項

1. **既存システム管理者の権限設定**
   - マイグレーション後、既存のシステム管理者は`can_manage_all_tenants=0`となります
   - 必要に応じて管理画面から権限を付与してください

2. **オーナー権限**
   - オーナー権限を持つシステム管理者は自動的に全テナントにアクセス可能です
   - オーナーの権限設定は変更できません

3. **テナント作成者**
   - 今後作成されるテナントには`created_by_admin_id`が自動的に設定されます
   - 既存のテナントは`created_by_admin_id=NULL`のままです

## 変更ファイル一覧

- `app/models_login.py` - モデル定義の更新
- `app/auto_migrations.py` - 自動マイグレーション機能（新規）
- `app/__init__.py` - 自動マイグレーションの統合
- `app/blueprints/system_admin.py` - ビジネスロジックの更新
- `app/templates/sys_system_admin_new.html` - 新規作成画面の更新
- `app/templates/sys_system_admin_edit.html` - 編集画面の更新

## 参考

- 同様の実装がaccounting-system-appでも完了しています
- login-system-appが最新のログインシステムの基準となっています
