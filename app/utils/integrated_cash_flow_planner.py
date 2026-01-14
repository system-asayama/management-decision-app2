"""
統合資金繰り計画モジュール

営業収支・投資収支・財務収支を統合した月次資金繰り表を生成します。
借入返済計画、設備投資計画、運転資金計画からキャッシュフローを統合します。
"""

from typing import Dict, List, Any


def generate_integrated_monthly_cash_flow(
    fiscal_year_id: int,
    beginning_cash_balance: float,
    monthly_operating_cash_flow: List[Dict[str, float]],
    monthly_investment_cash_flow: List[Dict[str, float]],
    monthly_financing_cash_flow: List[Dict[str, float]],
    minimum_cash_balance: float = 0
) -> Dict[str, Any]:
    """
    統合月次資金繰り表を生成
    
    Args:
        fiscal_year_id: 会計年度ID
        beginning_cash_balance: 期首現金残高
        monthly_operating_cash_flow: 月次営業収支リスト（12ヶ月分）
        monthly_investment_cash_flow: 月次投資収支リスト（12ヶ月分）
        monthly_financing_cash_flow: 月次財務収支リスト（12ヶ月分）
        minimum_cash_balance: 最低必要現金残高
    
    Returns:
        dict: 統合資金繰り表と警告情報
    """
    cash_flow_table = []
    current_balance = beginning_cash_balance
    shortage_warnings = []
    
    for month in range(1, 13):
        month_index = month - 1
        
        # 営業収支（収入 - 支出）
        operating_cf = monthly_operating_cash_flow[month_index] if month_index < len(monthly_operating_cash_flow) else {}
        operating_inflow = operating_cf.get('inflow', 0)
        operating_outflow = operating_cf.get('outflow', 0)
        net_operating_cf = operating_inflow - operating_outflow
        
        # 投資収支（収入 - 支出）
        investment_cf = monthly_investment_cash_flow[month_index] if month_index < len(monthly_investment_cash_flow) else {}
        investment_inflow = investment_cf.get('inflow', 0)
        investment_outflow = investment_cf.get('outflow', 0)
        net_investment_cf = investment_inflow - investment_outflow
        
        # 財務収支（収入 - 支出）
        financing_cf = monthly_financing_cash_flow[month_index] if month_index < len(monthly_financing_cash_flow) else {}
        financing_inflow = financing_cf.get('inflow', 0)
        financing_outflow = financing_cf.get('outflow', 0)
        net_financing_cf = financing_inflow - financing_outflow
        
        # 月次純キャッシュフロー
        net_cash_flow = net_operating_cf + net_investment_cf + net_financing_cf
        
        # 期末残高
        ending_balance = current_balance + net_cash_flow
        
        # 残高不足チェック
        is_shortage = ending_balance < minimum_cash_balance
        shortage_amount = minimum_cash_balance - ending_balance if is_shortage else 0
        
        if is_shortage:
            shortage_warnings.append({
                'month': month,
                'ending_balance': ending_balance,
                'minimum_required': minimum_cash_balance,
                'shortage_amount': shortage_amount,
                'severity': 'critical' if ending_balance < 0 else 'warning'
            })
        
        # 月次データを追加
        cash_flow_table.append({
            'month': month,
            'beginning_balance': current_balance,
            'operating_inflow': operating_inflow,
            'operating_outflow': operating_outflow,
            'net_operating_cf': net_operating_cf,
            'investment_inflow': investment_inflow,
            'investment_outflow': investment_outflow,
            'net_investment_cf': net_investment_cf,
            'financing_inflow': financing_inflow,
            'financing_outflow': financing_outflow,
            'net_financing_cf': net_financing_cf,
            'net_cash_flow': net_cash_flow,
            'ending_balance': ending_balance,
            'is_shortage': is_shortage,
            'shortage_amount': shortage_amount
        })
        
        # 次月の期首残高を更新
        current_balance = ending_balance
    
    return {
        'fiscal_year_id': fiscal_year_id,
        'beginning_cash_balance': beginning_cash_balance,
        'minimum_cash_balance': minimum_cash_balance,
        'cash_flow_table': cash_flow_table,
        'shortage_warnings': shortage_warnings,
        'has_shortage': len(shortage_warnings) > 0,
        'ending_cash_balance': current_balance
    }


def calculate_operating_cash_flow_from_pl(
    monthly_sales: List[float],
    monthly_cost_of_sales: List[float],
    monthly_operating_expenses: List[float],
    accounts_receivable_collection_period: int = 30,
    accounts_payable_payment_period: int = 30
) -> List[Dict[str, float]]:
    """
    PLから営業キャッシュフローを計算
    
    Args:
        monthly_sales: 月次売上高リスト
        monthly_cost_of_sales: 月次売上原価リスト
        monthly_operating_expenses: 月次営業費用リスト
        accounts_receivable_collection_period: 売掛金回収期間（日）
        accounts_payable_payment_period: 買掛金支払期間（日）
    
    Returns:
        list: 月次営業キャッシュフローリスト
    """
    monthly_cf = []
    
    # 回収期間・支払期間を月数に変換（簡易的に30日=1ヶ月とする）
    collection_lag_months = accounts_receivable_collection_period // 30
    payment_lag_months = accounts_payable_payment_period // 30
    
    for month in range(12):
        # 売上収入（回収期間を考慮）
        collection_month = month - collection_lag_months
        if collection_month >= 0 and collection_month < len(monthly_sales):
            cash_inflow = monthly_sales[collection_month]
        else:
            cash_inflow = 0
        
        # 仕入支出（支払期間を考慮）
        payment_month = month - payment_lag_months
        if payment_month >= 0 and payment_month < len(monthly_cost_of_sales):
            cash_outflow_cogs = monthly_cost_of_sales[payment_month]
        else:
            cash_outflow_cogs = 0
        
        # 営業費用支出（当月）
        cash_outflow_opex = monthly_operating_expenses[month] if month < len(monthly_operating_expenses) else 0
        
        monthly_cf.append({
            'inflow': cash_inflow,
            'outflow': cash_outflow_cogs + cash_outflow_opex
        })
    
    return monthly_cf


