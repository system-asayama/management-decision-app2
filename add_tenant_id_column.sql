-- companiesテーブルにtenant_idカラムを追加
ALTER TABLE companies ADD COLUMN IF NOT EXISTS tenant_id INTEGER NOT NULL DEFAULT 1;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS capital INTEGER;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS established_date DATE;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS address TEXT;
ALTER TABLE companies ADD COLUMN IF NOT EXISTS phone VARCHAR(20);
ALTER TABLE companies ADD COLUMN IF NOT EXISTS email VARCHAR(320);
ALTER TABLE companies ADD COLUMN IF NOT EXISTS website VARCHAR(500);
ALTER TABLE companies ADD COLUMN IF NOT EXISTS notes TEXT;

-- fiscal_yearsテーブルのカラムを修正
ALTER TABLE fiscal_years ADD COLUMN IF NOT EXISTS year_name VARCHAR(100);
ALTER TABLE fiscal_years ADD COLUMN IF NOT EXISTS months INTEGER DEFAULT 12;
ALTER TABLE fiscal_years ADD COLUMN IF NOT EXISTS notes TEXT;
ALTER TABLE fiscal_years ALTER COLUMN start_date TYPE DATE;
ALTER TABLE fiscal_years ALTER COLUMN end_date TYPE DATE;

-- インデックスを追加
CREATE INDEX IF NOT EXISTS idx_companies_tenant_id ON companies(tenant_id);

SELECT 'テーブル修正完了' AS result;
