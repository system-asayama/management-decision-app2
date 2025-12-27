"""
データベースモデル定義
経営意思決定支援システムのデータベーススキーマ
Node.js版（management-decision-making-app）の全テーブルをPythonに移植
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, Boolean, Enum as SQLEnum, JSON, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


# ==================== ユーザー管理 ====================

class UserRole(enum.Enum):
    """ユーザーロール"""
    USER = "user"
    ADMIN = "admin"


class User(Base):
    """ユーザーテーブル（Manus OAuth認証用）"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    open_id = Column(String(64), unique=True, nullable=False)
    name = Column(Text)
    email = Column(String(320))
    login_method = Column(String(64))
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    last_signed_in = Column(DateTime, default=datetime.now, nullable=False)


# ==================== 企業・会計年度 ====================

class Company(Base):
    """企業マスタ"""
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    industry = Column(String(100))  # 業種
    employee_count = Column(Integer)  # 従業員数
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    fiscal_years = relationship("FiscalYear", back_populates="company", cascade="all, delete-orphan")
    simulations = relationship("Simulation", back_populates="company", cascade="all, delete-orphan")
    loans = relationship("Loan", back_populates="company", cascade="all, delete-orphan")
    differential_analyses = relationship("DifferentialAnalysis", back_populates="company", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="company", cascade="all, delete-orphan")
    account_mappings = relationship("AccountMapping", back_populates="company", cascade="all, delete-orphan")


class FiscalYear(Base):
    """会計年度テーブル"""
    __tablename__ = 'fiscal_years'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    year = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    company = relationship("Company", back_populates="fiscal_years")
    profit_loss_statement = relationship("ProfitLossStatement", back_populates="fiscal_year", uselist=False, cascade="all, delete-orphan")
    balance_sheet = relationship("BalanceSheet", back_populates="fiscal_year", uselist=False, cascade="all, delete-orphan")
    restructured_pl = relationship("RestructuredPL", back_populates="fiscal_year", uselist=False, cascade="all, delete-orphan")
    restructured_bs = relationship("RestructuredBS", back_populates="fiscal_year", uselist=False, cascade="all, delete-orphan")
    labor_cost = relationship("LaborCost", back_populates="fiscal_year", uselist=False, cascade="all, delete-orphan")
    financial_indicators = relationship("FinancialIndicator", back_populates="fiscal_year", cascade="all, delete-orphan")
    business_segments = relationship("BusinessSegment", back_populates="fiscal_year", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="fiscal_year", cascade="all, delete-orphan")
    cash_flow_plans = relationship("CashFlowPlan", back_populates="fiscal_year", cascade="all, delete-orphan")
    labor_plans = relationship("LaborPlan", back_populates="fiscal_year", cascade="all, delete-orphan")
    capital_investment_plans = relationship("CapitalInvestmentPlan", back_populates="fiscal_year", cascade="all, delete-orphan")


# ==================== 財務諸表（簡易版） ====================

class ProfitLossStatement(Base):
    """損益計算書（簡易版）"""
    __tablename__ = 'profit_loss_statements'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    
    # 売上関連
    sales = Column(Integer, default=0, nullable=False)
    cost_of_sales = Column(Integer, default=0, nullable=False)
    gross_profit = Column(Integer, default=0, nullable=False)
    
    # 営業関連
    operating_expenses = Column(Integer, default=0, nullable=False)
    operating_income = Column(Integer, default=0, nullable=False)
    
    # 営業外
    non_operating_income = Column(Integer, default=0, nullable=False)
    non_operating_expenses = Column(Integer, default=0, nullable=False)
    ordinary_income = Column(Integer, default=0, nullable=False)
    
    # 特別損益
    extraordinary_income = Column(Integer, default=0, nullable=False)
    extraordinary_loss = Column(Integer, default=0, nullable=False)
    
    # 税引前・税引後
    income_before_tax = Column(Integer, default=0, nullable=False)
    income_tax = Column(Integer, default=0, nullable=False)
    net_income = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    fiscal_year = relationship("FiscalYear", back_populates="profit_loss_statement")


