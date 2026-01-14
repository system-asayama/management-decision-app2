"""
マイグレーション実行用Blueprint
"""

from flask import Blueprint, jsonify
from ..utils.decorators import require_roles, ROLES
from ..db import SessionLocal, engine
from ..models_login import TTenantAdminTenant

bp = Blueprint('migration', __name__, url_prefix='/migration')


@bp.route('/create-tenant-admin-table', methods=['POST'])
@require_roles(ROLES["SYSTEM_ADMIN"])
def create_tenant_admin_table():
    """T_テナント管理者_テナントテーブルを作成"""
    try:
        # テーブルを作成
        TTenantAdminTenant.__table__.create(engine, checkfirst=True)
        
        return jsonify({
            'success': True,
            'message': 'T_テナント管理者_テナントテーブルを作成しました'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/migrate-tenant-admin-data', methods=['POST'])
@require_roles(ROLES["SYSTEM_ADMIN"])
def migrate_tenant_admin_data():
    """既存のテナント管理者データを中間テーブルに移行"""
    from ..models_login import TKanrisha
    
    db = SessionLocal()
    try:
        # テナント管理者を取得 (role=2)
        tenant_admins = db.query(TKanrisha).filter(
            TKanrisha.role == 2,
            TKanrisha.tenant_id.isnot(None)
        ).all()
        
        migrated_count = 0
        for admin in tenant_admins:
            # 既に中間テーブルにデータがあるかチェック
            existing = db.query(TTenantAdminTenant).filter(
                TTenantAdminTenant.admin_id == admin.id,
                TTenantAdminTenant.tenant_id == admin.tenant_id
            ).first()
            
            if not existing:
                # 中間テーブルにデータを追加
                relation = TTenantAdminTenant(
                    admin_id=admin.id,
                    tenant_id=admin.tenant_id,
                    is_owner=admin.is_owner if hasattr(admin, 'is_owner') and admin.is_owner else 0
                )
                db.add(relation)
                migrated_count += 1
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': f'{migrated_count}件のデータを移行しました',
            'migrated_count': migrated_count
        })
        
    except Exception as e:
        db.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        db.close()
