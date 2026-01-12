"""
貢献度分析モジュール

製品別・部門別の売上高、変動費、固定費から貢献度を分析します。
"""

from typing import Dict, List, Any


def calculate_contribution_margin(sales: float, variable_cost: float) -> float:
    """
    貢献利益を計算
    
    Args:
        sales: 売上高
        variable_cost: 変動費
    
    Returns:
        貢献利益
    """
    return sales - variable_cost


def calculate_contribution_margin_ratio(sales: float, variable_cost: float) -> float:
    """
    貢献利益率を計算
    
    Args:
        sales: 売上高
        variable_cost: 変動費
    
    Returns:
        貢献利益率（%）
    """
    if sales == 0:
        return 0.0
    
    contribution_margin = calculate_contribution_margin(sales, variable_cost)
    return (contribution_margin / sales) * 100


def calculate_segment_profit(sales: float, variable_cost: float, direct_fixed_cost: float) -> float:
    """
    セグメント利益を計算
    
    Args:
        sales: 売上高
        variable_cost: 変動費
        direct_fixed_cost: 直接固定費（個別固定費）
    
    Returns:
        セグメント利益
    """
    contribution_margin = calculate_contribution_margin(sales, variable_cost)
    return contribution_margin - direct_fixed_cost


def calculate_operating_profit(sales: float, variable_cost: float, direct_fixed_cost: float, common_fixed_cost: float) -> float:
    """
    営業利益を計算
    
    Args:
        sales: 売上高
        variable_cost: 変動費
        direct_fixed_cost: 直接固定費
        common_fixed_cost: 共通固定費
    
    Returns:
        営業利益
    """
    segment_profit = calculate_segment_profit(sales, variable_cost, direct_fixed_cost)
    return segment_profit - common_fixed_cost


def analyze_contribution_by_segment(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    セグメント別貢献度分析を実行
    
    Args:
        segments: セグメント情報のリスト
            各セグメントは以下のキーを持つ辞書:
            - name: セグメント名
            - sales: 売上高
            - variable_cost: 変動費
            - direct_fixed_cost: 直接固定費
    
    Returns:
        分析結果の辞書
    """
    total_sales = 0
    total_variable_cost = 0
    total_direct_fixed_cost = 0
    total_contribution_margin = 0
    total_segment_profit = 0
    
    segment_results = []
    
    for segment in segments:
        name = segment.get('name', '')
        sales = float(segment.get('sales', 0))
        variable_cost = float(segment.get('variable_cost', 0))
        direct_fixed_cost = float(segment.get('direct_fixed_cost', 0))
        
        contribution_margin = calculate_contribution_margin(sales, variable_cost)
        contribution_margin_ratio = calculate_contribution_margin_ratio(sales, variable_cost)
        segment_profit = calculate_segment_profit(sales, variable_cost, direct_fixed_cost)
        
        segment_results.append({
            'name': name,
            'sales': sales,
            'variable_cost': variable_cost,
            'direct_fixed_cost': direct_fixed_cost,
            'contribution_margin': contribution_margin,
            'contribution_margin_ratio': contribution_margin_ratio,
            'segment_profit': segment_profit
        })
        
        total_sales += sales
        total_variable_cost += variable_cost
        total_direct_fixed_cost += direct_fixed_cost
        total_contribution_margin += contribution_margin
        total_segment_profit += segment_profit
    
    # 売上構成比と貢献利益構成比を計算
    for result in segment_results:
        if total_sales > 0:
            result['sales_ratio'] = (result['sales'] / total_sales) * 100
        else:
            result['sales_ratio'] = 0.0
        
        if total_contribution_margin > 0:
            result['contribution_ratio'] = (result['contribution_margin'] / total_contribution_margin) * 100
        else:
            result['contribution_ratio'] = 0.0
    
    return {
        'segments': segment_results,
        'total': {
            'sales': total_sales,
            'variable_cost': total_variable_cost,
            'direct_fixed_cost': total_direct_fixed_cost,
            'contribution_margin': total_contribution_margin,
            'contribution_margin_ratio': calculate_contribution_margin_ratio(total_sales, total_variable_cost),
            'segment_profit': total_segment_profit
        }
    }


def analyze_product_mix(products: List[Dict[str, Any]], common_fixed_cost: float = 0) -> Dict[str, Any]:
    """
    製品ミックス分析を実行
    
    Args:
        products: 製品情報のリスト
        common_fixed_cost: 共通固定費
    
    Returns:
        分析結果の辞書
    """
    # セグメント別分析を実行
    segment_analysis = analyze_contribution_by_segment(products)
    
    # 営業利益を計算
    operating_profit = segment_analysis['total']['segment_profit'] - common_fixed_cost
    
    # 製品別の営業利益への貢献度を計算
    for product in segment_analysis['segments']:
        if operating_profit != 0:
            product['profit_contribution'] = (product['segment_profit'] / operating_profit) * 100 if operating_profit > 0 else 0
        else:
            product['profit_contribution'] = 0.0
    
    segment_analysis['total']['common_fixed_cost'] = common_fixed_cost
    segment_analysis['total']['operating_profit'] = operating_profit
    
    return segment_analysis


def rank_segments_by_contribution(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    セグメントを貢献利益の降順でランキング
    
    Args:
        segments: セグメント情報のリスト
    
    Returns:
        ランキング済みセグメントのリスト
    """
    return sorted(segments, key=lambda x: x.get('contribution_margin', 0), reverse=True)


def identify_unprofitable_segments(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    赤字セグメントを特定
    
    Args:
        segments: セグメント情報のリスト
    
    Returns:
        赤字セグメントのリスト
    """
    return [s for s in segments if s.get('segment_profit', 0) < 0]


def calculate_breakeven_sales_by_segment(variable_cost: float, direct_fixed_cost: float, sales: float) -> float:
    """
    セグメント別損益分岐点売上高を計算
    
    Args:
        variable_cost: 変動費
        direct_fixed_cost: 直接固定費
        sales: 売上高
    
    Returns:
        損益分岐点売上高
    """
    if sales == 0:
        return 0.0
    
    variable_cost_ratio = variable_cost / sales
    
    if variable_cost_ratio >= 1:
        return float('inf')
    
    return direct_fixed_cost / (1 - variable_cost_ratio)
