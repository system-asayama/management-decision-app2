"""
経営意思決定アプリ - メインBlueprint
"""

from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from ..utils.decorators import require_roles, ROLES
from ..db import SessionLocal
from ..models_decision import Company, FiscalYear
from datetime import datetime

bp = Blueprint('decision', __name__, url_prefix='/decision')


@bp.route('/')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def index():
    """経営意思決定アプリのトップページ"""
    tenant_id = session.get('tenant_id')
    
    if not tenant_id:
        return render_template('decision_no_tenant.html')
    
    return render_template('decision_index.html', tenant_id=tenant_id)


@bp.route('/dashboard')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def dashboard():
    """経営意思決定ダッシュボード"""
    tenant_id = session.get('tenant_id')
    
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    return render_template('decision_dashboard.html', tenant_id=tenant_id)


# ============================================================
# 企業管理ルート
# ============================================================

@bp.route('/companies')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def company_list():
    """企業一覧ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        return render_template('company_list.html', companies=companies)
    finally:
        db.close()


@bp.route('/companies/new', methods=['GET', 'POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def company_new():
    """企業登録ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    if request.method == 'POST':
        db = SessionLocal()
        try:
            company = Company(
                tenant_id=tenant_id,
                name=request.form.get('name'),
                industry=request.form.get('industry') or None,
                capital=int(request.form.get('capital')) if request.form.get('capital') else None,
                employee_count=int(request.form.get('employee_count')) if request.form.get('employee_count') else None,
                established_date=datetime.strptime(request.form.get('established_date'), '%Y-%m-%d').date() if request.form.get('established_date') else None,
                address=request.form.get('address') or None,
                phone=request.form.get('phone') or None,
                email=request.form.get('email') or None,
                website=request.form.get('website') or None,
                notes=request.form.get('notes') or None
            )
            db.add(company)
            db.commit()
            return redirect(url_for('decision.company_list'))
        except Exception as e:
            db.rollback()
            return render_template('company_form.html', error=str(e))
        finally:
            db.close()
    
    return render_template('company_form.html')


@bp.route('/companies/<int:company_id>/edit', methods=['GET', 'POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def company_edit(company_id):
    """企業編集ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return redirect(url_for('decision.company_list'))
        
        if request.method == 'POST':
            try:
                company.name = request.form.get('name')
                company.industry = request.form.get('industry') or None
                company.capital = int(request.form.get('capital')) if request.form.get('capital') else None
                company.employee_count = int(request.form.get('employee_count')) if request.form.get('employee_count') else None
                company.established_date = datetime.strptime(request.form.get('established_date'), '%Y-%m-%d').date() if request.form.get('established_date') else None
                company.address = request.form.get('address') or None
                company.phone = request.form.get('phone') or None
                company.email = request.form.get('email') or None
                company.website = request.form.get('website') or None
                company.notes = request.form.get('notes') or None
                db.commit()
                return redirect(url_for('decision.company_list'))
            except Exception as e:
                db.rollback()
                return render_template('company_form.html', company=company, error=str(e))
        
        return render_template('company_form.html', company=company)
    finally:
        db.close()


@bp.route('/companies/<int:company_id>', methods=['DELETE'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def company_delete(company_id):
    """企業削除API"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'success': False, 'error': 'テナントIDが設定されていません'}), 400
    
    db = SessionLocal()
    try:
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'success': False, 'error': '企業が見つかりません'}), 404
        
        db.delete(company)
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()


# ============================================================
# 会計年度管理ルート
# ============================================================

@bp.route('/fiscal-years')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def fiscal_year_list():
    """会計年度一覧ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        fiscal_years = db.query(FiscalYear).join(Company).filter(
            Company.tenant_id == tenant_id
        ).all()
        return render_template('fiscal_year_list.html', fiscal_years=fiscal_years)
    finally:
        db.close()


@bp.route('/fiscal-years/new', methods=['GET', 'POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def fiscal_year_new():
    """会計年度登録ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        
        if request.method == 'POST':
            try:
                fiscal_year = FiscalYear(
                    company_id=int(request.form.get('company_id')),
                    year_name=request.form.get('year_name'),
                    start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date(),
                    end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date(),
                    months=int(request.form.get('months')) if request.form.get('months') else 12,
                    notes=request.form.get('notes') or None
                )
                db.add(fiscal_year)
                db.commit()
                return redirect(url_for('decision.fiscal_year_list'))
            except Exception as e:
                db.rollback()
                return render_template('fiscal_year_form.html', companies=companies, error=str(e))
        
        return render_template('fiscal_year_form.html', companies=companies)
    finally:
        db.close()


