"""
最小二乗法分析用のBlueprint
"""

from flask import Blueprint, request, jsonify, session
from app.decorators import require_roles
from app.config import ROLES
import os

bp = Blueprint('least_squares', __name__, url_prefix='/decision/least-squares')


@bp.route('/analyze-cost-structure', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def analyze_cost_structure():
    """費用構造を分析（固定費と変動費率を推定）"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    sales_data = data.get('sales_data', [])
    cost_data = data.get('cost_data', [])
    
    if not sales_data or not cost_data:
        return jsonify({'error': '売上データと費用データを指定してください'}), 400
    
    if len(sales_data) != len(cost_data):
        return jsonify({'error': '売上データと費用データの長さが一致しません'}), 400
    
    try:
        from app.utils.least_squares_forecaster import analyze_cost_structure as analyze_func
        
        result = analyze_func(sales_data, cost_data)
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/forecast-costs', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def forecast_costs_api():
    """費用の予測を実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    data = request.get_json()
    historical_data = data.get('historical_data', [])
    cost_metric = data.get('cost_metric', 'cost_of_sales')
    forecast_years = data.get('forecast_years', 5)
    
    if not historical_data:
        return jsonify({'error': '過去データを指定してください'}), 400
    
    try:
        from app.utils.least_squares_forecaster import forecast_costs
        
        result = forecast_costs(historical_data, cost_metric, forecast_years)
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/import-from-excel', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def import_from_excel():
    """Excelファイルから複数年度の財務データを読み取って最小二乗法分析を実行"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return jsonify({'error': 'テナントIDが見つかりません'}), 403
    
    # ファイルアップロード
    if 'file' not in request.files:
        return jsonify({'error': 'ファイルがアップロードされていません'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'ファイル名が空です'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': 'Excelファイル（.xlsx または .xls）をアップロードしてください'}), 400
    
    try:
        # 一時ファイルとして保存
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            file.save(tmp_file.name)
            tmp_file_path = tmp_file.name
        
        # Excelから財務データを読み取る
        from app.utils.excel_financial_data_importer import (
            import_multi_year_financial_data,
            prepare_data_for_least_squares
        )
        from app.utils.least_squares_forecaster import forecast_costs
        
        financial_data = import_multi_year_financial_data(tmp_file_path)
        
        # 原価の予測
        cost_of_sales_data = prepare_data_for_least_squares(financial_data, 'cost_of_sales')
        cost_of_sales_forecast = forecast_costs(cost_of_sales_data, 'cost_of_sales', forecast_years=5)
        
        # 販管費の予測
        operating_expenses_data = prepare_data_for_least_squares(financial_data, 'operating_expenses')
        operating_expenses_forecast = forecast_costs(operating_expenses_data, 'operating_expenses', forecast_years=5)
        
        # 一時ファイルを削除
        os.unlink(tmp_file_path)
        
        return jsonify({
            'financial_data': financial_data,
            'cost_of_sales_forecast': cost_of_sales_forecast,
            'operating_expenses_forecast': operating_expenses_forecast
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        # 一時ファイルを削除
        if 'tmp_file_path' in locals():
            try:
                os.unlink(tmp_file_path)
            except:
                pass
        return jsonify({'error': str(e)}), 500
