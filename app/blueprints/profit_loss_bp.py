"""
損益計算書（P/L）管理API Blueprint
損益計算書の保存と取得を行う
"""
from flask import Blueprint, request, jsonify
from app.database import get_db_session
from app.models import ProfitLossStatement, FiscalYear
from datetime import datetime

profit_loss_bp = Blueprint('profit_loss', __name__, url_prefix='/api/profit-loss')


@profit_loss_bp.route('/', methods=['POST'])
def save_profit_loss():
    """損益計算書を保存（作成または更新）"""
    data = request.get_json()
    
    if 'fiscal_year_id' not in data:
        return jsonify({'error': 'fiscal_year_idは必須です'}), 400
    
    db = get_db_session()
    try:
        # 会計年度の存在確認
        fiscal_year = db.query(FiscalYear).filter(FiscalYear.id == data['fiscal_year_id']).first()
        if not fiscal_year:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        # 既存のP/Lを検索
        pl = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == data['fiscal_year_id']
        ).first()
        
        if pl:
            # 更新
            pl.sales = data.get('sales', 0)
            pl.cost_of_sales = data.get('cost_of_sales', 0)
            pl.gross_profit = data.get('gross_profit', 0)
            pl.operating_expenses = data.get('operating_expenses', 0)
            pl.operating_income = data.get('operating_income', 0)
            pl.non_operating_income = data.get('non_operating_income', 0)
            pl.non_operating_expenses = data.get('non_operating_expenses', 0)
            pl.ordinary_income = data.get('ordinary_income', 0)
            pl.extraordinary_income = data.get('extraordinary_income', 0)
            pl.extraordinary_loss = data.get('extraordinary_loss', 0)
            pl.income_before_tax = data.get('income_before_tax', 0)
            pl.income_tax = data.get('income_tax', 0)
            pl.net_income = data.get('net_income', 0)
            pl.updated_at = datetime.now()
        else:
            # 新規作成
            pl = ProfitLossStatement(
                fiscal_year_id=data['fiscal_year_id'],
                sales=data.get('sales', 0),
                cost_of_sales=data.get('cost_of_sales', 0),
                gross_profit=data.get('gross_profit', 0),
                operating_expenses=data.get('operating_expenses', 0),
                operating_income=data.get('operating_income', 0),
                non_operating_income=data.get('non_operating_income', 0),
                non_operating_expenses=data.get('non_operating_expenses', 0),
                ordinary_income=data.get('ordinary_income', 0),
                extraordinary_income=data.get('extraordinary_income', 0),
                extraordinary_loss=data.get('extraordinary_loss', 0),
                income_before_tax=data.get('income_before_tax', 0),
                income_tax=data.get('income_tax', 0),
                net_income=data.get('net_income', 0)
            )
            db.add(pl)
        
        db.commit()
        db.refresh(pl)
        
        return jsonify({
            'id': pl.id,
            'fiscal_year_id': pl.fiscal_year_id,
            'sales': pl.sales,
            'cost_of_sales': pl.cost_of_sales,
            'gross_profit': pl.gross_profit,
            'operating_expenses': pl.operating_expenses,
            'operating_income': pl.operating_income,
            'non_operating_income': pl.non_operating_income,
            'non_operating_expenses': pl.non_operating_expenses,
            'ordinary_income': pl.ordinary_income,
            'extraordinary_income': pl.extraordinary_income,
            'extraordinary_loss': pl.extraordinary_loss,
            'income_before_tax': pl.income_before_tax,
            'income_tax': pl.income_tax,
            'net_income': pl.net_income,
            'created_at': pl.created_at.isoformat(),
            'updated_at': pl.updated_at.isoformat()
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@profit_loss_bp.route('/fiscal-year/<int:fiscal_year_id>', methods=['GET'])
def get_profit_loss_by_fiscal_year(fiscal_year_id):
    """会計年度別の損益計算書を取得"""
    db = get_db_session()
    try:
        pl = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not pl:
            return jsonify({'error': '損益計算書が見つかりません'}), 404
        
        return jsonify({
            'id': pl.id,
            'fiscal_year_id': pl.fiscal_year_id,
            'sales': pl.sales,
            'cost_of_sales': pl.cost_of_sales,
            'gross_profit': pl.gross_profit,
            'operating_expenses': pl.operating_expenses,
            'operating_income': pl.operating_income,
            'non_operating_income': pl.non_operating_income,
            'non_operating_expenses': pl.non_operating_expenses,
            'ordinary_income': pl.ordinary_income,
            'extraordinary_income': pl.extraordinary_income,
            'extraordinary_loss': pl.extraordinary_loss,
            'income_before_tax': pl.income_before_tax,
            'income_tax': pl.income_tax,
            'net_income': pl.net_income,
            'created_at': pl.created_at.isoformat(),
            'updated_at': pl.updated_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@profit_loss_bp.route('/<int:pl_id>', methods=['DELETE'])
def delete_profit_loss(pl_id):
    """損益計算書を削除"""
    db = get_db_session()
    try:
        pl = db.query(ProfitLossStatement).filter(ProfitLossStatement.id == pl_id).first()
        
        if not pl:
            return jsonify({'error': '損益計算書が見つかりません'}), 404
        
        db.delete(pl)
        db.commit()
        
        return jsonify({'message': '損益計算書を削除しました'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