class BalanceSheet(Base):
    """貸借対照表（簡易版）"""
    __tablename__ = 'balance_sheets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    
    # 資産
    current_assets = Column(Integer, default=0, nullable=False)
    fixed_assets = Column(Integer, default=0, nullable=False)
    total_assets = Column(Integer, default=0, nullable=False)
    
    # 負債
    current_liabilities = Column(Integer, default=0, nullable=False)
    fixed_liabilities = Column(Integer, default=0, nullable=False)
    total_liabilities = Column(Integer, default=0, nullable=False)
    
    # 純資産
    capital = Column(Integer, default=0, nullable=False)
    retained_earnings = Column(Integer, default=0, nullable=False)
    total_equity = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    fiscal_year = relationship("FiscalYear", back_populates="balance_sheet")


# ==================== 財務諸表（組換え版） ====================

class RestructuredPL(Base):
    """組換え損益計算書（詳細版）"""
    __tablename__ = 'restructured_pl'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    
    # 売上高
    sales = Column(Integer, default=0, nullable=False)
    # 売上原価
    cost_of_sales = Column(Integer, default=0, nullable=False)
    # 売上総利益
    gross_profit = Column(Integer, default=0, nullable=False)
    # 販売費及び一般管理費
    selling_general_admin_expenses = Column(Integer, default=0, nullable=False)
    # 営業利益
    operating_income = Column(Integer, default=0, nullable=False)
    # 営業外収益
    non_operating_income = Column(Integer, default=0, nullable=False)
    # 営業外費用
    non_operating_expenses = Column(Integer, default=0, nullable=False)
    # 経常利益
    ordinary_income = Column(Integer, default=0, nullable=False)
    # 特別利益
    extraordinary_income = Column(Integer, default=0, nullable=False)
    # 特別損失
    extraordinary_loss = Column(Integer, default=0, nullable=False)
    # 税引前当期純利益
    income_before_tax = Column(Integer, default=0, nullable=False)
    # 法人税等
    income_taxes = Column(Integer, default=0, nullable=False)
    # 当期純利益
    net_income = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    fiscal_year = relationship("FiscalYear", back_populates="restructured_pl")


class RestructuredBS(Base):
    """組換え貸借対照表（詳細版）"""
    __tablename__ = 'restructured_bs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    
    # 流動資産
    current_assets = Column(Integer, default=0, nullable=False)
    # 固定資産
    fixed_assets = Column(Integer, default=0, nullable=False)
    # 資産合計
    total_assets = Column(Integer, default=0, nullable=False)
    # 流動負債
    current_liabilities = Column(Integer, default=0, nullable=False)
    # 固定負債
    fixed_liabilities = Column(Integer, default=0, nullable=False)
    # 負債合計
    total_liabilities = Column(Integer, default=0, nullable=False)
    # 純資産
    net_assets = Column(Integer, default=0, nullable=False)
    # 負債純資産合計
    total_liabilities_and_net_assets = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    fiscal_year = relationship("FiscalYear", back_populates="restructured_bs")


# ==================== 人件費・労務管理 ====================

class LaborCost(Base):
    """人件費データ"""
    __tablename__ = 'labor_costs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    employee_count = Column(Integer, default=0, nullable=False)
    total_salary = Column(Integer, default=0, nullable=False)
    bonus = Column(Integer, default=0, nullable=False)
    retirement_allowance = Column(Integer, default=0, nullable=False)
    statutory_welfare = Column(Integer, default=0, nullable=False)
    welfare_expenses = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    fiscal_year = relationship("FiscalYear", back_populates="labor_cost")


class LaborPlan(Base):
    """労務費管理計画（月次）"""
    __tablename__ = 'labor_plans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    
    # 計画値
    planned_headcount = Column(Integer, default=0, nullable=False)
    planned_average_salary = Column(Integer, default=0, nullable=False)
    planned_total_labor_cost = Column(Integer, default=0, nullable=False)
    planned_bonuses = Column(Integer, default=0, nullable=False)
    planned_social_insurance = Column(Integer, default=0, nullable=False)
    
    # 実績値
    actual_headcount = Column(Integer, default=0, nullable=False)
    actual_average_salary = Column(Integer, default=0, nullable=False)
    actual_total_labor_cost = Column(Integer, default=0, nullable=False)
    actual_bonuses = Column(Integer, default=0, nullable=False)
    actual_social_insurance = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    fiscal_year = relationship("FiscalYear", back_populates="labor_plans")


# ==================== 経営分析 ====================

class IndicatorType(enum.Enum):
    """財務指標タイプ"""
    GROWTH = "growth"  # 成長力
    PROFITABILITY = "profitability"  # 収益力
    LIQUIDITY = "liquidity"  # 資金力
    PRODUCTIVITY = "productivity"  # 生産力


