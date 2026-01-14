"""
製品別貢献度分析モジュール

製品別の売上高、変動費、固定費から限界利益と貢献利益を計算し、
採算性を評価します。
"""

from typing import Dict, List, Any


def calculate_marginal_profit(sales: float, variable_cost: float) -> float:
    """
    限界利益を計算
    
    Args:
        sales: 売上高
        variable_cost: 変動費
    
    Returns:
        限界利益（売上高 - 変動費）
    """
    return sales - variable_cost


def calculate_marginal_profit_ratio(sales: float, variable_cost: float) -> float:
    """
    限界利益率を計算
    
    Args:
        sales: 売上高
        variable_cost: 変動費
    
    Returns:
        限界利益率（%）
    """
    if sales == 0:
        return 0.0
    
    marginal_profit = calculate_marginal_profit(sales, variable_cost)
    return (marginal_profit / sales) * 100


def calculate_contribution_profit(sales: float, variable_cost: float, fixed_cost: float) -> float:
    """
    貢献利益を計算
    
    Args:
        sales: 売上高
        variable_cost: 変動費
        fixed_cost: 固定費
    
    Returns:
        貢献利益（限界利益 - 固定費）
    """
    marginal_profit = calculate_marginal_profit(sales, variable_cost)
    return marginal_profit - fixed_cost


def calculate_contribution_profit_ratio(sales: float, variable_cost: float, fixed_cost: float) -> float:
    """
    貢献利益率を計算
    
    Args:
        sales: 売上高
        variable_cost: 変動費
        fixed_cost: 固定費
    
    Returns:
        貢献利益率（%）
    """
    if sales == 0:
        return 0.0
    
    contribution_profit = calculate_contribution_profit(sales, variable_cost, fixed_cost)
    return (contribution_profit / sales) * 100


def evaluate_profitability(contribution_profit: float, contribution_profit_ratio: float) -> Dict[str, Any]:
    """
    採算性を評価
    
    Args:
        contribution_profit: 貢献利益
        contribution_profit_ratio: 貢献利益率
    
    Returns:
        dict: 評価結果
    """
    if contribution_profit >= 0:
        status = 'profitable'
        status_label = '採算確保'
        status_symbol = '○'
    else:
        status = 'unprofitable'
        status_label = '不採算'
        status_symbol = '×'
    
    # 貢献利益率に基づく詳細評価
    if contribution_profit_ratio >= 20:
        rating = 'excellent'
        rating_label = '優良'
        rating_symbol = '◎'
    elif contribution_profit_ratio >= 10:
        rating = 'good'
        rating_label = '良好'
        rating_symbol = '○'
    elif contribution_profit_ratio >= 0:
        rating = 'fair'
        rating_label = '普通'
        rating_symbol = '△'
    else:
        rating = 'poor'
        rating_label = '要改善'
        rating_symbol = '×'
    
    return {
        'status': status,
        'status_label': status_label,
        'status_symbol': status_symbol,
        'rating': rating,
        'rating_label': rating_label,
        'rating_symbol': rating_symbol
    }


