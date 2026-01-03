"""
財務指標計算ロジック
"""

def calculate_profitability_ratios(profit_loss):
    """
    収益性指標を計算
    
    Args:
        profit_loss: ProfitLossStatementオブジェクト
    
    Returns:
        dict: 収益性指標
    """
    if not profit_loss or profit_loss.sales == 0:
        return {
            'operating_profit_margin': 0,
            'ordinary_profit_margin': 0,
            'net_profit_margin': 0
        }
    
    return {
        'operating_profit_margin': round(profit_loss.operating_income / profit_loss.sales * 100, 2),
        'ordinary_profit_margin': round(profit_loss.ordinary_income / profit_loss.sales * 100, 2),
        'net_profit_margin': round(profit_loss.net_income / profit_loss.sales * 100, 2)
    }


def calculate_safety_ratios(balance_sheet):
    """
    安全性指標を計算
    
    Args:
        balance_sheet: BalanceSheetオブジェクト
    
    Returns:
        dict: 安全性指標
    """
    if not balance_sheet:
        return {
            'current_ratio': 0,
            'fixed_ratio': 0,
            'equity_ratio': 0,
            'debt_ratio': 0
        }
    
    current_ratio = 0
    if balance_sheet.current_liabilities > 0:
        current_ratio = round(balance_sheet.current_assets / balance_sheet.current_liabilities * 100, 2)
    
    fixed_ratio = 0
    if balance_sheet.total_equity > 0:
        fixed_ratio = round(balance_sheet.fixed_assets / balance_sheet.total_equity * 100, 2)
    
    equity_ratio = 0
    if balance_sheet.total_assets > 0:
        equity_ratio = round(balance_sheet.total_equity / balance_sheet.total_assets * 100, 2)
    
    debt_ratio = 0
    if balance_sheet.total_equity > 0:
        debt_ratio = round(balance_sheet.total_liabilities / balance_sheet.total_equity * 100, 2)
    
    return {
        'current_ratio': current_ratio,
        'fixed_ratio': fixed_ratio,
        'equity_ratio': equity_ratio,
        'debt_ratio': debt_ratio
    }


def calculate_efficiency_ratios(profit_loss, balance_sheet):
    """
    効率性指標を計算
    
    Args:
        profit_loss: ProfitLossStatementオブジェクト
        balance_sheet: BalanceSheetオブジェクト
    
    Returns:
        dict: 効率性指標
    """
    if not profit_loss or not balance_sheet or profit_loss.sales == 0:
        return {
            'total_asset_turnover': 0,
            'fixed_asset_turnover': 0,
            'current_asset_turnover': 0
        }
    
    total_asset_turnover = 0
    if balance_sheet.total_assets > 0:
        total_asset_turnover = round(profit_loss.sales / balance_sheet.total_assets, 2)
    
    fixed_asset_turnover = 0
    if balance_sheet.fixed_assets > 0:
        fixed_asset_turnover = round(profit_loss.sales / balance_sheet.fixed_assets, 2)
    
    current_asset_turnover = 0
    if balance_sheet.current_assets > 0:
        current_asset_turnover = round(profit_loss.sales / balance_sheet.current_assets, 2)
    
    return {
        'total_asset_turnover': total_asset_turnover,
        'fixed_asset_turnover': fixed_asset_turnover,
        'current_asset_turnover': current_asset_turnover
    }


def calculate_roa_roe(profit_loss, balance_sheet):
    """
    ROAとROEを計算
    
    Args:
        profit_loss: ProfitLossStatementオブジェクト
        balance_sheet: BalanceSheetオブジェクト
    
    Returns:
        dict: ROAとROE
    """
    if not profit_loss or not balance_sheet:
        return {
            'roa': 0,
            'roe': 0
        }
    
    roa = 0
    if balance_sheet.total_assets > 0:
        roa = round(profit_loss.net_income / balance_sheet.total_assets * 100, 2)
    
    roe = 0
    if balance_sheet.total_equity > 0:
        roe = round(profit_loss.net_income / balance_sheet.total_equity * 100, 2)
    
    return {
        'roa': roa,
        'roe': roe
    }


def calculate_all_ratios(profit_loss, balance_sheet):
    """
    全ての財務指標を計算
    
    Args:
        profit_loss: ProfitLossStatementオブジェクト
        balance_sheet: BalanceSheetオブジェクト
    
    Returns:
        dict: 全ての財務指標
    """
    profitability = calculate_profitability_ratios(profit_loss)
    safety = calculate_safety_ratios(balance_sheet)
    efficiency = calculate_efficiency_ratios(profit_loss, balance_sheet)
    roa_roe = calculate_roa_roe(profit_loss, balance_sheet)
    
    return {
        'profitability': profitability,
        'safety': safety,
        'efficiency': efficiency,
        'roa_roe': roa_roe
    }


def get_ratio_status(ratio_name, value):
    """
    財務指標の状態を判定（良好、注意、警告）
    
    Args:
        ratio_name: 指標名
        value: 指標値
    
    Returns:
        str: 'success', 'warning', 'danger'
    """
    # 収益性指標
    if ratio_name in ['operating_profit_margin', 'ordinary_profit_margin', 'net_profit_margin']:
        if value >= 5:
            return 'success'
        elif value >= 2:
            return 'warning'
        else:
            return 'danger'
    
    # 流動比率
    elif ratio_name == 'current_ratio':
        if value >= 200:
            return 'success'
        elif value >= 100:
            return 'warning'
        else:
            return 'danger'
    
    # 自己資本比率
    elif ratio_name == 'equity_ratio':
        if value >= 40:
            return 'success'
        elif value >= 20:
            return 'warning'
        else:
            return 'danger'
    
    # 固定比率
    elif ratio_name == 'fixed_ratio':
        if value <= 100:
            return 'success'
        elif value <= 150:
            return 'warning'
        else:
            return 'danger'
    
    # 負債比率
    elif ratio_name == 'debt_ratio':
        if value <= 100:
            return 'success'
        elif value <= 200:
            return 'warning'
        else:
            return 'danger'
    
    # ROA, ROE
    elif ratio_name in ['roa', 'roe']:
        if value >= 10:
            return 'success'
        elif value >= 5:
            return 'warning'
        else:
            return 'danger'
    
    # 回転率
    elif ratio_name in ['total_asset_turnover', 'fixed_asset_turnover', 'current_asset_turnover']:
        if value >= 1.5:
            return 'success'
        elif value >= 1.0:
            return 'warning'
        else:
            return 'danger'
    
    return 'secondary'
