"""
設備投資計画モジュール

設備投資の経済性評価を行います。
"""

from typing import Dict, List, Any
import math


def calculate_npv(
    initial_investment: float,
    annual_cash_flows: List[float],
    discount_rate: float
) -> float:
    """
    正味現在価値（NPV: Net Present Value）を計算
    
    Args:
        initial_investment: 初期投資額
        annual_cash_flows: 年次キャッシュフローのリスト
        discount_rate: 割引率（%）
    
    Returns:
        正味現在価値
    """
    rate = discount_rate / 100
    
    # 将来キャッシュフローの現在価値を計算
    pv_cash_flows = sum(
        cf / ((1 + rate) ** (i + 1))
        for i, cf in enumerate(annual_cash_flows)
    )
    
    # NPV = 現在価値の合計 - 初期投資額
    npv = pv_cash_flows - initial_investment
    
    return npv


def calculate_irr(
    initial_investment: float,
    annual_cash_flows: List[float],
    max_iterations: int = 1000,
    tolerance: float = 0.0001
) -> float:
    """
    内部収益率（IRR: Internal Rate of Return）を計算
    ニュートン法を使用して近似値を求める
    
    Args:
        initial_investment: 初期投資額
        annual_cash_flows: 年次キャッシュフローのリスト
        max_iterations: 最大反復回数
        tolerance: 許容誤差
    
    Returns:
        内部収益率（%）
    """
    # 初期値を設定（10%からスタート）
    rate = 0.1
    
    for _ in range(max_iterations):
        # NPVを計算
        npv = -initial_investment
        npv_derivative = 0
        
        for i, cf in enumerate(annual_cash_flows):
            period = i + 1
            npv += cf / ((1 + rate) ** period)
            npv_derivative -= period * cf / ((1 + rate) ** (period + 1))
        
        # 収束判定
        if abs(npv) < tolerance:
            return rate * 100
        
        # ニュートン法で次の値を計算
        if npv_derivative != 0:
            rate = rate - npv / npv_derivative
        else:
            break
    
    # 収束しない場合はNaNを返す
    return float('nan')


def calculate_payback_period(
    initial_investment: float,
    annual_cash_flows: List[float]
) -> float:
    """
    回収期間を計算
    
    Args:
        initial_investment: 初期投資額
        annual_cash_flows: 年次キャッシュフローのリスト
    
    Returns:
        回収期間（年）
    """
    cumulative_cash_flow = 0
    
    for i, cf in enumerate(annual_cash_flows):
        cumulative_cash_flow += cf
        
        if cumulative_cash_flow >= initial_investment:
            # 線形補間で正確な回収期間を計算
            previous_cumulative = cumulative_cash_flow - cf
            remaining = initial_investment - previous_cumulative
            fraction = remaining / cf if cf > 0 else 0
            
            return i + fraction
    
    # 回収できない場合
    return float('inf')


def calculate_profitability_index(
    initial_investment: float,
    annual_cash_flows: List[float],
    discount_rate: float
) -> float:
    """
    収益性指数（PI: Profitability Index）を計算
    
    Args:
        initial_investment: 初期投資額
        annual_cash_flows: 年次キャッシュフローのリスト
        discount_rate: 割引率（%）
    
    Returns:
        収益性指数
    """
    rate = discount_rate / 100
    
    # 将来キャッシュフローの現在価値を計算
    pv_cash_flows = sum(
        cf / ((1 + rate) ** (i + 1))
        for i, cf in enumerate(annual_cash_flows)
    )
    
    # PI = 現在価値の合計 / 初期投資額
    if initial_investment == 0:
        return 0.0
    
    return pv_cash_flows / initial_investment


