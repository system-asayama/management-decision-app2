"""
複数年度計画統合管理 Blueprint
3期（複数年度）の個別計画を統合管理するAPI
"""

from flask import Blueprint, request, jsonify, session
from ..utils.decorators import require_roles, ROLES
from ..db import SessionLocal
from ..models_decision import MultiYearPlan, Company, FiscalYear
from datetime import datetime

bp = Blueprint('multi_year_plan', __name__, url_prefix='/decision/multi-year-plan')


@bp.route('/create-or-update', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def create_or_update():
    """
    複数年度計画の作成または更新
    
    Request Body:
    {
        "company_id": int,
        "base_fiscal_year_id": int,
        "years": {
            "year1": {
                "laborPlan": {...},
                "capexPlan": {...},
                "workingCapitalPlan": {...},
                "financingPlan": {...},
                "repaymentPlan": {...}
            },
            "year2": {...},
            "year3": {...}
        },
        "notes": str (optional)
    }
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'リクエストボディが空です'}), 400
        
        company_id = data.get('company_id')
        base_fiscal_year_id = data.get('base_fiscal_year_id')
        years_data = data.get('years')
        notes = data.get('notes', '')
        
        # 必須パラメータのチェック
        if not company_id or not base_fiscal_year_id or not years_data:
            return jsonify({
                'error': 'company_id, base_fiscal_year_id, yearsは必須です'
            }), 400
        
        db = SessionLocal()
        try:
            # 企業の存在確認とテナント権限チェック
            company = db.query(Company).filter(
                Company.id == company_id,
                Company.tenant_id == tenant_id
            ).first()
            
            if not company:
                return jsonify({'error': '企業が見つかりません'}), 404
            
            # 会計年度の存在確認
            fiscal_year = db.query(FiscalYear).filter(
                FiscalYear.id == base_fiscal_year_id,
                FiscalYear.company_id == company_id
            ).first()
            
            if not fiscal_year:
                return jsonify({'error': '会計年度が見つかりません'}), 404
            
            # 既存の計画を検索
            existing_plan = db.query(MultiYearPlan).filter(
                MultiYearPlan.company_id == company_id,
                MultiYearPlan.base_fiscal_year_id == base_fiscal_year_id
            ).first()
            
            if existing_plan:
                # 更新
                existing_plan.years = years_data
                existing_plan.notes = notes
                existing_plan.updated_at = datetime.now()
                
                db.commit()
                
                return jsonify({
                    'success': True,
                    'message': '複数年度計画を更新しました',
                    'data': {
                        'id': existing_plan.id,
                        'company_id': existing_plan.company_id,
                        'base_fiscal_year_id': existing_plan.base_fiscal_year_id,
                        'years': existing_plan.years,
                        'notes': existing_plan.notes,
                        'created_at': existing_plan.created_at.isoformat(),
                        'updated_at': existing_plan.updated_at.isoformat()
                    }
                }), 200
            else:
                # 新規作成
                new_plan = MultiYearPlan(
                    company_id=company_id,
                    base_fiscal_year_id=base_fiscal_year_id,
                    years=years_data,
                    notes=notes
                )
                
                db.add(new_plan)
                db.commit()
                db.refresh(new_plan)
                
                return jsonify({
                    'success': True,
                    'message': '複数年度計画を作成しました',
                    'data': {
                        'id': new_plan.id,
                        'company_id': new_plan.company_id,
                        'base_fiscal_year_id': new_plan.base_fiscal_year_id,
                        'years': new_plan.years,
                        'notes': new_plan.notes,
                        'created_at': new_plan.created_at.isoformat(),
                        'updated_at': new_plan.updated_at.isoformat()
                    }
                }), 201
                
        except Exception as e:
            db.rollback()
            return jsonify({'error': f'データベースエラー: {str(e)}'}), 500
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({'error': f'リクエスト処理エラー: {str(e)}'}), 500


@bp.route('/get-by-company', methods=['GET'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def get_by_company():
    """
    企業IDで複数年度計画を取得
    
    Query Parameters:
    - company_id: int (required)
    - base_fiscal_year_id: int (optional) - 指定した場合、その会計年度の計画のみ取得
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    try:
        company_id = request.args.get('company_id', type=int)
        base_fiscal_year_id = request.args.get('base_fiscal_year_id', type=int)
        
        if not company_id:
            return jsonify({'error': 'company_idは必須です'}), 400
        
        db = SessionLocal()
        try:
            # 企業の存在確認とテナント権限チェック
            company = db.query(Company).filter(
                Company.id == company_id,
                Company.tenant_id == tenant_id
            ).first()
            
            if not company:
                return jsonify({'error': '企業が見つかりません'}), 404
            
            # 計画を取得
            query = db.query(MultiYearPlan).filter(
                MultiYearPlan.company_id == company_id
            )
            
            if base_fiscal_year_id:
                query = query.filter(
                    MultiYearPlan.base_fiscal_year_id == base_fiscal_year_id
                )
            
            plans = query.all()
            
            # 結果を整形
            result = []
            for plan in plans:
                result.append({
                    'id': plan.id,
                    'company_id': plan.company_id,
                    'base_fiscal_year_id': plan.base_fiscal_year_id,
                    'years': plan.years,
                    'notes': plan.notes,
                    'created_at': plan.created_at.isoformat(),
                    'updated_at': plan.updated_at.isoformat()
                })
            
            return jsonify({
                'success': True,
                'count': len(result),
                'data': result
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'データベースエラー: {str(e)}'}), 500
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({'error': f'リクエスト処理エラー: {str(e)}'}), 500


@bp.route('/delete/<int:plan_id>', methods=['DELETE'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def delete(plan_id):
    """
    複数年度計画を削除
    
    Path Parameters:
    - plan_id: int
    """
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    try:
        db = SessionLocal()
        try:
            # 計画を取得
            plan = db.query(MultiYearPlan).filter(
                MultiYearPlan.id == plan_id
            ).first()
            
            if not plan:
                return jsonify({'error': '計画が見つかりません'}), 404
            
            # テナント権限チェック
            company = db.query(Company).filter(
                Company.id == plan.company_id,
                Company.tenant_id == tenant_id
            ).first()
            
            if not company:
                return jsonify({'error': '権限がありません'}), 403
            
            # 削除
            db.delete(plan)
            db.commit()
            
            return jsonify({
                'success': True,
                'message': '複数年度計画を削除しました'
            }), 200
            
        except Exception as e:
            db.rollback()
            return jsonify({'error': f'データベースエラー: {str(e)}'}), 500
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({'error': f'リクエスト処理エラー: {str(e)}'}), 500
