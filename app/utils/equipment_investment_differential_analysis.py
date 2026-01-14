"""
設備投資の差額原価収益分析モジュール

設備投資案と現状案を比較し、人件費削減額・減価償却費・税効果を考慮した
正味効果（差額利益）を複数年にわたって分析します。
"""

from typing import Dict, List, Any


def calculate_equipment_investment_differential_analysis(
    equipment_cost: float,
    useful_life: int,
    current_labor_cost: float,
    new_labor_cost: float,
    tax_rate: float,
    discount_rate: float,
    depreciation_method: str = 'straight_line'
) -> Dict[str, Any]:
    """
    設備投資の差額原価収益分析を実行
    
    Args:
        equipment_cost: 設備投資額
        useful_life: 耐用年数（年）
        current_labor_cost: 現状の年間労務費
        new_labor_cost: 投資後の年間労務費
        tax_rate: 税率（%）
        discount_rate: 割引率（%）
        depreciation_method: 減価償却方法（'straight_line': 定額法）
    
    Returns:
        dict: 差額原価収益分析結果
    """
    tax_rate_decimal = tax_rate / 100
    discount_rate_decimal = discount_rate / 100
    
    # 年間労務費削減額
    annual_labor_cost_savings = current_labor_cost - new_labor_cost
    
    # 年間減価償却費（定額法）
    annual_depreciation = equipment_cost / useful_life
    
    # 年次分析データを生成
    yearly_analysis = []
    cumulative_npv = 0
    
    for year in range(useful_life + 1):
        if year == 0:
            # 初年度（投資時点）
            yearly_analysis.append({
                'year': year,
                'equipment_investment': -equipment_cost,
                'labor_cost_savings': 0,
                'depreciation': 0,
                'income_increase': 0,
                'tax_shield': 0,
                'net_cash_flow': -equipment_cost,
                'discount_factor': 1.0,
                'present_value': -equipment_cost,
                'cumulative_npv': -equipment_cost
            })
            cumulative_npv = -equipment_cost
        else:
            # 各年度
            # 所得増加額 = 労務費削減額 - 減価償却費
            income_increase = annual_labor_cost_savings - annual_depreciation
            
            # タックスシールド（税負担軽減効果） = 減価償却費 × 税率
            tax_shield = annual_depreciation * tax_rate_decimal
            
            # 純キャッシュフロー = 労務費削減額 - タックスシールド
            # （減価償却費は非現金支出なので除外）
            net_cash_flow = annual_labor_cost_savings - (income_increase * tax_rate_decimal)
            
            # 割引係数
            discount_factor = 1 / ((1 + discount_rate_decimal) ** year)
            
            # 現在価値
            present_value = net_cash_flow * discount_factor
            
            # 累積NPV
            cumulative_npv += present_value
            
            yearly_analysis.append({
                'year': year,
                'equipment_investment': 0,
                'labor_cost_savings': annual_labor_cost_savings,
                'depreciation': annual_depreciation,
                'income_increase': income_increase,
                'tax_shield': tax_shield,
                'net_cash_flow': net_cash_flow,
                'discount_factor': discount_factor,
                'present_value': present_value,
                'cumulative_npv': cumulative_npv
            })
    
    # 最終NPV
    final_npv = cumulative_npv
    
    # IRR（内部収益率）を計算
    cash_flows = [-equipment_cost] + [annual_labor_cost_savings - (income_increase * tax_rate_decimal)] * useful_life
    irr = calculate_irr_simple(cash_flows)
    
    # 投資判断
    recommendation = 'accept' if final_npv > 0 else 'reject'
    recommendation_text = get_investment_recommendation_text(final_npv, irr, discount_rate)
    
    return {
        'equipment_cost': equipment_cost,
        'useful_life': useful_life,
        'current_labor_cost': current_labor_cost,
        'new_labor_cost': new_labor_cost,
        'annual_labor_cost_savings': annual_labor_cost_savings,
        'annual_depreciation': annual_depreciation,
        'tax_rate': tax_rate,
        'discount_rate': discount_rate,
        'yearly_analysis': yearly_analysis,
        'final_npv': final_npv,
        'irr': irr,
        'recommendation': recommendation,
        'recommendation_text': recommendation_text
    }