def calculate_investment_cash_flow_from_capex(
    monthly_capital_expenditure: List[float],
    monthly_asset_sales: List[float] = None
) -> List[Dict[str, float]]:
    """
    設備投資計画から投資キャッシュフローを計算
    
    Args:
        monthly_capital_expenditure: 月次設備投資額リスト
        monthly_asset_sales: 月次資産売却収入リスト
    
    Returns:
        list: 月次投資キャッシュフローリスト
    """
    if monthly_asset_sales is None:
        monthly_asset_sales = [0] * 12
    
    monthly_cf = []
    
    for month in range(12):
        capex = monthly_capital_expenditure[month] if month < len(monthly_capital_expenditure) else 0
        asset_sales = monthly_asset_sales[month] if month < len(monthly_asset_sales) else 0
        
        monthly_cf.append({
            'inflow': asset_sales,
            'outflow': capex
        })
    
    return monthly_cf


def calculate_financing_cash_flow_from_debt(
    monthly_borrowing: List[float],
    monthly_debt_repayment: List[float],
    monthly_interest_payment: List[float]
) -> List[Dict[str, float]]:
    """
    借入返済計画から財務キャッシュフローを計算
    
    Args:
        monthly_borrowing: 月次借入額リスト
        monthly_debt_repayment: 月次元金返済額リスト
        monthly_interest_payment: 月次利息支払額リスト
    
    Returns:
        list: 月次財務キャッシュフローリスト
    """
    monthly_cf = []
    
    for month in range(12):
        borrowing = monthly_borrowing[month] if month < len(monthly_borrowing) else 0
        repayment = monthly_debt_repayment[month] if month < len(monthly_debt_repayment) else 0
        interest = monthly_interest_payment[month] if month < len(monthly_interest_payment) else 0
        
        monthly_cf.append({
            'inflow': borrowing,
            'outflow': repayment + interest
        })
    
    return monthly_cf


def generate_shortage_alert_message(shortage_warnings: List[Dict[str, Any]]) -> str:
    """
    資金不足警告メッセージを生成
    
    Args:
        shortage_warnings: 資金不足警告リスト
    
    Returns:
        str: 警告メッセージ
    """
    if not shortage_warnings:
        return "資金不足は検出されませんでした。"
    
    critical_months = [w for w in shortage_warnings if w['severity'] == 'critical']
    warning_months = [w for w in shortage_warnings if w['severity'] == 'warning']
    
    messages = []
    
    if critical_months:
        critical_month_list = ', '.join([f"{w['month']}月" for w in critical_months])
        messages.append(f"【重大】{critical_month_list}に現金残高がマイナスになります。")
    
    if warning_months:
        warning_month_list = ', '.join([f"{w['month']}月" for w in warning_months])
        messages.append(f"【警告】{warning_month_list}に現金残高が最低必要残高を下回ります。")
    
    # 最大不足額を計算
    max_shortage = max(shortage_warnings, key=lambda x: x['shortage_amount'])
    messages.append(f"最大不足額: {max_shortage['shortage_amount']:,.0f}円（{max_shortage['month']}月）")
    
    return '\n'.join(messages)


def suggest_financing_solution(
    shortage_warnings: List[Dict[str, Any]],
    available_credit_line: float = 0
) -> Dict[str, Any]:
    """
    資金不足に対する資金調達提案を生成
    
    Args:
        shortage_warnings: 資金不足警告リスト
        available_credit_line: 利用可能な与信枠
    
    Returns:
        dict: 資金調達提案
    """
    if not shortage_warnings:
        return {
            'required': False,
            'suggested_amount': 0,
            'suggestion': '資金調達は不要です。'
        }
    
    # 最大不足額を計算
    max_shortage = max(shortage_warnings, key=lambda x: x['shortage_amount'])
    required_amount = max_shortage['shortage_amount']
    
    # 安全マージンを加える（10%）
    suggested_amount = required_amount * 1.1
    
    if suggested_amount <= available_credit_line:
        suggestion = f"与信枠内で{suggested_amount:,.0f}円の短期借入を推奨します。"
    else:
        suggestion = f"{suggested_amount:,.0f}円の資金調達が必要です。与信枠（{available_credit_line:,.0f}円）を超えるため、追加の資金調達手段を検討してください。"
    
    return {
        'required': True,
        'required_amount': required_amount,
        'suggested_amount': suggested_amount,
        'available_credit_line': available_credit_line,
        'suggestion': suggestion,
        'shortage_months': [w['month'] for w in shortage_warnings]
    }
