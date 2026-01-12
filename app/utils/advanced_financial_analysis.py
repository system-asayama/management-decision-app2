"""
高度な財務分析指標計算モジュール
"""

def calculate_growth_indicators(current_data, previous_data):
    """
    成長力指標を計算
    
    Args:
        current_data: 当期データ（dict）
        previous_data: 前期データ（dict）
    
    Returns:
        dict: 成長力指標
    """
    indicators = {}
    
    # 売上高成長率
    if previous_data.get('sales', 0) > 0:
        indicators['sales_growth_rate'] = ((current_data.get('sales', 0) - previous_data.get('sales', 0)) / previous_data.get('sales', 0)) * 100
    else:
        indicators['sales_growth_rate'] = 0
    
    # 総資産成長率
    if previous_data.get('total_assets', 0) > 0:
        indicators['total_assets_growth_rate'] = ((current_data.get('total_assets', 0) - previous_data.get('total_assets', 0)) / previous_data.get('total_assets', 0)) * 100
    else:
        indicators['total_assets_growth_rate'] = 0
    
    # 純資産成長率
    if previous_data.get('net_assets', 0) > 0:
        indicators['net_assets_growth_rate'] = ((current_data.get('net_assets', 0) - previous_data.get('net_assets', 0)) / previous_data.get('net_assets', 0)) * 100
    else:
        indicators['net_assets_growth_rate'] = 0
    
    # 従業員数成長率
    if previous_data.get('employees', 0) > 0:
        indicators['employees_growth_rate'] = ((current_data.get('employees', 0) - previous_data.get('employees', 0)) / previous_data.get('employees', 0)) * 100
    else:
        indicators['employees_growth_rate'] = 0
    
    return indicators


def calculate_profitability_indicators(pl_data, bs_data):
    """
    収益力指標を計算
    
    Args:
        pl_data: 損益計算書データ（dict）
        bs_data: 貸借対照表データ（dict）
    
    Returns:
        dict: 収益力指標
    """
    indicators = {}
    
    sales = pl_data.get('sales', 0)
    gross_profit = pl_data.get('gross_profit', 0)
    operating_income = pl_data.get('operating_income', 0)
    ordinary_income = pl_data.get('ordinary_income', 0)
    net_income = pl_data.get('net_income', 0)
    total_assets = bs_data.get('total_assets', 0)
    net_assets = bs_data.get('net_assets', 0)
    employees = pl_data.get('employees', 1)  # ゼロ除算を避けるため
    labor_cost = pl_data.get('labor_cost', 0)
    
    # 売上高総利益率
    if sales > 0:
        indicators['gross_profit_margin'] = (gross_profit / sales) * 100
    else:
        indicators['gross_profit_margin'] = 0
    
    # 売上高営業利益率
    if sales > 0:
        indicators['operating_profit_margin'] = (operating_income / sales) * 100
    else:
        indicators['operating_profit_margin'] = 0
    
    # 売上高経常利益率
    if sales > 0:
        indicators['ordinary_profit_margin'] = (ordinary_income / sales) * 100
    else:
        indicators['ordinary_profit_margin'] = 0
    
    # 売上高当期純利益率
    if sales > 0:
        indicators['net_profit_margin'] = (net_income / sales) * 100
    else:
        indicators['net_profit_margin'] = 0
    
    # ROA（総資産利益率）
    if total_assets > 0:
        indicators['roa'] = (net_income / total_assets) * 100
    else:
        indicators['roa'] = 0
    
    # ROE（自己資本利益率）
    if net_assets > 0:
        indicators['roe'] = (net_income / net_assets) * 100
    else:
        indicators['roe'] = 0
    
    # 労働生産性（従業員一人当たり売上高）
    if employees > 0:
        indicators['labor_productivity'] = sales / employees
    else:
        indicators['labor_productivity'] = 0
    
    # 労働分配率
    if sales > 0:
        indicators['labor_share_ratio'] = (labor_cost / sales) * 100
    else:
        indicators['labor_share_ratio'] = 0
    
    return indicators


def calculate_financial_strength_indicators(bs_data, pl_data):
    """
    資金力指標を計算
    
    Args:
        bs_data: 貸借対照表データ（dict）
        pl_data: 損益計算書データ（dict）
    
    Returns:
        dict: 資金力指標
    """
    indicators = {}
    
    current_assets = bs_data.get('current_assets', 0)
    current_liabilities = bs_data.get('current_liabilities', 0)
    quick_assets = bs_data.get('quick_assets', 0)  # 当座資産（現預金+売上債権）
    fixed_assets = bs_data.get('fixed_assets', 0)
    total_assets = bs_data.get('total_assets', 0)
    net_assets = bs_data.get('net_assets', 0)
    total_liabilities = bs_data.get('total_liabilities', 0)
    long_term_liabilities = bs_data.get('long_term_liabilities', 0)
    interest_expense = pl_data.get('interest_expense', 0)
    ordinary_income = pl_data.get('ordinary_income', 0)
    
    # 流動比率
    if current_liabilities > 0:
        indicators['current_ratio'] = (current_assets / current_liabilities) * 100
    else:
        indicators['current_ratio'] = 0
    
    # 当座比率
    if current_liabilities > 0:
        indicators['quick_ratio'] = (quick_assets / current_liabilities) * 100
    else:
        indicators['quick_ratio'] = 0
    
    # 固定比率
    if net_assets > 0:
        indicators['fixed_ratio'] = (fixed_assets / net_assets) * 100
    else:
        indicators['fixed_ratio'] = 0
    
    # 固定長期適合率
    if net_assets + long_term_liabilities > 0:
        indicators['fixed_long_term_suitability_ratio'] = (fixed_assets / (net_assets + long_term_liabilities)) * 100
    else:
        indicators['fixed_long_term_suitability_ratio'] = 0
    
    # 自己資本比率
    if total_assets > 0:
        indicators['equity_ratio'] = (net_assets / total_assets) * 100
    else:
        indicators['equity_ratio'] = 0
    
    # 負債比率
    if net_assets > 0:
        indicators['debt_ratio'] = (total_liabilities / net_assets) * 100
    else:
        indicators['debt_ratio'] = 0
    
    # インタレスト・カバレッジ・レシオ
    if interest_expense > 0:
        indicators['interest_coverage_ratio'] = (ordinary_income + interest_expense) / interest_expense
    else:
        indicators['interest_coverage_ratio'] = 0
    
    return indicators


