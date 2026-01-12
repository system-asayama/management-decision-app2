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



# ============================================================
# 経営シミュレーションルート
# ============================================================

@bp.route('/simulation')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"], ROLES["EMPLOYEE"])
def simulation():
    """経営シミュレーションページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        return render_template('simulation.html', companies=companies)
    finally:
        db.close()


@bp.route('/simulation/execute')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"], ROLES["EMPLOYEE"])
def simulation_execute():
    """シミュレーション実行API"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'success': False, 'error': 'テナントIDが設定されていません'}), 400
    
    # パラメータを取得
    company_id = request.args.get('company_id', type=int)
    base_fiscal_year_id = request.args.get('base_fiscal_year_id', type=int)
    forecast_years = request.args.get('forecast_years', type=int)
    sales_growth_rate = request.args.get('sales_growth_rate', type=float)
    
    # オプションパラメータ
    operating_margin = request.args.get('operating_margin', type=float)
    ordinary_margin = request.args.get('ordinary_margin', type=float)
    net_margin = request.args.get('net_margin', type=float)
    asset_turnover = request.args.get('asset_turnover', type=float)
    debt_ratio = request.args.get('debt_ratio', type=float)
    
    if not all([company_id, base_fiscal_year_id, forecast_years, sales_growth_rate is not None]):
        return jsonify({'success': False, 'error': '必須パラメータが不足しています'}), 400
    
    db = SessionLocal()
    try:
        from app.models_decision import ProfitLossStatement, BalanceSheet
        from app.utils.simulation_calculator import SimulationCalculator
        
        # 企業を確認
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'success': False, 'error': '企業が見つかりません'}), 404
        
        # ベース年度を確認
        base_fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == base_fiscal_year_id,
            FiscalYear.company_id == company_id
        ).first()
        
        if not base_fiscal_year:
            return jsonify({'success': False, 'error': 'ベース年度が見つかりません'}), 404
        
        # ベース年度の財務データを取得
        profit_loss = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == base_fiscal_year_id
        ).first()
        
        balance_sheet = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == base_fiscal_year_id
        ).first()
        
        if not profit_loss or not balance_sheet:
            return jsonify({'success': False, 'error': 'ベース年度の財務データが見つかりません'}), 404
        
        # シミュレーションを実行
        forecast_data = SimulationCalculator.forecast_financials(
            base_sales=profit_loss.sales,
            base_operating_income=profit_loss.operating_income,
            base_ordinary_income=profit_loss.ordinary_income,
            base_net_income=profit_loss.net_income,
            base_total_assets=balance_sheet.total_assets,
            base_total_liabilities=balance_sheet.total_liabilities,
            base_total_equity=balance_sheet.total_equity,
            forecast_years=forecast_years,
            sales_growth_rate=sales_growth_rate,
            operating_margin=operating_margin,
            ordinary_margin=ordinary_margin,
            net_margin=net_margin,
            asset_turnover=asset_turnover,
            debt_ratio=debt_ratio
        )
        
        # 財務指標を計算
        forecast_data_with_ratios = SimulationCalculator.calculate_financial_ratios(forecast_data)
        
        return jsonify({
            'success': True,
            'company_name': company.name,
            'base_year_name': base_fiscal_year.year_name,
            'forecast_years': forecast_years,
            'sales_growth_rate': sales_growth_rate,
            'forecast_data': forecast_data_with_ratios
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/simulation/scenario')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"], ROLES["ADMIN"], ROLES["EMPLOYEE"])
def simulation_scenario():
    """シナリオ分析API"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'success': False, 'error': 'テナントIDが設定されていません'}), 400
    
    # パラメータを取得
    company_id = request.args.get('company_id', type=int)
    base_fiscal_year_id = request.args.get('base_fiscal_year_id', type=int)
    forecast_years = request.args.get('forecast_years', type=int)
    sales_growth_rate = request.args.get('sales_growth_rate', type=float)
    
    if not all([company_id, base_fiscal_year_id, forecast_years, sales_growth_rate is not None]):
        return jsonify({'success': False, 'error': '必須パラメータが不足しています'}), 400
    
    db = SessionLocal()
    try:
        from app.models_decision import ProfitLossStatement, BalanceSheet
        from app.utils.simulation_calculator import SimulationCalculator
        
        # 企業を確認
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'success': False, 'error': '企業が見つかりません'}), 404
        
        # ベース年度を確認
        base_fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == base_fiscal_year_id,
            FiscalYear.company_id == company_id
        ).first()
        
        if not base_fiscal_year:
            return jsonify({'success': False, 'error': 'ベース年度が見つかりません'}), 404
        
        # ベース年度の財務データを取得
        profit_loss = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == base_fiscal_year_id
        ).first()
        
        balance_sheet = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == base_fiscal_year_id
        ).first()
        
        if not profit_loss or not balance_sheet:
            return jsonify({'success': False, 'error': 'ベース年度の財務データが見つかりません'}), 404
        
        # シナリオ分析を実行
        scenarios = SimulationCalculator.create_scenario_forecasts(
            base_sales=profit_loss.sales,
            base_operating_income=profit_loss.operating_income,
            base_ordinary_income=profit_loss.ordinary_income,
            base_net_income=profit_loss.net_income,
            base_total_assets=balance_sheet.total_assets,
            base_total_liabilities=balance_sheet.total_liabilities,
            base_total_equity=balance_sheet.total_equity,
            forecast_years=forecast_years,
            base_growth_rate=sales_growth_rate
        )
        
        # 各シナリオの財務指標を計算
        scenarios_with_ratios = {
            'optimistic': SimulationCalculator.calculate_financial_ratios(scenarios['optimistic']),
            'standard': SimulationCalculator.calculate_financial_ratios(scenarios['standard']),
            'pessimistic': SimulationCalculator.calculate_financial_ratios(scenarios['pessimistic'])
        }
        
        return jsonify({
            'success': True,
            'company_name': company.name,
            'base_year_name': base_fiscal_year.year_name,
            'forecast_years': forecast_years,
            'base_growth_rate': sales_growth_rate,
            'scenarios': scenarios_with_ratios
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()


# ============================================================
# 詳細財務分析ルート
# ============================================================

@bp.route('/financial-analysis-detailed')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def financial_analysis_detailed():
    """詳細財務分析ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        # テナントの企業一覧を取得
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        return render_template('financial_analysis_detailed.html', companies=companies)
    finally:
        db.close()


@bp.route('/financial-analysis-detailed/analyze')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def financial_analysis_detailed_analyze():
    """詳細財務分析を実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    company_id = request.args.get('company_id', type=int)
    fiscal_year_id = request.args.get('fiscal_year_id', type=int)
    
    if not company_id or not fiscal_year_id:
        return jsonify({'error': '企業IDと会計年度IDを指定してください'}), 400
    
    db = SessionLocal()
    try:
        from ..utils.advanced_financial_analysis import calculate_all_indicators
        
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 会計年度情報を取得
        fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == fiscal_year_id,
            FiscalYear.company_id == company_id
        ).first()
        
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 当期の財務データを取得
        current_pl = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == fiscal_year_id
        ).first()
        
        current_bs = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not current_pl or not current_bs:
            return jsonify({'error': '財務データが見つかりません'}), 404
        
        # 前期の財務データを取得（成長力指標用）
        # 前期の会計年度を取得
        previous_fiscal_years = db.query(FiscalYear).filter(
            FiscalYear.company_id == company_id,
            FiscalYear.start_date < fiscal_year.start_date
        ).order_by(FiscalYear.start_date.desc()).all()
        
        previous_pl = None
        previous_bs = None
        if previous_fiscal_years:
            previous_fiscal_year = previous_fiscal_years[0]
            previous_pl = db.query(ProfitLossStatement).filter(
                ProfitLossStatement.fiscal_year_id == previous_fiscal_year.id
            ).first()
            previous_bs = db.query(BalanceSheet).filter(
                BalanceSheet.fiscal_year_id == previous_fiscal_year.id
            ).first()
        
        # 当期PLデータを辞書に変換
        current_pl_data = {
            'sales': current_pl.sales,
            'cost_of_sales': current_pl.cost_of_sales,
            'gross_profit': current_pl.gross_profit,
            'operating_income': current_pl.operating_income,
            'ordinary_income': current_pl.ordinary_income,
            'net_income': current_pl.net_income,
            'employees': company.employee_count or 1,  # ゼロ除算を避けるため
            'labor_cost': current_pl.operating_expenses * 0.4,  # 仮の労務費（販管費の40%と仮定）
            'interest_expense': current_pl.non_operating_expenses  # 仮の支払利息
        }
        
        # 当期BSデータを辞書に変換
        current_bs_data = {
            'current_assets': current_bs.current_assets,
            'fixed_assets': current_bs.fixed_assets,
            'total_assets': current_bs.total_assets,
            'current_liabilities': current_bs.current_liabilities,
            'fixed_liabilities': current_bs.fixed_liabilities,
            'total_liabilities': current_bs.total_liabilities,
            'net_assets': current_bs.total_equity,
            'long_term_liabilities': current_bs.fixed_liabilities,
            'quick_assets': current_bs.current_assets * 0.7,  # 仮の当座資産（流動資産の70%と仮定）
            'accounts_receivable': current_bs.current_assets * 0.4,  # 仮の売上債権（流動資産の40%と仮定）
            'inventory': current_bs.current_assets * 0.3,  # 仮の棚卸資産（流動資産の30%と仮定）
            'accounts_payable': current_bs.current_liabilities * 0.5  # 仮の買入債務（流動負債の50%と仮定）
        }
        
        # 前期データを辞書に変換（存在する場合）
        previous_pl_data = None
        previous_bs_data = None
        if previous_pl and previous_bs:
            previous_pl_data = {
                'sales': previous_pl.sales,
                'employees': company.employee_count or 1
            }
            previous_bs_data = {
                'total_assets': previous_bs.total_assets,
                'net_assets': previous_bs.total_equity
            }
        
        # すべての財務指標を計算
        indicators = calculate_all_indicators(
            current_pl=current_pl_data,
            current_bs=current_bs_data,
            previous_pl=previous_pl_data,
            previous_bs=previous_bs_data
        )
        
        # 結果を返す
        return jsonify({
            'company_name': company.name,
            'fiscal_year_name': fiscal_year.year_name,
            'start_date': fiscal_year.start_date.strftime('%Y年%m月%d日'),
            'end_date': fiscal_year.end_date.strftime('%Y年%m月%d日'),
            'growth': indicators['growth'],
            'profitability': indicators['profitability'],
            'financial_strength': indicators['financial_strength'],
            'productivity': indicators['productivity']
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# ============================================================
# 損益分岐点分析ルート
# ============================================================

@bp.route('/breakeven-analysis')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def breakeven_analysis():
    """損益分岐点分析ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        # テナントの企業一覧を取得
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        return render_template('breakeven_analysis.html', companies=companies)
    finally:
        db.close()


@bp.route('/breakeven-analysis/analyze')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def breakeven_analysis_analyze():
    """損益分岐点分析を実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    company_id = request.args.get('company_id', type=int)
    fiscal_year_id = request.args.get('fiscal_year_id', type=int)
    
    if not company_id or not fiscal_year_id:
        return jsonify({'error': '企業IDと会計年度IDを指定してください'}), 400
    
    db = SessionLocal()
    try:
        from ..utils.breakeven_analysis import analyze_cost_volume_profit, estimate_cost_structure
        
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 会計年度情報を取得
        fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == fiscal_year_id,
            FiscalYear.company_id == company_id
        ).first()
        
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 損益計算書を取得
        profit_loss = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not profit_loss:
            return jsonify({'error': '損益計算書が見つかりません'}), 404
        
        # 費用構造を推定
        cost_structure = estimate_cost_structure(
            sales=profit_loss.sales,
            cost_of_sales=profit_loss.cost_of_sales,
            operating_expenses=profit_loss.operating_expenses,
            operating_income=profit_loss.operating_income
        )
        
        # CVP分析を実行
        cvp_result = analyze_cost_volume_profit(
            sales=profit_loss.sales,
            variable_costs=cost_structure['variable_costs'],
            fixed_costs=cost_structure['fixed_costs']
        )
        
        # 結果を返す
        return jsonify({
            'company_name': company.name,
            'fiscal_year_name': fiscal_year.year_name,
            'start_date': fiscal_year.start_date.strftime('%Y年%m月%d日'),
            'end_date': fiscal_year.end_date.strftime('%Y年%m月%d日'),
            **cvp_result
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# ============================================================
# 予算管理ルート
# ============================================================

@bp.route('/budget')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def budget_management():
    """予算管理ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        # テナントの企業一覧を取得
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        return render_template('budget_management.html', companies=companies)
    finally:
        db.close()


@bp.route('/budget/analyze')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def budget_analyze():
    """予算vs実績分析を実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    fiscal_year_id = request.args.get('fiscal_year_id', type=int)
    
    if not fiscal_year_id:
        return jsonify({'error': '会計年度IDを指定してください'}), 400
    
    db = SessionLocal()
    try:
        from ..utils.budget_analysis import analyze_budget_vs_actual, calculate_budget_achievement_summary
        from ..models_decision import Budget
        
        # 会計年度情報を取得
        fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == fiscal_year_id
        ).first()
        
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == fiscal_year.company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 予算を取得
        budget = db.query(Budget).filter(
            Budget.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not budget:
            return jsonify({
                'error': '予算が登録されていません',
                'has_budget': False
            })
        
        # 実績（損益計算書と貸借対照表）を取得
        profit_loss = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == fiscal_year_id
        ).first()
        
        balance_sheet = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not profit_loss or not balance_sheet:
            return jsonify({'error': '実績データが見つかりません'}), 404
        
        # 予算データを辞書に変換
        budget_data = {
            'budget_sales': float(budget.budget_sales or 0),
            'budget_cost_of_sales': float(budget.budget_cost_of_sales or 0),
            'budget_gross_profit': float(budget.budget_gross_profit or 0),
            'budget_operating_expenses': float(budget.budget_operating_expenses or 0),
            'budget_operating_income': float(budget.budget_operating_income or 0),
            'budget_ordinary_income': float(budget.budget_ordinary_income or 0),
            'budget_net_income': float(budget.budget_net_income or 0),
            'budget_current_assets': float(budget.budget_current_assets or 0),
            'budget_fixed_assets': float(budget.budget_fixed_assets or 0),
            'budget_total_assets': float(budget.budget_total_assets or 0),
            'budget_current_liabilities': float(budget.budget_current_liabilities or 0),
            'budget_fixed_liabilities': float(budget.budget_fixed_liabilities or 0),
            'budget_total_liabilities': float(budget.budget_total_liabilities or 0),
            'budget_total_equity': float(budget.budget_total_equity or 0)
        }
        
        # 実績データを辞書に変換
        actual_data = {
            'sales': float(profit_loss.sales or 0),
            'cost_of_sales': float(profit_loss.cost_of_sales or 0),
            'gross_profit': float(profit_loss.gross_profit or 0),
            'operating_expenses': float(profit_loss.operating_expenses or 0),
            'operating_income': float(profit_loss.operating_income or 0),
            'ordinary_income': float(profit_loss.ordinary_income or 0),
            'net_income': float(profit_loss.net_income or 0),
            'current_assets': float(balance_sheet.current_assets or 0),
            'fixed_assets': float(balance_sheet.fixed_assets or 0),
            'total_assets': float(balance_sheet.total_assets or 0),
            'current_liabilities': float(balance_sheet.current_liabilities or 0),
            'fixed_liabilities': float(balance_sheet.fixed_liabilities or 0),
            'total_liabilities': float(balance_sheet.total_liabilities or 0),
            'total_equity': float(balance_sheet.total_equity or 0)
        }
        
        # 予算vs実績分析を実行
        analysis_result = analyze_budget_vs_actual(budget_data, actual_data)
        
        # 予算達成度サマリーを計算
        summary = calculate_budget_achievement_summary(analysis_result)
        
        # 結果を返す
        return jsonify({
            'has_budget': True,
            'budget': {
                'id': budget.id,
                **budget_data
            },
            'pl': analysis_result['pl'],
            'bs': analysis_result['bs'],
            'summary': summary
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/budget', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def budget_create():
    """予算を登録"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    fiscal_year_id = data.get('fiscal_year_id')
    
    if not fiscal_year_id:
        return jsonify({'error': '会計年度IDを指定してください'}), 400
    
    db = SessionLocal()
    try:
        from ..models_decision import Budget
        
        # 会計年度の存在確認
        fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == fiscal_year_id
        ).first()
        
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 企業のテナント確認
        company = db.query(Company).filter(
            Company.id == fiscal_year.company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 既存の予算があるか確認
        existing_budget = db.query(Budget).filter(
            Budget.fiscal_year_id == fiscal_year_id
        ).first()
        
        if existing_budget:
            return jsonify({'error': 'この会計年度の予算は既に登録されています'}), 400
        
        # 予算を作成
        budget = Budget(
            fiscal_year_id=fiscal_year_id,
            budget_sales=data.get('budget_sales'),
            budget_cost_of_sales=data.get('budget_cost_of_sales'),
            budget_gross_profit=data.get('budget_gross_profit'),
            budget_operating_expenses=data.get('budget_operating_expenses'),
            budget_operating_income=data.get('budget_operating_income'),
            budget_non_operating_income=data.get('budget_non_operating_income'),
            budget_non_operating_expenses=data.get('budget_non_operating_expenses'),
            budget_ordinary_income=data.get('budget_ordinary_income'),
            budget_extraordinary_income=data.get('budget_extraordinary_income'),
            budget_extraordinary_loss=data.get('budget_extraordinary_loss'),
            budget_income_before_tax=data.get('budget_income_before_tax'),
            budget_income_tax=data.get('budget_income_tax'),
            budget_net_income=data.get('budget_net_income'),
            budget_current_assets=data.get('budget_current_assets'),
            budget_fixed_assets=data.get('budget_fixed_assets'),
            budget_total_assets=data.get('budget_total_assets'),
            budget_current_liabilities=data.get('budget_current_liabilities'),
            budget_fixed_liabilities=data.get('budget_fixed_liabilities'),
            budget_total_liabilities=data.get('budget_total_liabilities'),
            budget_total_equity=data.get('budget_total_equity'),
            notes=data.get('notes')
        )
        
        db.add(budget)
        db.commit()
        
        return jsonify({'message': '予算を登録しました', 'id': budget.id})
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/budget/<int:budget_id>', methods=['PUT'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def budget_update(budget_id):
    """予算を更新"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    db = SessionLocal()
    try:
        from ..models_decision import Budget
        
        # 予算を取得
        budget = db.query(Budget).filter(Budget.id == budget_id).first()
        
        if not budget:
            return jsonify({'error': '予算が見つかりません'}), 404
        
        # 会計年度の企業のテナント確認
        fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == budget.fiscal_year_id
        ).first()
        
        company = db.query(Company).filter(
            Company.id == fiscal_year.company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 予算を更新
        budget.budget_sales = data.get('budget_sales')
        budget.budget_cost_of_sales = data.get('budget_cost_of_sales')
        budget.budget_gross_profit = data.get('budget_gross_profit')
        budget.budget_operating_expenses = data.get('budget_operating_expenses')
        budget.budget_operating_income = data.get('budget_operating_income')
        budget.budget_non_operating_income = data.get('budget_non_operating_income')
        budget.budget_non_operating_expenses = data.get('budget_non_operating_expenses')
        budget.budget_ordinary_income = data.get('budget_ordinary_income')
        budget.budget_extraordinary_income = data.get('budget_extraordinary_income')
        budget.budget_extraordinary_loss = data.get('budget_extraordinary_loss')
        budget.budget_income_before_tax = data.get('budget_income_before_tax')
        budget.budget_income_tax = data.get('budget_income_tax')
        budget.budget_net_income = data.get('budget_net_income')
        budget.budget_current_assets = data.get('budget_current_assets')
        budget.budget_fixed_assets = data.get('budget_fixed_assets')
        budget.budget_total_assets = data.get('budget_total_assets')
        budget.budget_current_liabilities = data.get('budget_current_liabilities')
        budget.budget_fixed_liabilities = data.get('budget_fixed_liabilities')
        budget.budget_total_liabilities = data.get('budget_total_liabilities')
        budget.budget_total_equity = data.get('budget_total_equity')
        budget.notes = data.get('notes')
        
        db.commit()
        
        return jsonify({'message': '予算を更新しました'})
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# ============================================================
# 借入金許容限度額分析ルート
# ============================================================

@bp.route('/debt-capacity')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def debt_capacity_analysis():
    """借入金許容限度額分析ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        # テナントの企業一覧を取得
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        return render_template('debt_capacity_analysis.html', companies=companies)
    finally:
        db.close()


@bp.route('/debt-capacity/analyze')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def debt_capacity_analyze():
    """借入金許容限度額分析を実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    fiscal_year_id = request.args.get('fiscal_year_id', type=int)
    
    if not fiscal_year_id:
        return jsonify({'error': '会計年度IDを指定してください'}), 400
    
    db = SessionLocal()
    try:
        from ..utils.debt_capacity_analysis import calculate_debt_capacity, evaluate_debt_health
        
        # 会計年度情報を取得
        fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == fiscal_year_id
        ).first()
        
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == fiscal_year.company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 損益計算書と貸借対照表を取得
        profit_loss = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == fiscal_year_id
        ).first()
        
        balance_sheet = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not profit_loss or not balance_sheet:
            return jsonify({'error': '財務データが見つかりません'}), 404
        
        # 年間キャッシュフローを計算（簡易的に営業利益を使用）
        annual_cash_flow = float(profit_loss.operating_income or 0)
        
        # 支払利息（簡易的に営業外費用の50%と仮定）
        interest_expense = float(profit_loss.non_operating_expenses or 0) * 0.5
        
        # 借入金許容限度額を計算
        capacity = calculate_debt_capacity(
            total_assets=float(balance_sheet.total_assets or 0),
            total_liabilities=float(balance_sheet.total_liabilities or 0),
            total_equity=float(balance_sheet.total_equity or 0),
            operating_income=float(profit_loss.operating_income or 0),
            interest_expense=interest_expense,
            annual_cash_flow=annual_cash_flow
        )
        
        # 借入金健全性を評価
        health = evaluate_debt_health(
            equity_ratio=capacity['current_equity_ratio'],
            debt_ratio=capacity['current_debt_ratio'],
            debt_service_years=capacity['debt_service_years'],
            interest_coverage_ratio=capacity['interest_coverage_ratio']
        )
        
        return jsonify({
            'capacity': capacity,
            'health': health
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@bp.route('/debt-capacity/repayment-plan')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def debt_capacity_repayment_plan():
    """返済計画を計算"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    loan_amount = request.args.get('loan_amount', type=float)
    interest_rate = request.args.get('interest_rate', type=float)
    repayment_years = request.args.get('repayment_years', type=int)
    
    if not loan_amount or not repayment_years:
        return jsonify({'error': 'パラメータが不足しています'}), 400
    
    try:
        from ..utils.debt_capacity_analysis import calculate_debt_repayment_plan
        
        repayment_plan = calculate_debt_repayment_plan(
            debt_amount=loan_amount,
            annual_interest_rate=interest_rate,
            repayment_years=repayment_years
        )
        
        return jsonify({'repayment_plan': repayment_plan})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500



# ============================================================
# 資金繰り計画
# ============================================================

@bp.route('/cash-flow-planning')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def cash_flow_planning():
    """資金繰り計画ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        return render_template('cash_flow_planning.html', companies=companies)
    finally:
        db.close()


@bp.route('/cash-flow-planning/generate', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def generate_cash_flow_plan():
    """資金繰り計画を生成"""
    from app.utils.cash_flow_planning import generate_annual_cash_flow_plan, calculate_required_financing
    
    data = request.json
    
    # 年間の資金繰り計画を生成
    cash_flow_plan = generate_annual_cash_flow_plan(
        beginning_balance=data['beginning_balance'],
        monthly_sales_revenue=data['monthly_sales_revenue'],
        monthly_purchase_payment=data['monthly_purchase_payment'],
        monthly_personnel_cost=data['monthly_personnel_cost'],
        monthly_rent=data['monthly_rent'],
        monthly_utilities=data['monthly_utilities'],
        monthly_other_expenses=data['monthly_other_expenses'],
        loan_repayment=data.get('loan_repayment', 0),
        tax_payment_month=data.get('tax_payment_month'),
        tax_payment_amount=data.get('tax_payment_amount', 0)
    )
    
    # 資金不足を検出
    financing_info = calculate_required_financing(
        cash_flow_plan,
        minimum_balance=data['minimum_balance']
    )
    
    return jsonify({
        'cash_flow_plan': cash_flow_plan,
        'minimum_balance': data['minimum_balance'],
        **financing_info
    })


@bp.route('/cash-flow-planning/simulate-financing', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def simulate_financing():
    """資金調達の影響をシミュレーション"""
    from app.utils.cash_flow_planning import simulate_financing_impact
    
    data = request.json
    
    updated_plan = simulate_financing_impact(
        cash_flow_plan=data['cash_flow_plan'],
        financing_amount=data['financing_amount'],
        financing_month=data['financing_month'],
        interest_rate=data['interest_rate']
    )
    
    return jsonify({
        'updated_plan': updated_plan
    })



# ============================================================
# 内部留保シミュレーション
# ============================================================

@bp.route('/retained-earnings-simulation')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def retained_earnings_simulation():
    """内部留保シミュレーションページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        return render_template('retained_earnings_simulation.html', companies=companies)
    finally:
        db.close()


@bp.route('/retained-earnings-simulation/simulate')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def retained_earnings_simulation_simulate():
    """内部留保シミュレーションを実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    company_id = request.args.get('company_id', type=int)
    fiscal_year_id = request.args.get('fiscal_year_id', type=int)
    years = request.args.get('years', type=int, default=10)
    dividend_payout_ratio = request.args.get('dividend_payout_ratio', type=float, default=0.3)
    growth_rate = request.args.get('growth_rate', type=float, default=0.0)
    
    if not company_id or not fiscal_year_id:
        return jsonify({'error': '企業IDと会計年度IDを指定してください'}), 400
    
    db = SessionLocal()
    try:
        from ..utils.retained_earnings_simulation import simulate_retained_earnings
        
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 会計年度情報を取得
        fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == fiscal_year_id,
            FiscalYear.company_id == company_id
        ).first()
        
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 財務データを取得
        profit_loss = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == fiscal_year_id
        ).first()
        
        balance_sheet = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not profit_loss or not balance_sheet:
            return jsonify({'error': '財務データが見つかりません'}), 404
        
        # シミュレーションを実行
        result = simulate_retained_earnings(
            current_net_assets=float(balance_sheet.total_equity),
            annual_net_income=float(profit_loss.net_income),
            dividend_payout_ratio=dividend_payout_ratio,
            years=years,
            growth_rate=growth_rate
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# ============================================================
# 貢献度分析
# ============================================================

@bp.route('/contribution-analysis')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def contribution_analysis():
    """貢献度分析ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        return render_template('contribution_analysis.html', companies=companies)
    finally:
        db.close()


@bp.route('/contribution-analysis/analyze', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def contribution_analysis_analyze():
    """貢献度分析を実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    segments = data.get('segments', [])
    common_fixed_cost = float(data.get('common_fixed_cost', 0))
    
    if not segments:
        return jsonify({'error': 'セグメント情報を指定してください'}), 400
    
    try:
        from ..utils.contribution_analyzer import analyze_product_mix
        
        # 貢献度分析を実行
        result = analyze_product_mix(segments, common_fixed_cost)
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ============================================================
# 最小二乗法による予測
# ============================================================

@bp.route('/least-squares-forecast')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def least_squares_forecast():
    """最小二乗法による予測ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        return render_template('least_squares_forecast.html', companies=companies)
    finally:
        db.close()


@bp.route('/least-squares-forecast/forecast')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def least_squares_forecast_forecast():
    """最小二乗法による予測を実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    company_id = request.args.get('company_id', type=int)
    forecast_years = request.args.get('forecast_years', type=int, default=5)
    
    if not company_id:
        return jsonify({'error': '企業IDを指定してください'}), 400
    
    db = SessionLocal()
    try:
        from ..utils.least_squares_forecaster import forecast_sales
        
        # 企業情報を取得
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.tenant_id == tenant_id
        ).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 会計年度と財務データを取得
        fiscal_years = db.query(FiscalYear).filter(
            FiscalYear.company_id == company_id
        ).order_by(FiscalYear.start_date).all()
        
        if len(fiscal_years) < 2:
            return jsonify({'error': '最小2年分の会計年度データが必要です'}), 400
        
        # 売上高データを収集
        sales_data = []
        operating_income_data = []
        net_income_data = []
        
        for fy in fiscal_years:
            profit_loss = db.query(ProfitLossStatement).filter(
                ProfitLossStatement.fiscal_year_id == fy.id
            ).first()
            
            if profit_loss:
                # 年度番号を抽出（例: "2023年度" -> 2023）
                year_num = int(fy.year_name.replace('年度', ''))
                
                sales_data.append({
                    'year': year_num,
                    'sales': float(profit_loss.sales)
                })
                
                operating_income_data.append({
                    'year': year_num,
                    'sales': float(profit_loss.operating_income)
                })
                
                net_income_data.append({
                    'year': year_num,
                    'sales': float(profit_loss.net_income)
                })
        
        if len(sales_data) < 2:
            return jsonify({'error': '最小2年分の財務データが必要です'}), 400
        
        # 各指標の予測を実行
        sales_forecast = forecast_sales(sales_data, forecast_years)
        operating_income_forecast = forecast_sales(operating_income_data, forecast_years)
        net_income_forecast = forecast_sales(net_income_data, forecast_years)
        
        return jsonify({
            'sales': sales_forecast,
            'operating_income': operating_income_forecast,
            'net_income': net_income_forecast
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# ============================================================
# 差額原価収益分析
# ============================================================

@bp.route('/differential-analysis')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def differential_analysis():
    """差額原価収益分析ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    return render_template('differential_cost_analysis.html')


@bp.route('/differential-analysis/general', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def differential_analysis_general():
    """一般的な差額分析を実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.differential_analysis import calculate_differential_profit
        
        result = calculate_differential_profit(
            scenario_a_sales=float(data.get('scenario_a_sales', 0)),
            scenario_a_variable_cost=float(data.get('scenario_a_variable_cost', 0)),
            scenario_a_fixed_cost=float(data.get('scenario_a_fixed_cost', 0)),
            scenario_b_sales=float(data.get('scenario_b_sales', 0)),
            scenario_b_variable_cost=float(data.get('scenario_b_variable_cost', 0)),
            scenario_b_fixed_cost=float(data.get('scenario_b_fixed_cost', 0))
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/differential-analysis/make-or-buy', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def differential_analysis_make_or_buy():
    """自製か購入か分析を実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.differential_analysis import analyze_make_or_buy
        
        result = analyze_make_or_buy(
            make_variable_cost=float(data.get('make_variable_cost', 0)),
            make_fixed_cost=float(data.get('make_fixed_cost', 0)),
            buy_price=float(data.get('buy_price', 0)),
            quantity=int(data.get('quantity', 0))
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/differential-analysis/special-order', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def differential_analysis_special_order():
    """特別注文の受諾可否分析を実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.differential_analysis import analyze_accept_or_reject_order
        
        result = analyze_accept_or_reject_order(
            regular_price=float(data.get('regular_price', 0)),
            special_order_price=float(data.get('special_order_price', 0)),
            variable_cost=float(data.get('variable_cost', 0)),
            quantity=int(data.get('quantity', 0)),
            additional_fixed_cost=float(data.get('additional_fixed_cost', 0))
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/differential-analysis/continue-or-discontinue', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def differential_analysis_continue_or_discontinue():
    """事業継続・撤退分析を実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.differential_analysis import analyze_continue_or_discontinue
        
        result = analyze_continue_or_discontinue(
            sales=float(data.get('sales', 0)),
            variable_cost=float(data.get('variable_cost', 0)),
            direct_fixed_cost=float(data.get('direct_fixed_cost', 0)),
            avoidable_fixed_cost=float(data.get('avoidable_fixed_cost', 0)),
            unavoidable_fixed_cost=float(data.get('unavoidable_fixed_cost', 0))
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ============================================================
# 労務費管理計画
# ============================================================

@bp.route('/labor-cost-planning')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def labor_cost_planning():
    """労務費管理計画ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    return render_template('labor_cost_planning.html')


@bp.route('/labor-cost-planning/calculate', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def labor_cost_planning_calculate():
    """労務費計画を計算"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.labor_cost_planner import plan_labor_cost
        
        result = plan_labor_cost(
            current_employee_count=int(data.get('current_employee_count', 0)),
            planned_employee_count=int(data.get('planned_employee_count', 0)),
            average_salary=float(data.get('average_salary', 0)),
            bonus_months=float(data.get('bonus_months', 2.0)),
            social_insurance_rate=float(data.get('social_insurance_rate', 0.15)),
            welfare_rate=float(data.get('welfare_rate', 0.05)),
            other_rate=float(data.get('other_rate', 0.02))
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/labor-cost-planning/analyze', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def labor_cost_planning_analyze():
    """労務費効率性を分析"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.labor_cost_planner import analyze_labor_cost_efficiency
        
        result = analyze_labor_cost_efficiency(
            total_labor_cost=float(data.get('total_labor_cost', 0)),
            sales=float(data.get('sales', 0)),
            operating_income=float(data.get('operating_income', 0)),
            employee_count=int(data.get('employee_count', 1))
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ============================================================
# 設備投資計画
# ============================================================

@bp.route('/capital-investment')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def capital_investment():
    """設備投資計画ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    return render_template('capital_investment_planning.html')


@bp.route('/capital-investment/evaluate', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def capital_investment_evaluate():
    """投資案件を評価"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.capital_investment_planner import evaluate_investment
        
        result = evaluate_investment(
            initial_investment=float(data.get('initial_investment', 0)),
            annual_cash_flows=[float(cf) for cf in data.get('annual_cash_flows', [])],
            discount_rate=float(data.get('discount_rate', 5)),
            project_name=data.get('project_name', '投資案件')
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/capital-investment/replacement', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def capital_investment_replacement():
    """設備更新を評価"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.capital_investment_planner import calculate_equipment_replacement
        
        result = calculate_equipment_replacement(
            old_equipment_book_value=float(data.get('old_equipment_book_value', 0)),
            old_equipment_salvage_value=float(data.get('old_equipment_salvage_value', 0)),
            old_equipment_annual_cost=float(data.get('old_equipment_annual_cost', 0)),
            new_equipment_cost=float(data.get('new_equipment_cost', 0)),
            new_equipment_salvage_value=float(data.get('new_equipment_salvage_value', 0)),
            new_equipment_annual_cost=float(data.get('new_equipment_annual_cost', 0)),
            useful_life=int(data.get('useful_life', 10)),
            discount_rate=float(data.get('discount_rate', 5))
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ============================================================
# 主要運転資金計画
# ============================================================

@bp.route('/working-capital-planning')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def working_capital_planning():
    """主要運転資金計画ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    return render_template('working_capital_planning.html')


@bp.route('/working-capital-planning/calculate', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def working_capital_planning_calculate():
    """運転資金を計算"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.working_capital_planner import plan_working_capital
        
        result = plan_working_capital(
            sales=float(data.get('sales', 0)),
            cost_of_sales=float(data.get('cost_of_sales', 0)),
            accounts_receivable_days=int(data.get('accounts_receivable_days', 30)),
            inventory_days=int(data.get('inventory_days', 30)),
            accounts_payable_days=int(data.get('accounts_payable_days', 30))
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/working-capital-planning/increase', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def working_capital_planning_increase():
    """運転資金増加額を計算"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.working_capital_planner import calculate_required_working_capital_increase
        
        result = calculate_required_working_capital_increase(
            current_sales=float(data.get('current_sales', 0)),
            planned_sales=float(data.get('planned_sales', 0)),
            current_working_capital=float(data.get('current_working_capital', 0))
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ============================================================
# 資金調達返済計画
# ============================================================

@bp.route('/financing-repayment')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def financing_repayment():
    """資金調達返済計画ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    return render_template('financing_repayment_planning.html')


@bp.route('/financing-repayment/plan', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def financing_repayment_plan():
    """資金調達計画を作成"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.financing_repayment_planner import plan_financing_repayment
        
        result = plan_financing_repayment(
            required_funds=float(data.get('required_funds', 0)),
            equity_ratio=float(data.get('equity_ratio', 30)),
            loan_interest_rate=float(data.get('loan_interest_rate', 2.5)),
            loan_term_years=int(data.get('loan_term_years', 10)),
            payment_frequency=data.get('payment_frequency', 'monthly')
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/financing-repayment/schedule', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def financing_repayment_schedule():
    """返済スケジュールを生成"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.financing_repayment_planner import generate_amortization_schedule
        
        schedule = generate_amortization_schedule(
            principal=float(data.get('principal', 0)),
            annual_interest_rate=float(data.get('annual_interest_rate', 2.5)),
            term_years=int(data.get('term_years', 10)),
            payment_frequency='monthly'
        )
        
        return jsonify({'schedule': schedule})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/financing-repayment/refinance', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def financing_repayment_refinance():
    """借り換えを分析"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    
    try:
        from ..utils.financing_repayment_planner import calculate_refinancing_benefit
        
        result = calculate_refinancing_benefit(
            current_loan_balance=float(data.get('current_loan_balance', 0)),
            current_interest_rate=float(data.get('current_interest_rate', 3.0)),
            remaining_term_years=int(data.get('remaining_term_years', 8)),
            new_interest_rate=float(data.get('new_interest_rate', 2.0)),
            refinancing_cost=float(data.get('refinancing_cost', 0))
        )
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
