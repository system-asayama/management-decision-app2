"""
資金繰り計画の月次データモデル
⑦初年度資金繰り計画、⑧2年度資金繰り計画、⑨3年度資金繰り計画
"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db import Base


class MonthlyCashFlowPlan(Base):
    """資金繰り計画の月次データ"""
    __tablename__ = 'monthly_cash_flow_plans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    fiscal_year_id = Column(Integer, ForeignKey('fiscal_years.id'), nullable=False)
    month = Column(Integer, nullable=False, comment='月（1〜12）')
    
    # 月初残高
    beginning_balance = Column(Numeric(15, 2), comment='月初残高')
    
    # （１）手許現預金
    cash = Column(Numeric(15, 2), comment='現金')
    ordinary_deposit_1 = Column(Numeric(15, 2), comment='普通預金1')
    ordinary_deposit_2 = Column(Numeric(15, 2), comment='普通預金2')
    ordinary_deposit_3 = Column(Numeric(15, 2), comment='普通預金3')
    cash_and_deposits_total = Column(Numeric(15, 2), comment='手許現預金計')
    
    # （２）運用預金
    time_deposit = Column(Numeric(15, 2), comment='定期預金')
    investment_deposits_total = Column(Numeric(15, 2), comment='運用預金計')
    
    # 収入
    cash_sales = Column(Numeric(15, 2), comment='現金売上')
    accounts_receivable_collection = Column(Numeric(15, 2), comment='売掛金回収')
    notes_receivable_collection = Column(Numeric(15, 2), comment='手形回収')
    notes_discount = Column(Numeric(15, 2), comment='手形割引')
    other_cash_income = Column(Numeric(15, 2), comment='その他現金収入')
    income_total = Column(Numeric(15, 2), comment='収入計')
    
    # 仕入
    cash_purchases = Column(Numeric(15, 2), comment='現金仕入')
    accounts_payable_payment = Column(Numeric(15, 2), comment='買掛金支払')
    notes_payable_payment = Column(Numeric(15, 2), comment='手形支払')
    other_cash_expenses = Column(Numeric(15, 2), comment='その他現金支出')
    purchases_total = Column(Numeric(15, 2), comment='仕入計')
    
    # 人件費
    executive_compensation = Column(Numeric(15, 2), comment='役員報酬')
    executive_statutory_welfare = Column(Numeric(15, 2), comment='役員法定福利費')
    executive_retirement = Column(Numeric(15, 2), comment='役員退職金')
    salaries = Column(Numeric(15, 2), comment='給料手当')
    temporary_wages = Column(Numeric(15, 2), comment='雑給')
    bonuses = Column(Numeric(15, 2), comment='賞与')
    employee_statutory_welfare = Column(Numeric(15, 2), comment='従業員法定福利費')
    employee_retirement = Column(Numeric(15, 2), comment='従業員退職金')
    welfare_expenses = Column(Numeric(15, 2), comment='福利厚生費')
    labor_cost_total = Column(Numeric(15, 2), comment='人件費計')
    
    # その他経費
    office_supplies = Column(Numeric(15, 2), comment='事務用品費')
    consumables = Column(Numeric(15, 2), comment='消耗品費')
    travel_expenses = Column(Numeric(15, 2), comment='旅費交通費')
    commission_fees = Column(Numeric(15, 2), comment='支払手数料')
    entertainment_expenses = Column(Numeric(15, 2), comment='接待交際費')
    insurance_premiums = Column(Numeric(15, 2), comment='支払保険料')
    communication_expenses = Column(Numeric(15, 2), comment='通信費')
    membership_fees = Column(Numeric(15, 2), comment='諸会費')
    vehicle_expenses = Column(Numeric(15, 2), comment='車両費')
    books_and_publications = Column(Numeric(15, 2), comment='新聞図書費')
    advertising_expenses = Column(Numeric(15, 2), comment='広告宣伝費')
    utilities = Column(Numeric(15, 2), comment='水道光熱費')
    rent = Column(Numeric(15, 2), comment='地代家賃')
    repairs = Column(Numeric(15, 2), comment='修繕費')
    lease_expenses = Column(Numeric(15, 2), comment='賃借料(リース料）')
    miscellaneous_expenses = Column(Numeric(15, 2), comment='雑費')
    other_expenses_total = Column(Numeric(15, 2), comment='その他経費計')
    
    # 経費以外支出
    marketable_securities = Column(Numeric(15, 2), comment='有価証券')
    tangible_fixed_assets = Column(Numeric(15, 2), comment='有形固定資産')
    intangible_fixed_assets = Column(Numeric(15, 2), comment='無形固定資産')
    investments_and_other_assets = Column(Numeric(15, 2), comment='投資その他の資産')
    deferred_assets = Column(Numeric(15, 2), comment='繰延資産')
    non_operating_expenses_total = Column(Numeric(15, 2), comment='経費以外支出計')
    
    # 支出計
    expenses_total = Column(Numeric(15, 2), comment='支出計')
    
    # 差引計（収入－支出）
    net_cash_flow = Column(Numeric(15, 2), comment='差引計（収入－支出）')
    
    # ①月末残高
    ending_balance = Column(Numeric(15, 2), comment='①月末残高')
    
    # ②月末残高－主要運転資金計画
    ending_balance_minus_working_capital = Column(Numeric(15, 2), comment='②月末残高－主要運転資金計画')
    
    # （１）手許現預金（月末）
    ending_cash = Column(Numeric(15, 2), comment='現金（月末）')
    ending_ordinary_deposit_1 = Column(Numeric(15, 2), comment='普通預金1（月末）')
    ending_ordinary_deposit_2 = Column(Numeric(15, 2), comment='普通預金2（月末）')
    ending_ordinary_deposit_3 = Column(Numeric(15, 2), comment='普通預金3（月末）')
    ending_cash_and_deposits_total = Column(Numeric(15, 2), comment='手許現預金計（月末）')
    
    # （２）運用預金（月末）
    ending_time_deposit = Column(Numeric(15, 2), comment='定期預金（月末）')
    ending_investment_deposits_total = Column(Numeric(15, 2), comment='運用預金計（月末）')
    
    created_at = Column(DateTime, server_default=func.now(), comment='作成日時')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新日時')
    
    def __repr__(self):
        return f"<MonthlyCashFlowPlan(id={self.id}, company_id={self.company_id}, fiscal_year_id={self.fiscal_year_id}, month={self.month})>"