def analyze_product_contribution(products: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    製品別貢献度分析を実行
    
    Args:
        products: 製品情報のリスト
            各製品は以下のキーを持つ辞書:
            - name: 製品名
            - sales: 売上高
            - variable_cost: 変動費
            - fixed_cost: 固定費（個別固定費）
    
    Returns:
        dict: 分析結果
    """
    total_sales = 0
    total_variable_cost = 0
    total_fixed_cost = 0
    total_marginal_profit = 0
    total_contribution_profit = 0
    
    product_results = []
    
    for product in products:
        name = product.get('name', '')
        sales = float(product.get('sales', 0))
        variable_cost = float(product.get('variable_cost', 0))
        fixed_cost = float(product.get('fixed_cost', 0))
        
        # 限界利益と限界利益率を計算
        marginal_profit = calculate_marginal_profit(sales, variable_cost)
        marginal_profit_ratio = calculate_marginal_profit_ratio(sales, variable_cost)
        
        # 貢献利益と貢献利益率を計算
        contribution_profit = calculate_contribution_profit(sales, variable_cost, fixed_cost)
        contribution_profit_ratio = calculate_contribution_profit_ratio(sales, variable_cost, fixed_cost)
        
        # 採算性を評価
        profitability = evaluate_profitability(contribution_profit, contribution_profit_ratio)
        
        product_results.append({
            'name': name,
            'sales': sales,
            'variable_cost': variable_cost,
            'fixed_cost': fixed_cost,
            'marginal_profit': marginal_profit,
            'marginal_profit_ratio': marginal_profit_ratio,
            'contribution_profit': contribution_profit,
            'contribution_profit_ratio': contribution_profit_ratio,
            'profitability_status': profitability['status'],
            'profitability_status_label': profitability['status_label'],
            'profitability_status_symbol': profitability['status_symbol'],
            'profitability_rating': profitability['rating'],
            'profitability_rating_label': profitability['rating_label'],
            'profitability_rating_symbol': profitability['rating_symbol']
        })
        
        total_sales += sales
        total_variable_cost += variable_cost
        total_fixed_cost += fixed_cost
        total_marginal_profit += marginal_profit
        total_contribution_profit += contribution_profit
    
    # 売上構成比と貢献利益構成比を計算
    for result in product_results:
        if total_sales > 0:
            result['sales_ratio'] = (result['sales'] / total_sales) * 100
        else:
            result['sales_ratio'] = 0.0
        
        if total_contribution_profit > 0:
            result['contribution_ratio'] = (result['contribution_profit'] / total_contribution_profit) * 100
        else:
            result['contribution_ratio'] = 0.0
    
    # 全体の限界利益率と貢献利益率を計算
    total_marginal_profit_ratio = calculate_marginal_profit_ratio(total_sales, total_variable_cost)
    total_contribution_profit_ratio = calculate_contribution_profit_ratio(total_sales, total_variable_cost, total_fixed_cost)
    
    return {
        'products': product_results,
        'total': {
            'sales': total_sales,
            'variable_cost': total_variable_cost,
            'fixed_cost': total_fixed_cost,
            'marginal_profit': total_marginal_profit,
            'marginal_profit_ratio': total_marginal_profit_ratio,
            'contribution_profit': total_contribution_profit,
            'contribution_profit_ratio': total_contribution_profit_ratio
        }
    }


def rank_products_by_contribution(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    製品を貢献利益の降順でランキング
    
    Args:
        products: 製品情報のリスト
    
    Returns:
        list: ランキング済み製品のリスト
    """
    return sorted(products, key=lambda x: x.get('contribution_profit', 0), reverse=True)


def identify_unprofitable_products(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    不採算製品を特定
    
    Args:
        products: 製品情報のリスト
    
    Returns:
        list: 不採算製品のリスト
    """
    return [p for p in products if p.get('contribution_profit', 0) < 0]


def calculate_breakeven_sales(variable_cost: float, fixed_cost: float, sales: float) -> float:
    """
    損益分岐点売上高を計算
    
    Args:
        variable_cost: 変動費
        fixed_cost: 固定費
        sales: 売上高
    
    Returns:
        float: 損益分岐点売上高
    """
    if sales == 0:
        return 0.0
    
    variable_cost_ratio = variable_cost / sales
    
    if variable_cost_ratio >= 1:
        return float('inf')
    
    return fixed_cost / (1 - variable_cost_ratio)


def format_product_contribution_for_ui(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    製品別貢献度分析結果をUI表示用に整形
    
    Args:
        analysis_result: 分析結果
    
    Returns:
        dict: UI表示用の整形済みデータ
    """
    # 製品別分析テーブルを整形
    product_table = []
    for product in analysis_result['products']:
        product_table.append({
            'name': product['name'],
            'sales': round(product['sales'], 2),
            'sales_formatted': f"{product['sales']:,.0f}円",
            'sales_ratio': round(product['sales_ratio'], 2),
            'sales_ratio_formatted': f"{product['sales_ratio']:.2f}%",
            'variable_cost': round(product['variable_cost'], 2),
            'variable_cost_formatted': f"{product['variable_cost']:,.0f}円",
            'fixed_cost': round(product['fixed_cost'], 2),
            'fixed_cost_formatted': f"{product['fixed_cost']:,.0f}円",
            'marginal_profit': round(product['marginal_profit'], 2),
            'marginal_profit_formatted': f"{product['marginal_profit']:,.0f}円",
            'marginal_profit_ratio': round(product['marginal_profit_ratio'], 2),
            'marginal_profit_ratio_formatted': f"{product['marginal_profit_ratio']:.2f}%",
            'contribution_profit': round(product['contribution_profit'], 2),
            'contribution_profit_formatted': f"{product['contribution_profit']:,.0f}円",
            'contribution_profit_ratio': round(product['contribution_profit_ratio'], 2),
            'contribution_profit_ratio_formatted': f"{product['contribution_profit_ratio']:.2f}%",
            'contribution_ratio': round(product['contribution_ratio'], 2),
            'contribution_ratio_formatted': f"{product['contribution_ratio']:.2f}%",
            'profitability_status': product['profitability_status'],
            'profitability_status_label': product['profitability_status_label'],
            'profitability_status_symbol': product['profitability_status_symbol'],
            'profitability_rating': product['profitability_rating'],
            'profitability_rating_label': product['profitability_rating_label'],
            'profitability_rating_symbol': product['profitability_rating_symbol']
        })
    
    return {
        'product_table': product_table,
        'total': {
            'sales': round(analysis_result['total']['sales'], 2),
            'sales_formatted': f"{analysis_result['total']['sales']:,.0f}円",
            'variable_cost': round(analysis_result['total']['variable_cost'], 2),
            'variable_cost_formatted': f"{analysis_result['total']['variable_cost']:,.0f}円",
            'fixed_cost': round(analysis_result['total']['fixed_cost'], 2),
            'fixed_cost_formatted': f"{analysis_result['total']['fixed_cost']:,.0f}円",
            'marginal_profit': round(analysis_result['total']['marginal_profit'], 2),
            'marginal_profit_formatted': f"{analysis_result['total']['marginal_profit']:,.0f}円",
            'marginal_profit_ratio': round(analysis_result['total']['marginal_profit_ratio'], 2),
            'marginal_profit_ratio_formatted': f"{analysis_result['total']['marginal_profit_ratio']:.2f}%",
            'contribution_profit': round(analysis_result['total']['contribution_profit'], 2),
            'contribution_profit_formatted': f"{analysis_result['total']['contribution_profit']:,.0f}円",
            'contribution_profit_ratio': round(analysis_result['total']['contribution_profit_ratio'], 2),
            'contribution_profit_ratio_formatted': f"{analysis_result['total']['contribution_profit_ratio']:.2f}%"
        }
    }
