"""
財務管理UI Blueprint
財務データ入力、経営分析、シミュレーションのWebインターフェースを提供
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.db import SessionLocal
from app.models_decision import Company, FiscalYear, ProfitLossStatement, BalanceSheet
from functools import wraps

financial_ui_bp = Blueprint('financial_ui', __name__, url_prefix='/financial')


def login_required(f):
    """ログイン必須デコレータ"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('ログインが必要です', 'warning')
            return redirect(url_for('auth.staff_login'))
        return f(*args, **kwargs)
    return decorated_function


@financial_ui_bp.route('/dashboard')
@login_required
def dashboard():
    """財務管理ダッシュボード"""
    db = SessionLocal()
    try:
        # 企業一覧を取得
        companies = db.query(Company).all()
        
        # 選択された企業
        company_id = request.args.get('company_id', type=int)
        selected_company = None
        summary = None
        comparison_data = None
        indicators = None
        
        if company_id:
            selected_company = db.query(Company).filter(Company.id == company_id).first()
            
            if selected_company:
                # 最新の会計年度を取得
                latest_fiscal_year = db.query(FiscalYear).filter(
                    FiscalYear.company_id == company_id
                ).order_by(FiscalYear.start_date.desc()).first()
                
                if latest_fiscal_year:
                    # P/Lデータ
                    pl = db.query(ProfitLossStatement).filter(
                        ProfitLossStatement.fiscal_year_id == latest_fiscal_year.id
                    ).first()
                    
                    # B/Sデータ
                    bs = db.query(BalanceSheet).filter(
                        BalanceSheet.fiscal_year_id == latest_fiscal_year.id
                    ).first()
                    
                    if pl and bs:
                        summary = {
                            'sales': pl.sales,
                            'ordinary_income': pl.ordinary_income,
                            'total_assets': bs.total_assets,
                            'net_assets': bs.total_equity,
                            'total_liabilities': bs.total_liabilities,
                            'equity_ratio': (bs.total_equity / bs.total_assets * 100) if bs.total_assets > 0 else 0,
                            'roa': (pl.ordinary_income / bs.total_assets * 100) if bs.total_assets > 0 else 0,
                            'profit_margin': (pl.ordinary_income / pl.sales * 100) if pl.sales > 0 else 0
                        }
                        
                        # 簡易的な経営指標
                        indicators = {
                            'roa': summary['roa'],
                            'roe': (pl.ordinary_income / bs.total_equity * 100) if bs.total_equity > 0 else 0,
                            'operating_margin': (pl.operating_income / pl.sales * 100) if pl.sales > 0 else 0,
                            'current_ratio': (bs.current_assets / bs.current_liabilities * 100) if bs.current_liabilities > 0 else 0,
                            'quick_ratio': ((bs.current_assets * 0.7) / bs.current_liabilities * 100) if bs.current_liabilities > 0 else 0,
                            'debt_ratio': (bs.total_liabilities / bs.total_assets * 100) if bs.total_assets > 0 else 0
                        }
                
                # 複数年度比較データ
                fiscal_years = db.query(FiscalYear).filter(
                    FiscalYear.company_id == company_id
                ).order_by(FiscalYear.start_date.desc()).limit(3).all()
                
                if fiscal_years:
                    years = []
                    sales_data = []
                    income_data = []
                    
                    for fy in reversed(fiscal_years):
                        pl = db.query(ProfitLossStatement).filter(
                            ProfitLossStatement.fiscal_year_id == fy.id
                        ).first()
                        
                        if pl:
                            years.append(fy.year_name)
                            sales_data.append(pl.sales / 1000000)  # 百万円単位
                            income_data.append(pl.ordinary_income / 1000000)
                    
                    comparison_data = {
                        'years': years,
                        'sales': sales_data,
                        'ordinary_income': income_data
                    }
        
        return render_template(
            'financial_dashboard.html',
            companies=companies,
            selected_company=selected_company,
            summary=summary,
            comparison_data=comparison_data,
            indicators=indicators
        )
    finally:
        db.close()


@financial_ui_bp.route('/companies')
@login_required
def companies():
    """企業一覧"""
    db = SessionLocal()
    try:
        companies = db.query(Company).all()
        return render_template('financial_companies.html', companies=companies)
    finally:
        db.close()


