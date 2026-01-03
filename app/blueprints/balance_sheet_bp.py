"""
貸借対照表（B/S）管理API Blueprint
貸借対照表の保存と取得を行う
"""
from flask import Blueprint, request, jsonify
from app.database import get_db_session
from app.models import BalanceSheet, FiscalYear
from datetime import datetime

balance_sheet_bp = Blueprint('balance_sheet', __name__, url_prefix='/api/balance-sheet')


@balance_sheet_bp.route('/', methods=['POST'])
def save_balance_sheet():
    """貸借対照表を保存（作成または更新）"""
    data = request.get_json()
    
    if 'fiscal_year_id' not in data:
        return jsonify({'error': 'fiscal_year_idは必須です'}), 400
    
    db = get_db_session()
    try:
        # 会計年度の存在確認
        fiscal_year = db.query(FiscalYear).filter(FiscalYear.id == data['fiscal_year_id']).first()
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 既存のB/Sを検索
        bs = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == data['fiscal_year_id']
        ).first()
        
        if bs:
            # 更新
            bs.current_assets = data.get('current_assets', 0)
            bs.fixed_assets = data.get('fixed_assets', 0)
            bs.total_assets = data.get('total_assets', 0)
            bs.current_liabilities = data.get('current_liabilities', 0)
            bs.fixed_liabilities = data.get('fixed_liabilities', 0)
            bs.total_liabilities = data.get('total_liabilities', 0)
            bs.capital = data.get('capital', 0)
            bs.retained_earnings = data.get('retained_earnings', 0)
            bs.total_equity = data.get('total_equity', 0)
            bs.updated_at = datetime.now()
        else:
            # 新規作成
            bs = BalanceSheet(
                fiscal_year_id=data['fiscal_year_id'],
                current_assets=data.get('current_assets', 0),
                fixed_assets=data.get('fixed_assets', 0),
                total_assets=data.get('total_assets', 0),
                current_liabilities=data.get('current_liabilities', 0),
                fixed_liabilities=data.get('fixed_liabilities', 0),
                total_liabilities=data.get('total_liabilities', 0),
                capital=data.get('capital', 0),
                retained_earnings=data.get('retained_earnings', 0),
                total_equity=data.get('total_equity', 0)
            )
            db.add(bs)
        
        db.commit()
        db.refresh(bs)
        
        return jsonify({
            'id': bs.id,
            'fiscal_year_id': bs.fiscal_year_id,
            'current_assets': bs.current_assets,
            'fixed_assets': bs.fixed_assets,
            'total_assets': bs.total_assets,
            'current_liabilities': bs.current_liabilities,
            'fixed_liabilities': bs.fixed_liabilities,
            'total_liabilities': bs.total_liabilities,
            'capital': bs.capital,
            'retained_earnings': bs.retained_earnings,
            'total_equity': bs.total_equity,
            'created_at': bs.created_at.isoformat(),
            'updated_at': bs.updated_at.isoformat()
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@balance_sheet_bp.route('/fiscal-year/<int:fiscal_year_id>', methods=['GET'])
def get_balance_sheet_by_fiscal_year(fiscal_year_id):
    """会計年度別の貸借対照表を取得"""
    db = get_db_session()
    try:
        bs = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not bs:
            return jsonify({'error': '貸借対照表が見つかりません'}), 404
        
        return jsonify({
            'id': bs.id,
            'fiscal_year_id': bs.fiscal_year_id,
            'current_assets': bs.current_assets,
            'fixed_assets': bs.fixed_assets,
            'total_assets': bs.total_assets,
            'current_liabilities': bs.current_liabilities,
            'fixed_liabilities': bs.fixed_liabilities,
            'total_liabilities': bs.total_liabilities,
            'capital': bs.capital,
            'retained_earnings': bs.retained_earnings,
            'total_equity': bs.total_equity,
            'created_at': bs.created_at.isoformat(),
            'updated_at': bs.updated_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@balance_sheet_bp.route('/<int:bs_id>', methods=['DELETE'])
def delete_balance_sheet(bs_id):
    """貸借対照表を削除"""
    db = get_db_session()
    try:
        bs = db.query(BalanceSheet).filter(BalanceSheet.id == bs_id).first()
        
        if not bs:
            return jsonify({'error': '貸借対照表が見つかりません'}), 404
        
        db.delete(bs)
        db.commit()
        
        return jsonify({'message': '貸借対照表を削除しました'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