def evaluate_investment(
    initial_investment: float,
    annual_cash_flows: List[float],
    discount_rate: float,
    project_name: str = "投資案件"
) -> Dict[str, Any]:
    """
    設備投資案件を総合評価
    
    Args:
        initial_investment: 初期投資額
        annual_cash_flows: 年次キャッシュフローのリスト
        discount_rate: 割引率（%）
        project_name: 案件名
    
    Returns:
        評価結果の辞書
    """
    # NPVを計算
    npv = calculate_npv(initial_investment, annual_cash_flows, discount_rate)
    
    # IRRを計算
    irr = calculate_irr(initial_investment, annual_cash_flows)
    
    # 回収期間を計算
    payback_period = calculate_payback_period(initial_investment, annual_cash_flows)
    
    # 収益性指数を計算
    profitability_index = calculate_profitability_index(initial_investment, annual_cash_flows, discount_rate)
    
    # 総キャッシュフロー
    total_cash_flow = sum(annual_cash_flows)
    
    # 投資判断
    recommendation = get_investment_recommendation(npv, irr, discount_rate, payback_period)
    
    return {
        'project_name': project_name,
        'initial_investment': initial_investment,
        'annual_cash_flows': annual_cash_flows,
        'discount_rate': discount_rate,
        'npv': npv,
        'irr': irr,
        'payback_period': payback_period,
        'profitability_index': profitability_index,
        'total_cash_flow': total_cash_flow,
        'net_profit': total_cash_flow - initial_investment,
        'recommendation': recommendation
    }


def compare_investments(
    investments: List[Dict[str, Any]],
    discount_rate: float
) -> List[Dict[str, Any]]:
    """
    複数の投資案件を比較
    
    Args:
        investments: 投資案件のリスト
        discount_rate: 割引率（%）
    
    Returns:
        評価結果のリスト（NPVの降順）
    """
    results = []
    
    for inv in investments:
        result = evaluate_investment(
            initial_investment=inv['initial_investment'],
            annual_cash_flows=inv['annual_cash_flows'],
            discount_rate=discount_rate,
            project_name=inv.get('name', '投資案件')
        )
        results.append(result)
    
    # NPVの降順でソート
    results.sort(key=lambda x: x['npv'], reverse=True)
    
    return results


def get_investment_recommendation(
    npv: float,
    irr: float,
    discount_rate: float,
    payback_period: float
) -> str:
    """
    投資判断の推奨事項を取得
    
    Args:
        npv: 正味現在価値
        irr: 内部収益率
        discount_rate: 割引率
        payback_period: 回収期間
    
    Returns:
        推奨事項の文字列
    """
    recommendations = []
    
    # NPVによる判断
    if npv > 0:
        recommendations.append(f"NPVがプラス（{npv:,.0f}円）であり、投資価値があります。")
    else:
        recommendations.append(f"NPVがマイナス（{npv:,.0f}円）であり、投資は推奨されません。")
    
    # IRRによる判断
    if not math.isnan(irr):
        if irr > discount_rate:
            recommendations.append(f"IRR（{irr:.2f}%）が割引率（{discount_rate:.2f}%）を上回っており、投資効率が良好です。")
        else:
            recommendations.append(f"IRR（{irr:.2f}%）が割引率（{discount_rate:.2f}%）を下回っており、投資効率が低いです。")
    
    # 回収期間による判断
    if payback_period != float('inf'):
        if payback_period <= 3:
            recommendations.append(f"回収期間が{payback_period:.1f}年と短く、リスクが低いです。")
        elif payback_period <= 5:
            recommendations.append(f"回収期間が{payback_period:.1f}年と適正範囲内です。")
        else:
            recommendations.append(f"回収期間が{payback_period:.1f}年と長く、リスクが高いです。")
    else:
        recommendations.append("投資期間内に回収できません。")
    
    return " ".join(recommendations)


