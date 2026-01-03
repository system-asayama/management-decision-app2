"""
会計年度管理API Blueprint
会計年度の作成、取得、更新、削除を行う
"""
from flask import Blueprint, request, jsonify
from app.db import SessionLocal
from app.models_decision import FiscalYear, Company
from datetime import datetime

fiscal_year_bp = Blueprint('fiscal_year', __name__, url_prefix='/api/fiscal-year')


@fiscal_year_bp.route('/', methods=['POST'])
def create_fiscal_year():
    """会計年度を作成"""
    data = request.get_json()
    
    required_fields = ['company_id', 'year', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field}は必須です'}), 400
    
    db = SessionLocal()
    try:
        # 企業の存在確認
        company = db.query(Company).filter(Company.id == data['company_id']).first()
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 日付のパース
        start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        
        fiscal_year = FiscalYear(
            company_id=data['company_id'],
            year=data['year'],
            start_date=start_date,
            end_date=end_date
        )
        db.add(fiscal_year)
        db.commit()
        db.refresh(fiscal_year)
        
        return jsonify({
            'id': fiscal_year.id,
            'company_id': fiscal_year.company_id,
            'year': fiscal_year.year,
            'start_date': fiscal_year.start_date.isoformat(),
            'end_date': fiscal_year.end_date.isoformat(),
            'created_at': fiscal_year.created_at.isoformat(),
            'updated_at': fiscal_year.updated_at.isoformat()
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@fiscal_year_bp.route('/company/<int:company_id>', methods=['GET'])
def list_fiscal_years_by_company(company_id):
    """企業別の会計年度一覧を取得"""
    db = SessionLocal()
    try:
        fiscal_years = db.query(FiscalYear).filter(
            FiscalYear.company_id == company_id
        ).order_by(FiscalYear.year.desc()).all()
        
        return jsonify([{
            'id': fy.id,
            'company_id': fy.company_id,
            'year': fy.year,
            'start_date': fy.start_date.isoformat(),
            'end_date': fy.end_date.isoformat(),
            'created_at': fy.created_at.isoformat(),
            'updated_at': fy.updated_at.isoformat()
        } for fy in fiscal_years]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@fiscal_year_bp.route('/<int:fiscal_year_id>', methods=['GET'])
def get_fiscal_year(fiscal_year_id):
    """会計年度詳細を取得"""
    db = SessionLocal()
    try:
        fiscal_year = db.query(FiscalYear).filter(FiscalYear.id == fiscal_year_id).first()
        
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        return jsonify({
            'id': fiscal_year.id,
            'company_id': fiscal_year.company_id,
            'year': fiscal_year.year,
            'start_date': fiscal_year.start_date.isoformat(),
            'end_date': fiscal_year.end_date.isoformat(),
            'created_at': fiscal_year.created_at.isoformat(),
            'updated_at': fiscal_year.updated_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@fiscal_year_bp.route('/<int:fiscal_year_id>', methods=['PUT'])
def update_fiscal_year(fiscal_year_id):
    """会計年度情報を更新"""
    data = request.get_json()
    
    db = SessionLocal()
    try:
        fiscal_year = db.query(FiscalYear).filter(FiscalYear.id == fiscal_year_id).first()
        
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 更新可能なフィールド
        if 'year' in data:
            fiscal_year.year = data['year']
        if 'start_date' in data:
            fiscal_year.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        if 'end_date' in data:
            fiscal_year.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        
        fiscal_year.updated_at = datetime.now()
        db.commit()
        db.refresh(fiscal_year)
        
        return jsonify({
            'id': fiscal_year.id,
            'company_id': fiscal_year.company_id,
            'year': fiscal_year.year,
            'start_date': fiscal_year.start_date.isoformat(),
            'end_date': fiscal_year.end_date.isoformat(),
            'created_at': fiscal_year.created_at.isoformat(),
            'updated_at': fiscal_year.updated_at.isoformat()
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@fiscal_year_bp.route('/<int:fiscal_year_id>', methods=['DELETE'])
def delete_fiscal_year(fiscal_year_id):
    """会計年度を削除"""
    db = SessionLocal()
    try:
        fiscal_year = db.query(FiscalYear).filter(FiscalYear.id == fiscal_year_id).first()
        
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        db.delete(fiscal_year)
        db.commit()
        
        return jsonify({'message': '会計年度を削除しました'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
