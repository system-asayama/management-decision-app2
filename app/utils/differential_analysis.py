"""
差額原価収益分析モジュール

複数のシナリオを比較し、差額利益を分析します。
"""

from typing import Dict, List, Any


def calculate_differential_profit(
    scenario_a_sales: float,
    scenario_a_variable_cost: float,
    scenario_a_fixed_cost: float,
    scenario_b_sales: float,
    scenario_b_variable_cost: float,
    scenario_b_fixed_cost: float
) -> Dict[str, Any]:
    """
    2つのシナリオの差額利益を計算
    
    Args:
        scenario_a_sales: シナリオAの売上高
        scenario_a_variable_cost: シナリオAの変動費
        scenario_a_fixed_cost: シナリオAの固定費
        scenario_b_sales: シナリオBの売上高
        scenario_b_variable_cost: シナリオBの変動費
        scenario_b_fixed_cost: シナリオBの固定費
    
    Returns:
        差額分析結果の辞書
    """
    # シナリオAの利益計算
    scenario_a_contribution_margin = scenario_a_sales - scenario_a_variable_cost
    scenario_a_profit = scenario_a_contribution_margin - scenario_a_fixed_cost
    
    # シナリオBの利益計算
    scenario_b_contribution_margin = scenario_b_sales - scenario_b_variable_cost
    scenario_b_profit = scenario_b_contribution_margin - scenario_b_fixed_cost
    
    # 差額計算
    differential_sales = scenario_b_sales - scenario_a_sales
    differential_variable_cost = scenario_b_variable_cost - scenario_a_variable_cost
    differential_fixed_cost = scenario_b_fixed_cost - scenario_a_fixed_cost
    differential_contribution_margin = scenario_b_contribution_margin - scenario_a_contribution_margin
    differential_profit = scenario_b_profit - scenario_a_profit
    
    return {
        'scenario_a': {
            'sales': scenario_a_sales,
            'variable_cost': scenario_a_variable_cost,
            'fixed_cost': scenario_a_fixed_cost,
            'contribution_margin': scenario_a_contribution_margin,
            'profit': scenario_a_profit
        },
        'scenario_b': {
            'sales': scenario_b_sales,
            'variable_cost': scenario_b_variable_cost,
            'fixed_cost': scenario_b_fixed_cost,
            'contribution_margin': scenario_b_contribution_margin,
            'profit': scenario_b_profit
        },
        'differential': {
            'sales': differential_sales,
            'variable_cost': differential_variable_cost,
            'fixed_cost': differential_fixed_cost,
            'contribution_margin': differential_contribution_margin,
            'profit': differential_profit
        },
        'recommendation': get_recommendation(differential_profit)
    }


def analyze_make_or_buy(
    make_variable_cost: float,
    make_fixed_cost: float,
    buy_price: float,
    quantity: int
) -> Dict[str, Any]:
    """
    自製か購入かの意思決定分析
    
    Args:
        make_variable_cost: 自製時の単位変動費
        make_fixed_cost: 自製時の固定費
        buy_price: 購入時の単価
        quantity: 数量
    
    Returns:
        分析結果の辞書
    """
    # 自製時のコスト
    make_total_cost = (make_variable_cost * quantity) + make_fixed_cost
    make_unit_cost = make_total_cost / quantity if quantity > 0 else 0
    
    # 購入時のコスト
    buy_total_cost = buy_price * quantity
    buy_unit_cost = buy_price
    
    # 差額
    differential_cost = buy_total_cost - make_total_cost
    
    # 損益分岐点数量（固定費を回収できる数量）
    if buy_price > make_variable_cost:
        breakeven_quantity = make_fixed_cost / (buy_price - make_variable_cost)
    else:
        breakeven_quantity = float('inf')
    
    return {
        'make': {
            'total_cost': make_total_cost,
            'unit_cost': make_unit_cost,
            'variable_cost': make_variable_cost * quantity,
            'fixed_cost': make_fixed_cost
        },
        'buy': {
            'total_cost': buy_total_cost,
            'unit_cost': buy_unit_cost
        },
        'differential': {
            'cost': differential_cost,
            'savings': -differential_cost
        },
        'breakeven_quantity': breakeven_quantity,
        'recommendation': 'buy' if differential_cost < 0 else 'make',
        'recommendation_text': get_make_or_buy_recommendation(differential_cost, breakeven_quantity, quantity)
    }


def analyze_accept_or_reject_order(
    regular_price: float,
    special_order_price: float,
    variable_cost: float,
    quantity: int,
    additional_fixed_cost: float = 0
) -> Dict[str, Any]:
    """
    特別注文の受諾可否分析
    
    Args:
        regular_price: 通常販売価格
        special_order_price: 特別注文価格
        variable_cost: 単位変動費
        quantity: 数量
        additional_fixed_cost: 追加固定費
    
    Returns:
        分析結果の辞書
    """
    # 通常注文の利益
    regular_contribution_margin = (regular_price - variable_cost) * quantity
    regular_profit = regular_contribution_margin
    
    # 特別注文の利益
    special_contribution_margin = (special_order_price - variable_cost) * quantity
    special_profit = special_contribution_margin - additional_fixed_cost
    
    # 差額利益
    differential_profit = special_profit
    
    return {
        'regular': {
            'price': regular_price,
            'contribution_margin': regular_contribution_margin,
            'profit': regular_profit
        },
        'special_order': {
            'price': special_order_price,
            'contribution_margin': special_contribution_margin,
            'additional_fixed_cost': additional_fixed_cost,
            'profit': special_profit
        },
        'differential': {
            'profit': differential_profit
        },
        'recommendation': 'accept' if differential_profit > 0 else 'reject',
        'recommendation_text': get_accept_or_reject_recommendation(differential_profit, special_order_price, variable_cost)
    }