def calculate_productivity_indicators(pl_data, bs_data):
    """
    生産力指標を計算
    
    Args:
        pl_data: 損益計算書データ（dict）
        bs_data: 貸借対照表データ（dict）
    
    Returns:
        dict: 生産力指標
    """
    indicators = {}
    
    sales = pl_data.get('sales', 0)
    total_assets = bs_data.get('total_assets', 0)
    fixed_assets = bs_data.get('fixed_assets', 0)
    current_assets = bs_data.get('current_assets', 0)
    accounts_receivable = bs_data.get('accounts_receivable', 0)
    inventory = bs_data.get('inventory', 0)
    accounts_payable = bs_data.get('accounts_payable', 0)
    
    # 総資産回転率
    if total_assets > 0:
        indicators['total_assets_turnover'] = sales / total_assets
    else:
        indicators['total_assets_turnover'] = 0
    
    # 固定資産回転率
    if fixed_assets > 0:
        indicators['fixed_assets_turnover'] = sales / fixed_assets
    else:
        indicators['fixed_assets_turnover'] = 0
    
    # 流動資産回転率
    if current_assets > 0:
        indicators['current_assets_turnover'] = sales / current_assets
    else:
        indicators['current_assets_turnover'] = 0
    
    # 売上債権回転率
    if accounts_receivable > 0:
        indicators['accounts_receivable_turnover'] = sales / accounts_receivable
    else:
        indicators['accounts_receivable_turnover'] = 0
    
    # 売上債権回転期間（日数）
    if indicators['accounts_receivable_turnover'] > 0:
        indicators['accounts_receivable_turnover_days'] = 365 / indicators['accounts_receivable_turnover']
    else:
        indicators['accounts_receivable_turnover_days'] = 0
    
    # 棚卸資産回転率
    if inventory > 0:
        indicators['inventory_turnover'] = sales / inventory
    else:
        indicators['inventory_turnover'] = 0
    
    # 棚卸資産回転期間（日数）
    if indicators['inventory_turnover'] > 0:
        indicators['inventory_turnover_days'] = 365 / indicators['inventory_turnover']
    else:
        indicators['inventory_turnover_days'] = 0
    
    # 仕入債務回転率
    if accounts_payable > 0:
        indicators['accounts_payable_turnover'] = sales / accounts_payable
    else:
        indicators['accounts_payable_turnover'] = 0
    
    # 仕入債務回転期間（日数）
    if indicators['accounts_payable_turnover'] > 0:
        indicators['accounts_payable_turnover_days'] = 365 / indicators['accounts_payable_turnover']
    else:
        indicators['accounts_payable_turnover_days'] = 0
    
    return indicators


def calculate_all_indicators(current_pl, current_bs, previous_pl=None, previous_bs=None):
    """
    すべての財務分析指標を計算
    
    Args:
        current_pl: 当期損益計算書データ（dict）
        current_bs: 当期貸借対照表データ（dict）
        previous_pl: 前期損益計算書データ（dict、オプション）
        previous_bs: 前期貸借対照表データ（dict、オプション）
    
    Returns:
        dict: すべての財務分析指標
    """
    all_indicators = {}
    
    # 成長力指標（前期データがある場合のみ）
    if previous_pl and previous_bs:
        current_data = {
            'sales': current_pl.get('sales', 0),
            'total_assets': current_bs.get('total_assets', 0),
            'net_assets': current_bs.get('net_assets', 0),
            'employees': current_pl.get('employees', 0)
        }
        previous_data = {
            'sales': previous_pl.get('sales', 0),
            'total_assets': previous_bs.get('total_assets', 0),
            'net_assets': previous_bs.get('net_assets', 0),
            'employees': previous_pl.get('employees', 0)
        }
        all_indicators['growth'] = calculate_growth_indicators(current_data, previous_data)
    else:
        all_indicators['growth'] = {}
    
    # 収益力指標
    all_indicators['profitability'] = calculate_profitability_indicators(current_pl, current_bs)
    
    # 資金力指標
    all_indicators['financial_strength'] = calculate_financial_strength_indicators(current_bs, current_pl)
    
    # 生産力指標
    all_indicators['productivity'] = calculate_productivity_indicators(current_pl, current_bs)
    
    return all_indicators
