"""
ダッシュボードAPI Blueprint
ダッシュボード用のサマリーデータを提供
"""
from flask import Blueprint, request, jsonify
from app.db import SessionLocal
from app.models_decision import Company, FiscalYear, ProfitLossStatement, BalanceSheet
from sqlalchemy import func, desc

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@dashboard_bp.route('/summary/<int:company_id>', methods=['GET'])
def get_dashboard_summary(company_id):
    """ダッシュボード用サマリーデータを取得"""
    db = SessionLocal()
    try:
        # 企業情報
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            return jsonify({'error': '企業が見つかりません'}), 404
        
        # 最新の会計年度を取得
        latest_fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.company_id == company_id
        ).order_by(desc(FiscalYear.year)).first()
        
        if not latest_fiscal_year:
            return jsonify({
                'company': {
                    'id': company.id,
                    'name': company.name
                },
                'latest_fiscal_year': None,
                'profit_loss': None,
                'balance_sheet': None,
                'fiscal_years_count': 0
            }), 200
        
        # 最新のP/L
        pl = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == latest_fiscal_year.id
        ).first()
        
        # 最新のB/S
        bs = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == latest_fiscal_year.id
        ).first()
        
        # 会計年度の総数
        fiscal_years_count = db.query(func.count(FiscalYear.id)).filter(
            FiscalYear.company_id == company_id
        ).scalar()
        
        return jsonify({
            'company': {
                'id': company.id,
                'name': company.name
            },
            'latest_fiscal_year': {
                'id': latest_fiscal_year.id,
                'year': latest_fiscal_year.year,
                'start_date': latest_fiscal_year.start_date.isoformat(),
                'end_date': latest_fiscal_year.end_date.isoformat()
            },
            'profit_loss': {
                'sales': pl.sales if pl else 0,
                'operating_income': pl.operating_income if pl else 0,
                'ordinary_income': pl.ordinary_income if pl else 0,
                'net_income': pl.net_income if pl else 0
            } if pl else None,
            'balance_sheet': {
                'total_assets': bs.total_assets if bs else 0,
                'total_liabilities': bs.total_liabilities if bs else 0,
                'total_equity': bs.total_equity if bs else 0
            } if bs else None,
            'fiscal_years_count': fiscal_years_count
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@dashboard_bp.route('/comparison/<int:company_id>', methods=['GET'])
def get_multi_year_comparison(company_id):
    """複数年度の財務データ比較を取得"""
    db = SessionLocal()
    try:
        # 最新3年度を取得
        fiscal_years = db.query(FiscalYear).filter(
            FiscalYear.company_id == company_id
        ).order_by(desc(FiscalYear.year)).limit(3).all()
        
        if not fiscal_years:
            return jsonify({'error': '会計年度が見つかりません'}), 404
        
        comparison_data = []
        for fy in fiscal_years:
            pl = db.query(ProfitLossStatement).filter(
                ProfitLossStatement.fiscal_year_id == fy.id
            ).first()
            
            bs = db.query(BalanceSheet).filter(
                BalanceSheet.fiscal_year_id == fy.id
            ).first()
            
            comparison_data.append({
                'fiscal_year': {
                    'id': fy.id,
                    'year': fy.year,
                    'start_date': fy.start_date.isoformat(),
                    'end_date': fy.end_date.isoformat()
                },
                'profit_loss': {
                    'sales': pl.sales if pl else 0,
                    'cost_of_sales': pl.cost_of_sales if pl else 0,
                    'gross_profit': pl.gross_profit if pl else 0,
                    'operating_income': pl.operating_income if pl else 0,
                    'ordinary_income': pl.ordinary_income if pl else 0,
                    'net_income': pl.net_income if pl else 0
                } if pl else None,
                'balance_sheet': {
                    'total_assets': bs.total_assets if bs else 0,
                    'total_liabilities': bs.total_liabilities if bs else 0,
                    'total_equity': bs.total_equity if bs else 0
                } if bs else None
            })
        
        return jsonify({
            'company_id': company_id,
            'comparison_data': comparison_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