@bp.route('/fiscal-years/<int:fiscal_year_id>/edit', methods=['GET', 'POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def fiscal_year_edit(fiscal_year_id):
    """会計年度編集ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        fiscal_year = db.query(FiscalYear).join(Company).filter(
            FiscalYear.id == fiscal_year_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not fiscal_year:
            return redirect(url_for('decision.fiscal_year_list'))
        
        if request.method == 'POST':
            try:
                fiscal_year.company_id = int(request.form.get('company_id'))
                fiscal_year.year_name = request.form.get('year_name')
                fiscal_year.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
                fiscal_year.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
                fiscal_year.months = int(request.form.get('months')) if request.form.get('months') else 12
                fiscal_year.notes = request.form.get('notes') or None
                db.commit()
                return redirect(url_for('decision.fiscal_year_list'))
            except Exception as e:
                db.rollback()
                return render_template('fiscal_year_form.html', companies=companies, fiscal_year=fiscal_year, error=str(e))
        
        return render_template('fiscal_year_form.html', companies=companies, fiscal_year=fiscal_year)
    finally:
        db.close()


@bp.route('/fiscal-years/<int:fiscal_year_id>', methods=['DELETE'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def fiscal_year_delete(fiscal_year_id):
    """会計年度削除API"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'success': False, 'error': 'テナントIDが設定されていません'}), 400
    
    db = SessionLocal()
    try:
        fiscal_year = db.query(FiscalYear).join(Company).filter(
            FiscalYear.id == fiscal_year_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not fiscal_year:
            return jsonify({'success': False, 'error': '会計年度が見つかりません'}), 404
        
        db.delete(fiscal_year)
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()


# ==================== 損益計算書管理 ====================

@bp.route('/profit-loss')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"], ROLES["EMPLOYEE"])
def profit_loss_list():
    """損益計算書一覧ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return render_template('decision_no_tenant.html')
    
    db = SessionLocal()
    try:
        from app.models_decision import ProfitLossStatement
        profit_loss_statements = db.query(ProfitLossStatement).join(FiscalYear).join(Company).filter(
            Company.tenant_id == tenant_id
        ).all()
        return render_template('profit_loss_list.html', profit_loss_statements=profit_loss_statements)
    finally:
        db.close()


@bp.route('/profit-loss/new', methods=['GET', 'POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"])
def profit_loss_new():
    """損益計算書新規登録ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return render_template('decision_no_tenant.html')
    
    db = SessionLocal()
    try:
        from app.models_decision import ProfitLossStatement
        
        # 会計年度一覧を取得
        fiscal_years = db.query(FiscalYear).join(Company).filter(
            Company.tenant_id == tenant_id
        ).all()
        
        if request.method == 'POST':
            try:
                profit_loss = ProfitLossStatement(
                    fiscal_year_id=int(request.form.get('fiscal_year_id')),
                    sales=int(request.form.get('sales') or 0),
                    cost_of_sales=int(request.form.get('cost_of_sales') or 0),
                    gross_profit=int(request.form.get('gross_profit') or 0),
                    operating_expenses=int(request.form.get('operating_expenses') or 0),
                    operating_income=int(request.form.get('operating_income') or 0),
                    non_operating_income=int(request.form.get('non_operating_income') or 0),
                    non_operating_expenses=int(request.form.get('non_operating_expenses') or 0),
                    ordinary_income=int(request.form.get('ordinary_income') or 0),
                    extraordinary_income=int(request.form.get('extraordinary_income') or 0),
                    extraordinary_loss=int(request.form.get('extraordinary_loss') or 0),
                    income_before_tax=int(request.form.get('income_before_tax') or 0),
                    income_tax=int(request.form.get('income_tax') or 0),
                    net_income=int(request.form.get('net_income') or 0)
                )
                db.add(profit_loss)
                db.commit()
                return redirect(url_for('decision.profit_loss_list'))
            except Exception as e:
                db.rollback()
                return render_template('profit_loss_form.html', fiscal_years=fiscal_years, error=str(e))
        
        return render_template('profit_loss_form.html', fiscal_years=fiscal_years, profit_loss=None)
    finally:
        db.close()


@bp.route('/profit-loss/<int:id>/edit', methods=['GET', 'POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"])
def profit_loss_edit(id):
    """損益計算書編集ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return render_template('decision_no_tenant.html')
    
    db = SessionLocal()
    try:
        from app.models_decision import ProfitLossStatement
        
        # 会計年度一覧を取得
        fiscal_years = db.query(FiscalYear).join(Company).filter(
            Company.tenant_id == tenant_id
        ).all()
        
        # 損益計算書を取得
        profit_loss = db.query(ProfitLossStatement).join(FiscalYear).join(Company).filter(
            ProfitLossStatement.id == id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not profit_loss:
            return redirect(url_for('decision.profit_loss_list'))
        
        if request.method == 'POST':
            try:
                profit_loss.fiscal_year_id = int(request.form.get('fiscal_year_id'))
                profit_loss.sales = int(request.form.get('sales') or 0)
                profit_loss.cost_of_sales = int(request.form.get('cost_of_sales') or 0)
                profit_loss.gross_profit = int(request.form.get('gross_profit') or 0)
                profit_loss.operating_expenses = int(request.form.get('operating_expenses') or 0)
                profit_loss.operating_income = int(request.form.get('operating_income') or 0)
                profit_loss.non_operating_income = int(request.form.get('non_operating_income') or 0)
                profit_loss.non_operating_expenses = int(request.form.get('non_operating_expenses') or 0)
                profit_loss.ordinary_income = int(request.form.get('ordinary_income') or 0)
                profit_loss.extraordinary_income = int(request.form.get('extraordinary_income') or 0)
                profit_loss.extraordinary_loss = int(request.form.get('extraordinary_loss') or 0)
                profit_loss.income_before_tax = int(request.form.get('income_before_tax') or 0)
                profit_loss.income_tax = int(request.form.get('income_tax') or 0)
                profit_loss.net_income = int(request.form.get('net_income') or 0)
                db.commit()
                return redirect(url_for('decision.profit_loss_list'))
            except Exception as e:
                db.rollback()
                return render_template('profit_loss_form.html', fiscal_years=fiscal_years, profit_loss=profit_loss, error=str(e))
        
        return render_template('profit_loss_form.html', fiscal_years=fiscal_years, profit_loss=profit_loss)
    finally:
        db.close()


@bp.route('/profit-loss/<int:id>', methods=['DELETE'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"])
def profit_loss_delete(id):
    """損益計算書削除API"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'success': False, 'error': 'テナントIDが設定されていません'}), 400
    
    db = SessionLocal()
    try:
        from app.models_decision import ProfitLossStatement
        
        profit_loss = db.query(ProfitLossStatement).join(FiscalYear).join(Company).filter(
            ProfitLossStatement.id == id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not profit_loss:
            return jsonify({'success': False, 'error': '損益計算書が見つかりません'}), 404
        
        db.delete(profit_loss)
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()


# ==================== 貸借対照表管理 ====================

@bp.route('/balance-sheets')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"], ROLES["EMPLOYEE"])
def balance_sheet_list():
    """貸借対照表一覧ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return render_template('decision_no_tenant.html')
    
    db = SessionLocal()
    try:
        from app.models_decision import BalanceSheet
        balance_sheets = db.query(BalanceSheet).join(FiscalYear).join(Company).filter(
            Company.tenant_id == tenant_id
        ).all()
        return render_template('balance_sheet_list.html', balance_sheets=balance_sheets)
    finally:
        db.close()


@bp.route('/balance-sheets/new', methods=['GET', 'POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"])
def balance_sheet_new():
    """貸借対照表新規登録ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return render_template('decision_no_tenant.html')
    
    db = SessionLocal()
    try:
        from app.models_decision import BalanceSheet
        
        # 会計年度一覧を取得
        fiscal_years = db.query(FiscalYear).join(Company).filter(
            Company.tenant_id == tenant_id
        ).all()
        
        if request.method == 'POST':
            try:
                balance_sheet = BalanceSheet(
                    fiscal_year_id=int(request.form.get('fiscal_year_id')),
                    current_assets=int(request.form.get('current_assets') or 0),
                    fixed_assets=int(request.form.get('fixed_assets') or 0),
                    total_assets=int(request.form.get('total_assets') or 0),
                    current_liabilities=int(request.form.get('current_liabilities') or 0),
                    fixed_liabilities=int(request.form.get('fixed_liabilities') or 0),
                    total_liabilities=int(request.form.get('total_liabilities') or 0),
                    capital=int(request.form.get('capital') or 0),
                    retained_earnings=int(request.form.get('retained_earnings') or 0),
                    total_equity=int(request.form.get('total_equity') or 0)
                )
                db.add(balance_sheet)
                db.commit()
                return redirect(url_for('decision.balance_sheet_list'))
            except Exception as e:
                db.rollback()
                return render_template('balance_sheet_form.html', fiscal_years=fiscal_years, error=str(e))
        
        return render_template('balance_sheet_form.html', fiscal_years=fiscal_years, balance_sheet=None)
    finally:
        db.close()


@bp.route('/balance-sheets/<int:id>/edit', methods=['GET', 'POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"])
def balance_sheet_edit(id):
    """貸借対照表編集ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return render_template('decision_no_tenant.html')
    
    db = SessionLocal()
    try:
        from app.models_decision import BalanceSheet
        
        # 会計年度一覧を取得
        fiscal_years = db.query(FiscalYear).join(Company).filter(
            Company.tenant_id == tenant_id
        ).all()
        
        # 貸借対照表を取得
        balance_sheet = db.query(BalanceSheet).join(FiscalYear).join(Company).filter(
            BalanceSheet.id == id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not balance_sheet:
            return redirect(url_for('decision.balance_sheet_list'))
        
        if request.method == 'POST':
            try:
                balance_sheet.fiscal_year_id = int(request.form.get('fiscal_year_id'))
                balance_sheet.current_assets = int(request.form.get('current_assets') or 0)
                balance_sheet.fixed_assets = int(request.form.get('fixed_assets') or 0)
                balance_sheet.total_assets = int(request.form.get('total_assets') or 0)
                balance_sheet.current_liabilities = int(request.form.get('current_liabilities') or 0)
                balance_sheet.fixed_liabilities = int(request.form.get('fixed_liabilities') or 0)
                balance_sheet.total_liabilities = int(request.form.get('total_liabilities') or 0)
                balance_sheet.capital = int(request.form.get('capital') or 0)
                balance_sheet.retained_earnings = int(request.form.get('retained_earnings') or 0)
                balance_sheet.total_equity = int(request.form.get('total_equity') or 0)
                db.commit()
                return redirect(url_for('decision.balance_sheet_list'))
            except Exception as e:
                db.rollback()
                return render_template('balance_sheet_form.html', fiscal_years=fiscal_years, balance_sheet=balance_sheet, error=str(e))
        
        return render_template('balance_sheet_form.html', fiscal_years=fiscal_years, balance_sheet=balance_sheet)
    finally:
        db.close()


@bp.route('/balance-sheets/<int:id>', methods=['DELETE'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"])
def balance_sheet_delete(id):
    """貸借対照表削除API"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'success': False, 'error': 'テナントIDが設定されていません'}), 400
    
    db = SessionLocal()
    try:
        from app.models_decision import BalanceSheet
        
        balance_sheet = db.query(BalanceSheet).join(FiscalYear).join(Company).filter(
            BalanceSheet.id == id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not balance_sheet:
            return jsonify({'success': False, 'error': '貸借対照表が見つかりません'}), 404
        
        db.delete(balance_sheet)
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()


# ==================== ダッシュボード ====================

@bp.route('/dashboard-analysis')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"], ROLES["EMPLOYEE"])
def dashboard_analysis():
    """ダッシュボード分析ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return render_template('decision_no_tenant.html')
    
    db = SessionLocal()
    try:
        # 企業一覧を取得
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        return render_template('dashboard_analysis.html', companies=companies)
    finally:
        db.close()


@bp.route('/dashboard-analysis/data/<int:company_id>/<int:fiscal_year_id>')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"], ROLES["EMPLOYEE"])
def dashboard_analysis_data(company_id, fiscal_year_id):
    """ダッシュボード分析データAPI"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'success': False, 'error': 'テナントIDが設定されていません'}), 400
    
    db = SessionLocal()
    try:
        from app.models_decision import ProfitLossStatement, BalanceSheet
        from app.utils.financial_calculator import calculate_all_ratios, get_ratio_status
        
        # 会計年度を確認
        fiscal_year = db.query(FiscalYear).join(Company).filter(
            FiscalYear.id == fiscal_year_id,
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not fiscal_year:
            return jsonify({'success': False, 'error': '会計年度が見つかりません'}), 404
        
        # 損益計算書を取得
        profit_loss = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == fiscal_year_id
        ).first()
        
        # 貸借対照表を取得
        balance_sheet = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not profit_loss or not balance_sheet:
            return jsonify({
                'success': False,
                'error': '損益計算書または貸借対照表が登録されていません'
            }), 404
        
        # 財務指標を計算
        ratios = calculate_all_ratios(profit_loss, balance_sheet)
        
        # 各指標の状態を判定
        ratios_with_status = {}
        for category, indicators in ratios.items():
            ratios_with_status[category] = {}
            for name, value in indicators.items():
                ratios_with_status[category][name] = {
                    'value': value,
                    'status': get_ratio_status(name, value)
                }
        
        return jsonify({
            'success': True,
            'company_name': fiscal_year.company.name,
            'fiscal_year_name': fiscal_year.year_name,
            'profit_loss': {
                'sales': profit_loss.sales,
                'cost_of_sales': profit_loss.cost_of_sales,
                'gross_profit': profit_loss.gross_profit,
                'operating_expenses': profit_loss.operating_expenses,
                'operating_income': profit_loss.operating_income,
                'ordinary_income': profit_loss.ordinary_income,
                'net_income': profit_loss.net_income
            },
            'balance_sheet': {
                'current_assets': balance_sheet.current_assets,
                'fixed_assets': balance_sheet.fixed_assets,
                'total_assets': balance_sheet.total_assets,
                'current_liabilities': balance_sheet.current_liabilities,
                'fixed_liabilities': balance_sheet.fixed_liabilities,
                'total_liabilities': balance_sheet.total_liabilities,
                'total_equity': balance_sheet.total_equity
            },
            'ratios': ratios_with_status
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/fiscal-years/by-company/<int:company_id>')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"], ROLES["EMPLOYEE"])
def get_fiscal_years_by_company(company_id):
    """企業に紐づく会計年度一覧を取得するAPI"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'success': False, 'error': 'テナントIDが設定されていません'}), 400
    
    db = SessionLocal()
    try:
        # 企業を確認
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'success': False, 'error': '企業が見つかりません'}), 404
        
        # 会計年度一覧を取得
        fiscal_years = db.query(FiscalYear).filter(
            FiscalYear.company_id == company_id
        ).order_by(FiscalYear.start_date.desc()).all()
        
        fiscal_year_list = []
        for fy in fiscal_years:
            fiscal_year_list.append({
                'id': fy.id,
                'year_name': fy.year_name,
                'start_date': fy.start_date.strftime('%Y-%m-%d'),
                'end_date': fy.end_date.strftime('%Y-%m-%d')
            })
        
        return jsonify({
            'success': True,
            'fiscal_years': fiscal_year_list
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/dashboard-analysis/multi-year/<int:company_id>')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"], ROLES["EMPLOYEE"])
def dashboard_multi_year_data(company_id):
    """複数年度データAPI"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'success': False, 'error': 'テナントIDが設定されていません'}), 400
    
    db = SessionLocal()
    try:
        from app.models_decision import ProfitLossStatement, BalanceSheet
        
        # 企業を確認
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'success': False, 'error': '企業が見つかりません'}), 404
        
        # 会計年度一覧を取得
        fiscal_years = db.query(FiscalYear).filter(
            FiscalYear.company_id == company_id
        ).order_by(FiscalYear.year).all()
        
        multi_year_data = []
        for fy in fiscal_years:
            profit_loss = db.query(ProfitLossStatement).filter(
                ProfitLossStatement.fiscal_year_id == fy.id
            ).first()
            
            balance_sheet = db.query(BalanceSheet).filter(
                BalanceSheet.fiscal_year_id == fy.id
            ).first()
            
            if profit_loss and balance_sheet:
                multi_year_data.append({
                    'fiscal_year_name': fy.year_name,
                    'sales': profit_loss.sales,
                    'operating_income': profit_loss.operating_income,
                    'ordinary_income': profit_loss.ordinary_income,
                    'net_income': profit_loss.net_income,
                    'total_assets': balance_sheet.total_assets,
                    'total_liabilities': balance_sheet.total_liabilities,
                    'total_equity': balance_sheet.total_equity
                })
        
        return jsonify({
            'success': True,
            'company_name': company.name,
            'data': multi_year_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()