@financial_ui_bp.route('/companies/new', methods=['GET', 'POST'])
@login_required
def company_new():
    """企業新規登録"""
    if request.method == 'POST':
        db = SessionLocal()
        try:
            company = Company(
                name=request.form['name'],
                industry=request.form.get('industry'),
                employee_count=int(request.form.get('employee_count', 0))
            )
            db.add(company)
            db.commit()
            flash('企業を登録しました', 'success')
            return redirect(url_for('financial_ui.companies'))
        except Exception as e:
            db.rollback()
            flash(f'エラーが発生しました: {str(e)}', 'danger')
        finally:
            db.close()
    
    return render_template('financial_company_form.html')


@financial_ui_bp.route('/fiscal-years')
@login_required
def fiscal_years():
    """会計年度一覧"""
    company_id = request.args.get('company_id', type=int)
    
    db = SessionLocal()
    try:
        companies = db.query(Company).all()
        selected_company = None
        fiscal_years = []
        
        if company_id:
            selected_company = db.query(Company).filter(Company.id == company_id).first()
            fiscal_years = db.query(FiscalYear).filter(
                FiscalYear.company_id == company_id
            ).order_by(FiscalYear.start_date.desc()).all()
        
        return render_template(
            'financial_fiscal_years.html',
            companies=companies,
            selected_company=selected_company,
            fiscal_years=fiscal_years
        )
    finally:
        db.close()


@financial_ui_bp.route('/pl-input')
@login_required
def pl_input():
    """損益計算書入力"""
    company_id = request.args.get('company_id', type=int)
    fiscal_year_id = request.args.get('fiscal_year_id', type=int)
    
    db = SessionLocal()
    try:
        companies = db.query(Company).all()
        selected_company = None
        fiscal_years = []
        pl_data = None
        
        if company_id:
            selected_company = db.query(Company).filter(Company.id == company_id).first()
            fiscal_years = db.query(FiscalYear).filter(
                FiscalYear.company_id == company_id
            ).order_by(FiscalYear.start_date.desc()).all()
            
            if fiscal_year_id:
                pl_data = db.query(ProfitLossStatement).filter(
                    ProfitLossStatement.fiscal_year_id == fiscal_year_id
                ).first()
        
        return render_template(
            'financial_pl_input.html',
            companies=companies,
            selected_company=selected_company,
            fiscal_years=fiscal_years,
            fiscal_year_id=fiscal_year_id,
            pl_data=pl_data
        )
    finally:
        db.close()


@financial_ui_bp.route('/bs-input')
@login_required
def bs_input():
    """貸借対照表入力"""
    company_id = request.args.get('company_id', type=int)
    fiscal_year_id = request.args.get('fiscal_year_id', type=int)
    
    db = SessionLocal()
    try:
        companies = db.query(Company).all()
        selected_company = None
        fiscal_years = []
        bs_data = None
        
        if company_id:
            selected_company = db.query(Company).filter(Company.id == company_id).first()
            fiscal_years = db.query(FiscalYear).filter(
                FiscalYear.company_id == company_id
            ).order_by(FiscalYear.start_date.desc()).all()
            
            if fiscal_year_id:
                bs_data = db.query(BalanceSheet).filter(
                    BalanceSheet.fiscal_year_id == fiscal_year_id
                ).first()
        
        return render_template(
            'financial_bs_input.html',
            companies=companies,
            selected_company=selected_company,
            fiscal_years=fiscal_years,
            fiscal_year_id=fiscal_year_id,
            bs_data=bs_data
        )
    finally:
        db.close()


@financial_ui_bp.route('/analysis')
@login_required
def analysis():
    """経営分析"""
    company_id = request.args.get('company_id', type=int)
    
    db = SessionLocal()
    try:
        companies = db.query(Company).all()
        selected_company = None
        
        if company_id:
            selected_company = db.query(Company).filter(Company.id == company_id).first()
        
        return render_template(
            'financial_analysis.html',
            companies=companies,
            selected_company=selected_company
        )
    finally:
        db.close()


@financial_ui_bp.route('/simulation')
@login_required
def simulation():
    """シミュレーション"""
    company_id = request.args.get('company_id', type=int)
    
    db = SessionLocal()
    try:
        companies = db.query(Company).all()
        selected_company = None
        
        if company_id:
            selected_company = db.query(Company).filter(Company.id == company_id).first()
        
        return render_template(
            'financial_simulation.html',
            companies=companies,
            selected_company=selected_company
        )
    finally:
        db.close()
