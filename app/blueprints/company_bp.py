"""
企業管理API Blueprint
企業の作成、取得、更新、削除を行う
"""
from flask import Blueprint, request, jsonify
from app.database import get_db_session
from app.models import Company
from datetime import datetime

company_bp = Blueprint('company', __name__, url_prefix='/api/company')


@company_bp.route('/', methods=['POST'])
def create_company():
    """企業を作成"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': '企業名は必須です'}), 400
    
    db = get_db_session()
    try:
        company = Company(
            name=data['name']
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        
        return jsonify({
            'id': company.id,
            'name': company.name,
            'created_at': company.created_at.isoformat(),
            'updated_at': company.updated_at.isoformat()
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@company_bp.route('/', methods=['GET'])
def list_companies():
    """企業一覧を取得"""
    db = get_db_session()
    try:
        companies = db.query(Company).order_by(Company.created_at.desc()).all()
        
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'created_at': c.created_at.isoformat(),
            'updated_at': c.updated_at.isoformat()
        } for c in companies]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@company_bp.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
    """企業詳細を取得"""
    db = get_db_session()
    try:
        company = db.query(Company).filter(Company.id == company_id).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        return jsonify({
            'id': company.id,
            'name': company.name,
            'created_at': company.created_at.isoformat(),
            'updated_at': company.updated_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@company_bp.route('/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    """企業情報を更新"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': '企業名は必須です'}), 400
    
    db = get_db_session()
    try:
        company = db.query(Company).filter(Company.id == company_id).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        company.name = data['name']
        company.updated_at = datetime.now()
        db.commit()
        db.refresh(company)
        
        return jsonify({
            'id': company.id,
            'name': company.name,
            'created_at': company.created_at.isoformat(),
            'updated_at': company.updated_at.isoformat()
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@company_bp.route('/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    """企業を削除"""
    db = get_db_session()
    try:
        company = db.query(Company).filter(Company.id == company_id).first()
        
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        db.delete(company)
        db.commit()
        
        return jsonify({'message': '企業を削除しました'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