class FinancialIndicator(Base):
    """財務指標データ"""
    __tablename__ = 'financial_indicators'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    indicator_type = Column(SQLEnum(IndicatorType), nullable=False)
    indicator_name = Column(String(255), nullable=False)
    value = Column(Text, nullable=False)
    unit = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    fiscal_year = relationship("FiscalYear", back_populates="financial_indicators")


class SegmentType(enum.Enum):
    """セグメントタイプ"""
    DEPARTMENT = "department"  # 部門
    PRODUCT = "product"  # 製品
    BUSINESS = "business"  # 事業
    REGION = "region"  # 地域


class BusinessSegment(Base):
    """事業セグメント（貢献度分析用）"""
    __tablename__ = 'business_segments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    segment_name = Column(String(255), nullable=False)
    segment_type = Column(SQLEnum(SegmentType), nullable=False)
    sales = Column(Integer, default=0, nullable=False)
    operating_income = Column(Integer, default=0, nullable=False)
    assets = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    fiscal_year = relationship("FiscalYear", back_populates="business_segments")


# ==================== 差額原価収益分析 ====================

class DifferentialAnalysis(Base):
    """差額原価収益分析マスタ"""
    __tablename__ = 'differential_analyses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    analysis_name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    company = relationship("Company", back_populates="differential_analyses")
    scenarios = relationship("DifferentialScenario", back_populates="analysis", cascade="all, delete-orphan")


