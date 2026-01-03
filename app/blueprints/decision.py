"""
経営意思決定アプリ - メインBlueprint
"""

from flask import Blueprint, render_template, redirect, url_for, session
from ..utils.decorators import require_roles, ROLES

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