def analyze_continue_or_discontinue(
    sales: float,
    variable_cost: float,
    direct_fixed_cost: float,
    avoidable_fixed_cost: float,
    unavoidable_fixed_cost: float
) -> Dict[str, Any]:
    """
    事業継続・撤退の意思決定分析
    
    Args:
        sales: 売上高
        variable_cost: 変動費
        direct_fixed_cost: 直接固定費
        avoidable_fixed_cost: 回避可能固定費
        unavoidable_fixed_cost: 回避不可能固定費
    
    Returns:
        分析結果の辞書
    """
    # 継続時の利益
    contribution_margin = sales - variable_cost
    continue_profit = contribution_margin - direct_fixed_cost - avoidable_fixed_cost - unavoidable_fixed_cost
    
    # 撤退時の利益（損失）
    discontinue_profit = -unavoidable_fixed_cost
    
    # 差額利益
    differential_profit = continue_profit - discontinue_profit
    
    return {
        'continue': {
            'sales': sales,
            'variable_cost': variable_cost,
            'contribution_margin': contribution_margin,
            'direct_fixed_cost': direct_fixed_cost,
            'avoidable_fixed_cost': avoidable_fixed_cost,
            'unavoidable_fixed_cost': unavoidable_fixed_cost,
            'profit': continue_profit
        },
        'discontinue': {
            'unavoidable_fixed_cost': unavoidable_fixed_cost,
            'profit': discontinue_profit
        },
        'differential': {
            'profit': differential_profit
        },
        'recommendation': 'continue' if differential_profit > 0 else 'discontinue',
        'recommendation_text': get_continue_or_discontinue_recommendation(differential_profit, contribution_margin, avoidable_fixed_cost)
    }


def get_recommendation(differential_profit: float) -> str:
    """
    差額利益に基づく推奨事項を取得
    
    Args:
        differential_profit: 差額利益
    
    Returns:
        推奨事項の文字列
    """
    if differential_profit > 0:
        return "シナリオBを選択することで、利益が増加します。"
    elif differential_profit < 0:
        return "シナリオAを選択することで、利益が増加します。"
    else:
        return "両シナリオの利益は同じです。"


def get_make_or_buy_recommendation(differential_cost: float, breakeven_quantity: float, quantity: int) -> str:
    """
    自製か購入かの推奨事項を取得
    
    Args:
        differential_cost: 差額コスト
        breakeven_quantity: 損益分岐点数量
        quantity: 数量
    
    Returns:
        推奨事項の文字列
    """
    if differential_cost < 0:
        return f"購入することで、{abs(differential_cost):,.0f}円のコスト削減が可能です。"
    elif differential_cost > 0:
        return f"自製することで、{differential_cost:,.0f}円のコスト削減が可能です。"
    else:
        return "自製と購入のコストは同じです。"


def get_accept_or_reject_recommendation(differential_profit: float, special_order_price: float, variable_cost: float) -> str:
    """
    特別注文の受諾可否の推奨事項を取得
    
    Args:
        differential_profit: 差額利益
        special_order_price: 特別注文価格
        variable_cost: 単位変動費
    
    Returns:
        推奨事項の文字列
    """
    if differential_profit > 0:
        return f"特別注文を受諾することで、{differential_profit:,.0f}円の追加利益が得られます。"
    elif differential_profit < 0:
        return f"特別注文を受諾すると、{abs(differential_profit):,.0f}円の損失が発生します。拒否を推奨します。"
    else:
        if special_order_price >= variable_cost:
            return "特別注文の利益はゼロですが、変動費は回収できます。"
        else:
            return "特別注文価格が変動費を下回っています。拒否を推奨します。"


def get_continue_or_discontinue_recommendation(differential_profit: float, contribution_margin: float, avoidable_fixed_cost: float) -> str:
    """
    事業継続・撤退の推奨事項を取得
    
    Args:
        differential_profit: 差額利益
        contribution_margin: 貢献利益
        avoidable_fixed_cost: 回避可能固定費
    
    Returns:
        推奨事項の文字列
    """
    if differential_profit > 0:
        return f"事業を継続することで、{differential_profit:,.0f}円の利益改善が見込まれます。"
    elif differential_profit < 0:
        return f"事業を撤退することで、{abs(differential_profit):,.0f}円の損失削減が可能です。"
    else:
        if contribution_margin > avoidable_fixed_cost:
            return "貢献利益が回避可能固定費を上回っています。継続を検討してください。"
        else:
            return "貢献利益が回避可能固定費を下回っています。撤退を検討してください。"
