"""
資金繰り計画計算ロジック
月次の資金収支を予測し、資金不足を事前に把握
"""

def calculate_monthly_cash_flow(
    beginning_balance: float,
    sales_revenue: float,
    other_revenue: float,
    purchase_payment: float,
    personnel_cost: float,
    rent: float,
    utilities: float,
    other_expenses: float,
    loan_repayment: float,
    tax_payment: float
) -> dict:
    """
    月次の資金収支を計算
    
    Args:
        beginning_balance: 期首残高
        sales_revenue: 売上収入
        other_revenue: その他収入
        purchase_payment: 仕入支払
        personnel_cost: 人件費
        rent: 賃借料
        utilities: 水道光熱費
        other_expenses: その他経費
        loan_repayment: 借入金返済
        tax_payment: 税金支払
    
    Returns:
        dict: 資金収支計算結果
    """
    # 収入合計
    total_revenue = sales_revenue + other_revenue
    
    # 支出合計
    total_expenses = (
        purchase_payment + personnel_cost + rent + utilities + 
        other_expenses + loan_repayment + tax_payment
    )
    
    # 資金収支（収入-支出）
    net_cash_flow = total_revenue - total_expenses
    
    # 期末残高
    ending_balance = beginning_balance + net_cash_flow
    
    return {
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_cash_flow': net_cash_flow,
        'ending_balance': ending_balance
    }


def generate_annual_cash_flow_plan(
    beginning_balance: float,
    monthly_sales_revenue: list,
    monthly_purchase_payment: list,
    monthly_personnel_cost: float,
    monthly_rent: float,
    monthly_utilities: float,
    monthly_other_expenses: float,
    loan_repayment: float = 0,
    tax_payment_month: int = None,
    tax_payment_amount: float = 0
) -> list:
    """
    年間の資金繰り計画を生成
    
    Args:
        beginning_balance: 期首残高
        monthly_sales_revenue: 月次売上収入リスト（12ヶ月分）
        monthly_purchase_payment: 月次仕入支払リスト（12ヶ月分）
        monthly_personnel_cost: 月次人件費
        monthly_rent: 月次賃借料
        monthly_utilities: 月次水道光熱費
        monthly_other_expenses: 月次その他経費
        loan_repayment: 月次借入金返済額
        tax_payment_month: 税金支払月（1-12）
        tax_payment_amount: 税金支払額
    
    Returns:
        list: 12ヶ月分の資金繰り計画
    """
    cash_flow_plan = []
    current_balance = beginning_balance
    
    for month in range(1, 13):
        # 売上収入（リストから取得）
        sales_revenue = monthly_sales_revenue[month - 1] if month - 1 < len(monthly_sales_revenue) else 0
        
        # 仕入支払（リストから取得）
        purchase_payment = monthly_purchase_payment[month - 1] if month - 1 < len(monthly_purchase_payment) else 0
        
        # 税金支払（指定月のみ）
        tax_payment = tax_payment_amount if month == tax_payment_month else 0
        
        # 月次資金収支を計算
        result = calculate_monthly_cash_flow(
            beginning_balance=current_balance,
            sales_revenue=sales_revenue,
            other_revenue=0,
            purchase_payment=purchase_payment,
            personnel_cost=monthly_personnel_cost,
            rent=monthly_rent,
            utilities=monthly_utilities,
            other_expenses=monthly_other_expenses,
            loan_repayment=loan_repayment,
            tax_payment=tax_payment
        )
        
        # 資金繰り計画に追加
        cash_flow_plan.append({
            'month': month,
            'beginning_balance': current_balance,
            'sales_revenue': sales_revenue,
            'other_revenue': 0,
            'total_revenue': result['total_revenue'],
            'purchase_payment': purchase_payment,
            'personnel_cost': monthly_personnel_cost,
            'rent': monthly_rent,
            'utilities': monthly_utilities,
            'other_expenses': monthly_other_expenses,
            'loan_repayment': loan_repayment,
            'tax_payment': tax_payment,
            'total_expenses': result['total_expenses'],
            'net_cash_flow': result['net_cash_flow'],
            'ending_balance': result['ending_balance']
        })
        
        # 次月の期首残高を更新
        current_balance = result['ending_balance']
    
    return cash_flow_plan


def detect_cash_shortage(cash_flow_plan: list, minimum_balance: float = 0) -> list:
    """
    資金不足を検出
    
    Args:
        cash_flow_plan: 資金繰り計画リスト
        minimum_balance: 最低必要残高
    
    Returns:
        list: 資金不足が発生する月のリスト
    """
    shortage_months = []
    
    for plan in cash_flow_plan:
        if plan['ending_balance'] < minimum_balance:
            shortage_months.append({
                'month': plan['month'],
                'ending_balance': plan['ending_balance'],
                'shortage_amount': minimum_balance - plan['ending_balance']
            })
    
    return shortage_months


def calculate_required_financing(cash_flow_plan: list, minimum_balance: float = 0) -> dict:
    """
    必要な資金調達額を計算
    
    Args:
        cash_flow_plan: 資金繰り計画リスト
        minimum_balance: 最低必要残高
    
    Returns:
        dict: 資金調達額の計算結果
    """
    shortage_months = detect_cash_shortage(cash_flow_plan, minimum_balance)
    
    if not shortage_months:
        return {
            'required_financing': 0,
            'shortage_months': [],
            'max_shortage': 0,
            'max_shortage_month': None
        }
    
    # 最大不足額を計算
    max_shortage = max(shortage_months, key=lambda x: x['shortage_amount'])
    
    return {
        'required_financing': max_shortage['shortage_amount'],
        'shortage_months': shortage_months,
        'max_shortage': max_shortage['shortage_amount'],
        'max_shortage_month': max_shortage['month']
    }


def simulate_financing_impact(
    cash_flow_plan: list,
    financing_amount: float,
    financing_month: int,
    interest_rate: float = 0.02
) -> list:
    """
    資金調達の影響をシミュレーション
    
    Args:
        cash_flow_plan: 資金繰り計画リスト
        financing_amount: 資金調達額
        financing_month: 資金調達月（1-12）
        interest_rate: 年利率（デフォルト: 2%）
    
    Returns:
        list: 資金調達後の資金繰り計画
    """
    updated_plan = []
    
    for plan in cash_flow_plan:
        updated_plan_item = plan.copy()
        
        # 資金調達月に収入を追加
        if plan['month'] == financing_month:
            updated_plan_item['other_revenue'] += financing_amount
            updated_plan_item['total_revenue'] += financing_amount
            updated_plan_item['net_cash_flow'] += financing_amount
            updated_plan_item['ending_balance'] += financing_amount
        
        # 資金調達月以降の月に利息を追加
        elif plan['month'] > financing_month:
            monthly_interest = financing_amount * (interest_rate / 12)
            updated_plan_item['other_expenses'] += monthly_interest
            updated_plan_item['total_expenses'] += monthly_interest
            updated_plan_item['net_cash_flow'] -= monthly_interest
            updated_plan_item['ending_balance'] -= monthly_interest
        
        updated_plan.append(updated_plan_item)
    
    return updated_plan