def calculate_depreciation(
    asset_cost: float,
    salvage_value: float,
    useful_life: int,
    method: str = 'straight_line'
) -> List[Dict[str, float]]:
    """
    減価償却を計算
    
    Args:
        asset_cost: 資産取得価額
        salvage_value: 残存価額
        useful_life: 耐用年数
        method: 償却方法（'straight_line': 定額法、'declining_balance': 定率法）
    
    Returns:
        年次減価償却費のリスト
    """
    depreciation_schedule = []
    depreciable_amount = asset_cost - salvage_value
    
    if method == 'straight_line':
        # 定額法
        annual_depreciation = depreciable_amount / useful_life
        
        for year in range(1, useful_life + 1):
            depreciation_schedule.append({
                'year': year,
                'depreciation': annual_depreciation,
                'accumulated_depreciation': annual_depreciation * year,
                'book_value': asset_cost - (annual_depreciation * year)
            })
    
    elif method == 'declining_balance':
        # 定率法（200%定率法）
        rate = 2.0 / useful_life
        book_value = asset_cost
        accumulated_depreciation = 0
        
        for year in range(1, useful_life + 1):
            depreciation = book_value * rate
            
            # 最終年度の調整
            if year == useful_life:
                depreciation = book_value - salvage_value
            
            accumulated_depreciation += depreciation
            book_value -= depreciation
            
            depreciation_schedule.append({
                'year': year,
                'depreciation': depreciation,
                'accumulated_depreciation': accumulated_depreciation,
                'book_value': book_value
            })
    
    return depreciation_schedule


def calculate_equipment_replacement(
    old_equipment_book_value: float,
    old_equipment_salvage_value: float,
    old_equipment_annual_cost: float,
    new_equipment_cost: float,
    new_equipment_salvage_value: float,
    new_equipment_annual_cost: float,
    useful_life: int,
    discount_rate: float
) -> Dict[str, Any]:
    """
    設備更新の経済性を評価
    
    Args:
        old_equipment_book_value: 旧設備の帳簿価額
        old_equipment_salvage_value: 旧設備の売却価額
        old_equipment_annual_cost: 旧設備の年間運転費用
        new_equipment_cost: 新設備の取得価額
        new_equipment_salvage_value: 新設備の残存価額
        new_equipment_annual_cost: 新設備の年間運転費用
        useful_life: 新設備の耐用年数
        discount_rate: 割引率（%）
    
    Returns:
        更新評価結果の辞書
    """
    # 旧設備継続時のキャッシュフロー
    old_cash_flows = [-old_equipment_annual_cost] * useful_life
    
    # 新設備導入時のキャッシュフロー
    initial_outlay = new_equipment_cost - old_equipment_salvage_value
    annual_savings = old_equipment_annual_cost - new_equipment_annual_cost
    new_cash_flows = [annual_savings] * useful_life
    new_cash_flows[-1] += new_equipment_salvage_value  # 最終年度に残存価額を加算
    
    # NPVを計算
    npv = calculate_npv(initial_outlay, new_cash_flows, discount_rate)
    
    # 総コスト比較
    old_total_cost = old_equipment_annual_cost * useful_life
    new_total_cost = initial_outlay + (new_equipment_annual_cost * useful_life) - new_equipment_salvage_value
    
    return {
        'old_equipment': {
            'book_value': old_equipment_book_value,
            'salvage_value': old_equipment_salvage_value,
            'annual_cost': old_equipment_annual_cost,
            'total_cost': old_total_cost
        },
        'new_equipment': {
            'cost': new_equipment_cost,
            'salvage_value': new_equipment_salvage_value,
            'annual_cost': new_equipment_annual_cost,
            'total_cost': new_total_cost
        },
        'initial_outlay': initial_outlay,
        'annual_savings': annual_savings,
        'npv': npv,
        'cost_savings': old_total_cost - new_total_cost,
        'recommendation': 'replace' if npv > 0 else 'keep',
        'recommendation_text': get_replacement_recommendation(npv, annual_savings)
    }


def get_replacement_recommendation(npv: float, annual_savings: float) -> str:
    """
    設備更新の推奨事項を取得
    
    Args:
        npv: 正味現在価値
        annual_savings: 年間節約額
    
    Returns:
        推奨事項の文字列
    """
    if npv > 0:
        return f"設備更新により、NPV {npv:,.0f}円の価値が創出されます。年間{annual_savings:,.0f}円のコスト削減が見込まれるため、更新を推奨します。"
    else:
        return f"設備更新のNPVは{npv:,.0f}円とマイナスです。現状維持を推奨します。"
