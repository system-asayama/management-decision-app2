"""
経営指標分析Blueprint
成長力・収益力・資金力・生産力の4つの視点から評価記号付きで指標を提供
"""
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from app.models import Company, FiscalYear, ProfitLossStatement, BalanceSheet
from app.database import SessionLocal
from app.services.analysis_service import AnalysisService
from app.utils.evaluation_helpers import evaluate_multiple_indicators
from app.auth import require_roles, ROLES

bp = Blueprint('management_analysis', __name__, url_prefix='/decision/management-analysis')


@bp.route('/')
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def index():
    """経営指標分析ページ"""
    tenant_id = session.get('tenant_id')
    if not tenant_id:
        return redirect(url_for('decision.index'))
    
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.tenant_id == tenant_id).all()
        return render_template('management_analysis.html', companies=companies)
    finally:
        db.close()


@bp.route('/analyze', methods=['POST'])
@require_roles(ROLES["TENANT_ADMIN"], ROLES["SYSTEM_ADMIN"])
def analyze():
    """
    経営指標分析を実行
    
    Request Body:
        company_id: int - 企業ID
        current_fiscal_year_id: int - 当年度ID
        previous_fiscal_year_id: int - 前年度ID
    
    Response:
        growth: dict - 成長力指標（評価記号付き）
        profitability: dict - 収益力指標（評価記号付き）
        financial_strength: dict - 資金力指標（評価記号付き）
        productivity: dict - 生産力指標（評価記号付き）
    """
    data = request.json
    company_id = data.get('company_id')
    current_fiscal_year_id = data.get('current_fiscal_year_id')
    previous_fiscal_year_id = data.get('previous_fiscal_year_id')
    
    if not all([company_id, current_fiscal_year_id, previous_fiscal_year_id]):
        return jsonify({'error': '必須パラメータが不足しています'}), 400
    
    db = SessionLocal()
    try:
        # 当年度のデータを取得
        current_pl = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.company_id == company_id,
            ProfitLossStatement.fiscal_year_id == current_fiscal_year_id
        ).first()
        
        current_bs = db.query(BalanceSheet).filter(
            BalanceSheet.company_id == company_id,
            BalanceSheet.fiscal_year_id == current_fiscal_year_id
        ).first()
        
        # 前年度のデータを取得
        previous_pl = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.company_id == company_id,
            ProfitLossStatement.fiscal_year_id == previous_fiscal_year_id
        ).first()
        
        previous_bs = db.query(BalanceSheet).filter(
            BalanceSheet.company_id == company_id,
            BalanceSheet.fiscal_year_id == previous_fiscal_year_id
        ).first()
        
        if not all([current_pl, current_bs, previous_pl, previous_bs]):
            return jsonify({'error': '財務データが不足しています'}), 404
        
        # 当年度のデータを辞書に変換
        current_data = _convert_to_dict(current_pl, current_bs)
        previous_data = _convert_to_dict(previous_pl, previous_bs)
        
        # 各視点の指標を計算
        growth_indicators = AnalysisService.calculate_growth_indicators(current_data, previous_data)
        profitability_indicators = AnalysisService.calculate_profitability_indicators(current_data)
        financial_strength_indicators = AnalysisService.calculate_financial_strength_indicators(current_data)
        productivity_indicators = AnalysisService.calculate_productivity_indicators(current_data)
        
        # 前年度の指標も計算（比較用）
        previous_profitability = AnalysisService.calculate_profitability_indicators(previous_data)
        previous_financial_strength = AnalysisService.calculate_financial_strength_indicators(previous_data)
        previous_productivity = AnalysisService.calculate_productivity_indicators(previous_data)
        
        # 評価記号を付与
        growth_with_grades = {}
        for key, value in growth_indicators.items():
            growth_with_grades[key] = {
                'value': value,
                'grade': _get_grade_for_growth_rate(value)
            }
        
        profitability_with_grades = evaluate_multiple_indicators(
            profitability_indicators,
            previous_profitability
        )
        
        financial_strength_with_grades = evaluate_multiple_indicators(
            financial_strength_indicators,
            previous_financial_strength
        )
        
        productivity_with_grades = evaluate_multiple_indicators(
            productivity_indicators,
            previous_productivity
        )
        
        return jsonify({
            'growth': growth_with_grades,
            'profitability': profitability_with_grades,
            'financial_strength': financial_strength_with_grades,
            'productivity': productivity_with_grades
        })
    
    finally:
        db.close()


def _convert_to_dict(pl: ProfitLossStatement, bs: BalanceSheet) -> dict:
    """PL/BSモデルを辞書に変換"""
    return {
        # PL項目
        'sales': pl.sales or 0,
        'cost_of_sales': pl.cost_of_sales or 0,
        'gross_profit': pl.gross_profit or 0,
        'selling_general_admin_expenses': pl.selling_general_admin_expenses or 0,
        'operating_income': pl.operating_income or 0,
        'non_operating_income': pl.non_operating_income or 0,
        'non_operating_expenses': pl.non_operating_expenses or 0,
        'ordinary_income': pl.ordinary_income or 0,
        'extraordinary_income': pl.extraordinary_income or 0,
        'extraordinary_losses': pl.extraordinary_losses or 0,
        'income_before_tax': pl.income_before_tax or 0,
        'corporate_tax': pl.corporate_tax or 0,
        'net_income': pl.net_income or 0,
        
        # BS項目
        'total_assets': bs.total_assets or 0,
        'current_assets': bs.current_assets or 0,
        'fixed_assets': bs.fixed_assets or 0,
        'total_liabilities': bs.total_liabilities or 0,
        'current_liabilities': bs.current_liabilities or 0,
        'fixed_liabilities': bs.fixed_liabilities or 0,
        'net_assets': bs.net_assets or 0,
        
        # その他（仮の値、実際のモデルに合わせて調整）
        'gross_added_value': (pl.gross_profit or 0) + (pl.selling_general_admin_expenses or 0),
        'total_labor_cost': 0,  # 労務費データが必要
        'executive_compensation': 0,  # 役員報酬データが必要
        'capital_regeneration_cost': 0,  # 資本再生産費用データが必要
        'research_development_expenses': 0,  # 研究開発費データが必要
        'general_expenses': pl.selling_general_admin_expenses or 0,
        'number_of_employees': 0,  # 従業員数データが必要
    }


def _get_grade_for_growth_rate(growth_rate: float) -> str:
    """成長率に基づいて評価記号を返す"""
    if growth_rate >= 10.0:
        return '◎'
    elif growth_rate >= 0.0:
        return '◯'
    elif growth_rate >= -10.0:
        return '△'
    else:
        return '×'
