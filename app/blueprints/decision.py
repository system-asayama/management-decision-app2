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