class DifferentialScenario(Base):
    """差額原価収益分析シナリオ"""
    __tablename__ = 'differential_scenarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    analysis_id = Column(Integer, ForeignKey('differential_analyses.id'), nullable=False)
    scenario_name = Column(String(255), nullable=False)
    sales = Column(Integer, default=0, nullable=False)
    variable_costs = Column(Integer, default=0, nullable=False)
    fixed_costs = Column(Integer, default=0, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    analysis = relationship("DifferentialAnalysis", back_populates="scenarios")


# ==================== 予算・計画管理 ====================

class Budget(Base):
    """予算管理（月次）"""
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    
    # 予算
    budget_sales = Column(Integer, default=0, nullable=False)
    budget_cogs = Column(Integer, default=0, nullable=False)
    budget_sga = Column(Integer, default=0, nullable=False)
    
    # 実績
    actual_sales = Column(Integer, default=0, nullable=False)
    actual_cogs = Column(Integer, default=0, nullable=False)
    actual_sga = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    fiscal_year = relationship("FiscalYear", back_populates="budgets")


class CashFlowPlan(Base):
    """資金繰り計画（月次）"""
    __tablename__ = 'cash_flow_plans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    
    # 期首残高
    opening_balance = Column(Integer, default=0, nullable=False)
    
    # 収入計画
    planned_sales_receipts = Column(Integer, default=0, nullable=False)
    planned_other_receipts = Column(Integer, default=0, nullable=False)
    planned_total_receipts = Column(Integer, default=0, nullable=False)
    
    # 支出計画
    planned_purchase_payments = Column(Integer, default=0, nullable=False)
    planned_labor_costs = Column(Integer, default=0, nullable=False)
    planned_expenses = Column(Integer, default=0, nullable=False)
    planned_loan_repayments = Column(Integer, default=0, nullable=False)
    planned_other_payments = Column(Integer, default=0, nullable=False)
    planned_total_payments = Column(Integer, default=0, nullable=False)
    
    # 期末残高（計画）
    planned_closing_balance = Column(Integer, default=0, nullable=False)
    
    # 実績収入
    actual_sales_receipts = Column(Integer, default=0, nullable=False)
    actual_other_receipts = Column(Integer, default=0, nullable=False)
    actual_total_receipts = Column(Integer, default=0, nullable=False)
    
    # 実績支出
    actual_purchase_payments = Column(Integer, default=0, nullable=False)
    actual_labor_costs = Column(Integer, default=0, nullable=False)
    actual_expenses = Column(Integer, default=0, nullable=False)
    actual_loan_repayments = Column(Integer, default=0, nullable=False)
    actual_other_payments = Column(Integer, default=0, nullable=False)
    actual_total_payments = Column(Integer, default=0, nullable=False)
    
    # 期末残高（実績）
    actual_closing_balance = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    fiscal_year = relationship("FiscalYear", back_populates="cash_flow_plans")


class InvestmentStatus(enum.Enum):
    """設備投資ステータス"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CapitalInvestmentPlan(Base):
    """設備投資計画"""
    __tablename__ = 'capital_investment_plans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    investment_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    
    # 計画値
    planned_amount = Column(Integer, default=0, nullable=False)
    planned_start_date = Column(DateTime)
    planned_completion_date = Column(DateTime)
    expected_roi = Column(Numeric(5, 2), default=0.00)
    expected_payback_period = Column(Integer, default=0)
    
    # 実績値
    actual_amount = Column(Integer, default=0, nullable=False)
    actual_start_date = Column(DateTime)
    actual_completion_date = Column(DateTime)
    actual_roi = Column(Numeric(5, 2), default=0.00)
    
    # ステータス
    status = Column(SQLEnum(InvestmentStatus), default=InvestmentStatus.PLANNED, nullable=False)
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    fiscal_year = relationship("FiscalYear", back_populates="capital_investment_plans")


# ==================== 借入金管理 ====================

class Loan(Base):
    """借入金マスタ"""
    __tablename__ = 'loans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    loan_name = Column(String(255), nullable=False)
    lender = Column(String(255), nullable=False)
    loan_amount = Column(Integer, nullable=False)
    interest_rate = Column(Integer, nullable=False)  # 年利（%）を100倍した整数（例: 2.5% → 250）
    loan_date = Column(DateTime, nullable=False)
    repayment_start_date = Column(DateTime, nullable=False)
    repayment_end_date = Column(DateTime, nullable=False)
    monthly_repayment = Column(Integer, nullable=False)
    repayment_method = Column(String(50), nullable=False)  # 元利均等、元金均等など
    status = Column(String(50), default="active", nullable=False)  # active, completed
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    company = relationship("Company", back_populates="loans")
    repayments = relationship("LoanRepayment", back_populates="loan", cascade="all, delete-orphan")


class LoanRepayment(Base):
    """返済実績"""
    __tablename__ = 'loan_repayments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(Integer, ForeignKey('loans.id'), nullable=False)
    repayment_date = Column(DateTime, nullable=False)
    principal_amount = Column(Integer, nullable=False)
    interest_amount = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False)
    remaining_balance = Column(Integer, nullable=False)
    status = Column(String(50), default="scheduled", nullable=False)  # scheduled, paid
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    loan = relationship("Loan", back_populates="repayments")


# ==================== シミュレーション ====================

class Simulation(Base):
    """シミュレーション"""
    __tablename__ = 'simulations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    simulation_name = Column(String(255), nullable=False)
    base_fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    parameters = Column(Text)  # JSON形式でパラメータを保存
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    company = relationship("Company", back_populates="simulations")
    results = relationship("SimulationResult", back_populates="simulation", cascade="all, delete-orphan")


class SimulationResult(Base):
    """シミュレーション結果"""
    __tablename__ = 'simulation_results'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(Integer, ForeignKey('simulations.id'), nullable=False)
    year_offset = Column(Integer, nullable=False)  # 0, 1, 2（初年度、2年度、3年度）
    pl_data = Column(Text, nullable=False)  # JSON形式でP/Lデータを保存
    bs_data = Column(Text, nullable=False)  # JSON形式でB/Sデータを保存
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    simulation = relationship("Simulation", back_populates="results")


# ==================== その他 ====================

class NotificationType(enum.Enum):
    """通知タイプ"""
    CASH_SHORTAGE = "cash_shortage"
    FINANCIAL_INDICATOR_CHANGE = "financial_indicator_change"
    BUDGET_ALERT = "budget_alert"
    LOAN_ALERT = "loan_alert"


class NotificationSeverity(enum.Enum):
    """通知重要度"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Notification(Base):
    """通知"""
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    type = Column(SQLEnum(NotificationType), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(SQLEnum(NotificationSeverity), default=NotificationSeverity.INFO, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    related_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    company = relationship("Company", back_populates="notifications")


class StatementType(enum.Enum):
    """財務諸表タイプ"""
    PL = "PL"
    BS = "BS"


class AccountMapping(Base):
    """勘定科目マッピング（財務諸表組換え用）"""
    __tablename__ = 'account_mappings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    source_account = Column(String(255), nullable=False)  # 元の勘定科目名
    target_category = Column(String(100), nullable=False)  # 標準カテゴリ
    statement_type = Column(SQLEnum(StatementType), nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # リレーション
    company = relationship("Company", back_populates="account_mappings")