def compare_multiple_equipment_investments(
    investment_plans: List[Dict[str, Any]],
    tax_rate: float,
    discount_rate: float
) -> Dict[str, Any]:
    """
    複数の設備投資案を比較
    
    Args:
        investment_plans: 投資案リスト
        tax_rate: 税率（%）
        discount_rate: 割引率（%）
    
    Returns:
        dict: 比較分析結果
    """
    results = []
    
    for plan in investment_plans:
        result = calculate_equipment_investment_differential_analysis(
            equipment_cost=plan['equipment_cost'],
            useful_life=plan['useful_life'],
            current_labor_cost=plan['current_labor_cost'],
            new_labor_cost=plan['new_labor_cost'],
            tax_rate=tax_rate,
            discount_rate=discount_rate
        )
        result['plan_name'] = plan.get('name', f"投資案{len(results) + 1}")
        results.append(result)
    
    # NPVの降順でソート
    results.sort(key=lambda x: x['final_npv'], reverse=True)
    
    # 最適案を選定
    best_plan = results[0] if results else None
    
    return {
        'investment_plans': results,
        'best_plan': best_plan,
        'comparison_summary': generate_comparison_summary(results)
    }


def calculate_irr_simple(cash_flows: List[float], max_iterations: int = 1000, tolerance: float = 0.0001) -> float:
    """
    IRR（内部収益率）を簡易的に計算
    
    Args:
        cash_flows: キャッシュフローリスト
        max_iterations: 最大反復回数
        tolerance: 許容誤差
    
    Returns:
        float: IRR（%）
    """
    # 初期値を設定（10%からスタート）
    rate = 0.1
    
    for _ in range(max_iterations):
        # NPVを計算
        npv = sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cash_flows))
        
        # 収束判定
        if abs(npv) < tolerance:
            return rate * 100
        
        # NPVの微分を計算
        npv_derivative = sum(-i * cf / ((1 + rate) ** (i + 1)) for i, cf in enumerate(cash_flows))
        
        # ニュートン法で次の値を計算
        if npv_derivative != 0:
            rate = rate - npv / npv_derivative
        else:
            break
    
    # 収束しない場合はNaNを返す
    return float('nan')


def get_investment_recommendation_text(npv: float, irr: float, discount_rate: float) -> str:
    """
    投資判断の推奨テキストを生成
    
    Args:
        npv: 正味現在価値
        irr: 内部収益率
        discount_rate: 割引率
    
    Returns:
        str: 推奨テキスト
    """
    recommendations = []
    
    if npv > 0:
        recommendations.append(f"NPVがプラス（{npv:,.0f}円）であり、投資価値があります。")
    else:
        recommendations.append(f"NPVがマイナス（{npv:,.0f}円）であり、投資は推奨されません。")
    
    if not (irr != irr):  # NaNチェック
        if irr > discount_rate:
            recommendations.append(f"IRRが{irr:.2f}%で割引率{discount_rate:.2f}%を上回っており、投資効率が良好です。")
        else:
            recommendations.append(f"IRRが{irr:.2f}%で割引率{discount_rate:.2f}%を下回っており、投資効率が低いです。")
    
    return " ".join(recommendations)


