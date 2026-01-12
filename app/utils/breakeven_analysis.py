"""
損益分岐点分析計算ロジック

損益分岐点分析に必要な指標を計算します：
- 損益分岐点売上高
- 損益分岐点比率
- 安全余裕率
- 限界利益率
- 変動費率
"""

def calculate_breakeven_point(sales, variable_costs, fixed_costs):
    """
    損益分岐点売上高を計算
    
    Args:
        sales: 売上高
        variable_costs: 変動費
        fixed_costs: 固定費
    
    Returns:
        dict: 損益分岐点分析結果
    """
    if sales == 0:
        return {
            'breakeven_sales': 0,
            'breakeven_ratio': 0,
            'safety_margin_ratio': 0,
            'contribution_margin_ratio': 0,
            'variable_cost_ratio': 0,
            'contribution_margin': 0,
            'operating_income': 0
        }
    
    # 限界利益 = 売上高 - 変動費
    contribution_margin = sales - variable_costs
    
    # 限界利益率 = 限界利益 / 売上高 × 100
    contribution_margin_ratio = (contribution_margin / sales) * 100 if sales > 0 else 0
    
    # 変動費率 = 変動費 / 売上高 × 100
    variable_cost_ratio = (variable_costs / sales) * 100 if sales > 0 else 0
    
    # 損益分岐点売上高 = 固定費 / 限界利益率
    breakeven_sales = (fixed_costs / contribution_margin_ratio) * 100 if contribution_margin_ratio > 0 else 0
    
    # 損益分岐点比率 = 損益分岐点売上高 / 売上高 × 100
    breakeven_ratio = (breakeven_sales / sales) * 100 if sales > 0 else 0
    
    # 安全余裕率 = (売上高 - 損益分岐点売上高) / 売上高 × 100
    safety_margin_ratio = ((sales - breakeven_sales) / sales) * 100 if sales > 0 else 0
    
    # 営業利益 = 限界利益 - 固定費
    operating_income = contribution_margin - fixed_costs
    
    return {
        'breakeven_sales': breakeven_sales,
        'breakeven_ratio': breakeven_ratio,
        'safety_margin_ratio': safety_margin_ratio,
        'contribution_margin_ratio': contribution_margin_ratio,
        'variable_cost_ratio': variable_cost_ratio,
        'contribution_margin': contribution_margin,
        'operating_income': operating_income,
        'sales': sales,
        'variable_costs': variable_costs,
        'fixed_costs': fixed_costs
    }


def calculate_target_sales(fixed_costs, target_profit, contribution_margin_ratio):
    """
    目標利益を達成するための必要売上高を計算
    
    Args:
        fixed_costs: 固定費
        target_profit: 目標利益
        contribution_margin_ratio: 限界利益率（%）
    
    Returns:
        float: 必要売上高
    """
    if contribution_margin_ratio == 0:
        return 0
    
    # 必要売上高 = (固定費 + 目標利益) / 限界利益率
    target_sales = ((fixed_costs + target_profit) / contribution_margin_ratio) * 100
    
    return target_sales


def estimate_cost_structure(sales, cost_of_sales, operating_expenses, operating_income):
    """
    費用構造を推定（変動費と固定費に分類）
    
    簡易的な推定方法：
    - 変動費 = 売上原価 + 販管費の一部（販管費の30%と仮定）
    - 固定費 = 販管費の残り（販管費の70%と仮定）
    
    Args:
        sales: 売上高
        cost_of_sales: 売上原価
        operating_expenses: 販売費及び一般管理費
        operating_income: 営業利益
    
    Returns:
        dict: 推定された費用構造
    """
    # 変動費 = 売上原価 + 販管費の30%
    variable_costs = cost_of_sales + (operating_expenses * 0.3)
    
    # 固定費 = 販管費の70%
    fixed_costs = operating_expenses * 0.7
    
    return {
        'variable_costs': variable_costs,
        'fixed_costs': fixed_costs,
        'total_costs': variable_costs + fixed_costs
    }


def analyze_cost_volume_profit(sales, variable_costs, fixed_costs, target_profit=0):
    """
    CVP分析（Cost-Volume-Profit Analysis）を実行
    
    Args:
        sales: 売上高
        variable_costs: 変動費
        fixed_costs: 固定費
        target_profit: 目標利益（デフォルト: 0）
    
    Returns:
        dict: CVP分析結果
    """
    # 損益分岐点分析
    breakeven_result = calculate_breakeven_point(sales, variable_costs, fixed_costs)
    
    # 目標利益達成に必要な売上高
    target_sales = 0
    if target_profit > 0:
        target_sales = calculate_target_sales(
            fixed_costs,
            target_profit,
            breakeven_result['contribution_margin_ratio']
        )
    
    return {
        **breakeven_result,
        'target_profit': target_profit,
        'target_sales': target_sales
    }