def generate_comparison_summary(results: List[Dict[str, Any]]) -> str:
    """
    比較分析のサマリーテキストを生成
    
    Args:
        results: 分析結果リスト
    
    Returns:
        str: サマリーテキスト
    """
    if not results:
        return "比較対象の投資案がありません。"
    
    best_plan = results[0]
    summary_lines = []
    
    summary_lines.append(f"最適案: {best_plan['plan_name']}")
    summary_lines.append(f"  - NPV: {best_plan['final_npv']:,.0f}円")
    summary_lines.append(f"  - IRR: {best_plan['irr']:.2f}%")
    summary_lines.append(f"  - 設備投資額: {best_plan['equipment_cost']:,.0f}円")
    summary_lines.append(f"  - 年間労務費削減額: {best_plan['annual_labor_cost_savings']:,.0f}円")
    
    if len(results) > 1:
        summary_lines.append(f"\n他の投資案との比較:")
        for i, plan in enumerate(results[1:], start=2):
            npv_diff = best_plan['final_npv'] - plan['final_npv']
            summary_lines.append(f"  {i}. {plan['plan_name']}: NPV {plan['final_npv']:,.0f}円（差額 {npv_diff:,.0f}円）")
    
    return "\n".join(summary_lines)


def format_differential_analysis_for_ui(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    差額原価収益分析結果をUI表示用に整形
    
    Args:
        analysis_result: 分析結果
    
    Returns:
        dict: UI表示用の整形済みデータ
    """
    # 年次分析テーブルを整形
    yearly_table = []
    for row in analysis_result['yearly_analysis']:
        yearly_table.append({
            'year': row['year'],
            'year_label': f"{row['year']}年目" if row['year'] > 0 else "初年度",
            'equipment_investment': round(row['equipment_investment'], 2),
            'equipment_investment_formatted': f"{row['equipment_investment']:,.0f}円",
            'labor_cost_savings': round(row['labor_cost_savings'], 2),
            'labor_cost_savings_formatted': f"{row['labor_cost_savings']:,.0f}円",
            'depreciation': round(row['depreciation'], 2),
            'depreciation_formatted': f"{row['depreciation']:,.0f}円",
            'income_increase': round(row['income_increase'], 2),
            'income_increase_formatted': f"{row['income_increase']:,.0f}円",
            'tax_shield': round(row['tax_shield'], 2),
            'tax_shield_formatted': f"{row['tax_shield']:,.0f}円",
            'net_cash_flow': round(row['net_cash_flow'], 2),
            'net_cash_flow_formatted': f"{row['net_cash_flow']:,.0f}円",
            'present_value': round(row['present_value'], 2),
            'present_value_formatted': f"{row['present_value']:,.0f}円",
            'cumulative_npv': round(row['cumulative_npv'], 2),
            'cumulative_npv_formatted': f"{row['cumulative_npv']:,.0f}円"
        })
    
    return {
        'summary': {
            'equipment_cost': round(analysis_result['equipment_cost'], 2),
            'equipment_cost_formatted': f"{analysis_result['equipment_cost']:,.0f}円",
            'useful_life': analysis_result['useful_life'],
            'annual_labor_cost_savings': round(analysis_result['annual_labor_cost_savings'], 2),
            'annual_labor_cost_savings_formatted': f"{analysis_result['annual_labor_cost_savings']:,.0f}円",
            'annual_depreciation': round(analysis_result['annual_depreciation'], 2),
            'annual_depreciation_formatted': f"{analysis_result['annual_depreciation']:,.0f}円",
            'final_npv': round(analysis_result['final_npv'], 2),
            'final_npv_formatted': f"{analysis_result['final_npv']:,.0f}円",
            'irr': round(analysis_result['irr'], 2) if not (analysis_result['irr'] != analysis_result['irr']) else None,
            'irr_formatted': f"{analysis_result['irr']:.2f}%" if not (analysis_result['irr'] != analysis_result['irr']) else "N/A",
            'recommendation': analysis_result['recommendation'],
            'recommendation_label': '投資を推奨' if analysis_result['recommendation'] == 'accept' else '投資を非推奨',
            'recommendation_text': analysis_result['recommendation_text']
        },
        'yearly_table': yearly_table
    }
