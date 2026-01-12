"""
資金調達返済計画モジュール

借入金の調達と返済計画を管理します。
"""

from typing import Dict, List, Any
import math


def calculate_loan_payment(
    principal: float,
    annual_interest_rate: float,
    term_years: int,
    payment_frequency: str = 'monthly'
) -> Dict[str, Any]:
    """
    ローンの返済額を計算
    
    Args:
        principal: 元金
        annual_interest_rate: 年利率（%）
        term_years: 返済期間（年）
        payment_frequency: 返済頻度（'monthly', 'quarterly', 'annually'）
    
    Returns:
        返済計算結果の辞書
    """
    # 返済回数を計算
    if payment_frequency == 'monthly':
        periods = term_years * 12
        rate_per_period = annual_interest_rate / 100 / 12
    elif payment_frequency == 'quarterly':
        periods = term_years * 4
        rate_per_period = annual_interest_rate / 100 / 4
    else:  # annually
        periods = term_years
        rate_per_period = annual_interest_rate / 100
    
    # 元利均等返済額を計算
    if rate_per_period == 0:
        payment_per_period = principal / periods
    else:
        payment_per_period = principal * rate_per_period * (1 + rate_per_period) ** periods / \
                           ((1 + rate_per_period) ** periods - 1)
    
    # 総返済額
    total_payment = payment_per_period * periods
    
    # 総利息額
    total_interest = total_payment - principal
    
    return {
        'principal': principal,
        'annual_interest_rate': annual_interest_rate,
        'term_years': term_years,
        'payment_frequency': payment_frequency,
        'periods': periods,
        'payment_per_period': payment_per_period,
        'total_payment': total_payment,
        'total_interest': total_interest
    }


def generate_amortization_schedule(
    principal: float,
    annual_interest_rate: float,
    term_years: int,
    payment_frequency: str = 'monthly'
) -> List[Dict[str, Any]]:
    """
    償却スケジュールを生成
    
    Args:
        principal: 元金
        annual_interest_rate: 年利率（%）
        term_years: 返済期間（年）
        payment_frequency: 返済頻度
    
    Returns:
        償却スケジュールのリスト
    """
    # 返済額を計算
    loan_info = calculate_loan_payment(principal, annual_interest_rate, term_years, payment_frequency)
    
    payment_per_period = loan_info['payment_per_period']
    periods = loan_info['periods']
    
    # 期間あたりの利率
    if payment_frequency == 'monthly':
        rate_per_period = annual_interest_rate / 100 / 12
    elif payment_frequency == 'quarterly':
        rate_per_period = annual_interest_rate / 100 / 4
    else:
        rate_per_period = annual_interest_rate / 100
    
    schedule = []
    remaining_balance = principal
    
    for period in range(1, periods + 1):
        # 利息額
        interest_payment = remaining_balance * rate_per_period
        
        # 元金返済額
        principal_payment = payment_per_period - interest_payment
        
        # 残高
        remaining_balance -= principal_payment
        
        # 最終期の調整（端数処理）
        if period == periods:
            principal_payment += remaining_balance
            remaining_balance = 0
        
        schedule.append({
            'period': period,
            'payment': payment_per_period,
            'principal_payment': principal_payment,
            'interest_payment': interest_payment,
            'remaining_balance': max(0, remaining_balance)
        })
    
    return schedule


def calculate_multiple_loans(
    loans: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    複数の借入金を統合計算
    
    Args:
        loans: 借入金のリスト
    
    Returns:
        統合計算結果の辞書
    """
    total_principal = 0
    total_payment = 0
    total_interest = 0
    loan_details = []
    
    for loan in loans:
        loan_calc = calculate_loan_payment(
            principal=loan.get('principal', 0),
            annual_interest_rate=loan.get('annual_interest_rate', 0),
            term_years=loan.get('term_years', 1),
            payment_frequency=loan.get('payment_frequency', 'monthly')
        )
        
        total_principal += loan_calc['principal']
        total_payment += loan_calc['total_payment']
        total_interest += loan_calc['total_interest']
        
        loan_calc['name'] = loan.get('name', f"借入金{len(loan_details) + 1}")
        loan_details.append(loan_calc)
    
    return {
        'total_principal': total_principal,
        'total_payment': total_payment,
        'total_interest': total_interest,
        'loan_details': loan_details
    }


def calculate_debt_service_coverage_ratio(
    operating_income: float,
    annual_debt_payment: float,
    depreciation: float = 0
) -> float:
    """
    債務返済能力比率（DSCR）を計算
    
    Args:
        operating_income: 営業利益
        annual_debt_payment: 年間借入金返済額
        depreciation: 減価償却費
    
    Returns:
        DSCR
    """
    # キャッシュフロー = 営業利益 + 減価償却費
    cash_flow = operating_income + depreciation
    
    if annual_debt_payment == 0:
        return 0.0
    
    return cash_flow / annual_debt_payment


def plan_financing_repayment(
    required_funds: float,
    equity_ratio: float,
    loan_interest_rate: float,
    loan_term_years: int,
    payment_frequency: str = 'monthly'
) -> Dict[str, Any]:
    """
    資金調達返済計画を作成
    
    Args:
        required_funds: 必要資金額
        equity_ratio: 自己資本比率（%）
        loan_interest_rate: 借入金利率（%）
        loan_term_years: 返済期間（年）
        payment_frequency: 返済頻度
    
    Returns:
        資金調達返済計画の辞書
    """
    # 自己資金と借入金を計算
    equity = required_funds * (equity_ratio / 100)
    loan = required_funds - equity
    
    # 借入金返済計画を計算
    if loan > 0:
        loan_calc = calculate_loan_payment(
            principal=loan,
            annual_interest_rate=loan_interest_rate,
            term_years=loan_term_years,
            payment_frequency=payment_frequency
        )
    else:
        loan_calc = {
            'principal': 0,
            'payment_per_period': 0,
            'total_payment': 0,
            'total_interest': 0,
            'periods': 0
        }
    
    return {
        'required_funds': required_funds,
        'equity': equity,
        'equity_ratio': equity_ratio,
        'loan': loan,
        'loan_ratio': 100 - equity_ratio,
        'loan_interest_rate': loan_interest_rate,
        'loan_term_years': loan_term_years,
        'payment_frequency': payment_frequency,
        'payment_per_period': loan_calc['payment_per_period'],
        'total_payment': loan_calc['total_payment'],
        'total_interest': loan_calc['total_interest'],
        'periods': loan_calc.get('periods', 0)
    }


def calculate_refinancing_benefit(
    current_loan_balance: float,
    current_interest_rate: float,
    remaining_term_years: int,
    new_interest_rate: float,
    refinancing_cost: float = 0
) -> Dict[str, Any]:
    """
    借り換えの効果を計算
    
    Args:
        current_loan_balance: 現在の借入残高
        current_interest_rate: 現在の金利（%）
        remaining_term_years: 残存期間（年）
        new_interest_rate: 新金利（%）
        refinancing_cost: 借り換え費用
    
    Returns:
        借り換え効果の辞書
    """
    # 現在の返済計画
    current_plan = calculate_loan_payment(
        principal=current_loan_balance,
        annual_interest_rate=current_interest_rate,
        term_years=remaining_term_years
    )
    
    # 借り換え後の返済計画
    new_plan = calculate_loan_payment(
        principal=current_loan_balance,
        annual_interest_rate=new_interest_rate,
        term_years=remaining_term_years
    )
    
    # 利息削減額
    interest_savings = current_plan['total_interest'] - new_plan['total_interest']
    
    # 実質的な削減額（借り換え費用を差し引く）
    net_savings = interest_savings - refinancing_cost
    
    # 月次返済額の削減
    monthly_payment_savings = current_plan['payment_per_period'] - new_plan['payment_per_period']
    
    return {
        'current_total_interest': current_plan['total_interest'],
        'new_total_interest': new_plan['total_interest'],
        'interest_savings': interest_savings,
        'refinancing_cost': refinancing_cost,
        'net_savings': net_savings,
        'current_monthly_payment': current_plan['payment_per_period'],
        'new_monthly_payment': new_plan['payment_per_period'],
        'monthly_payment_savings': monthly_payment_savings,
        'recommendation': 'refinance' if net_savings > 0 else 'keep',
        'recommendation_text': get_refinancing_recommendation(net_savings, monthly_payment_savings)
    }


def get_refinancing_recommendation(net_savings: float, monthly_savings: float) -> str:
    """
    借り換えの推奨事項を取得
    
    Args:
        net_savings: 実質削減額
        monthly_savings: 月次削減額
    
    Returns:
        推奨事項の文字列
    """
    if net_savings > 0:
        return f"借り換えにより、総額{net_savings:,.0f}円の利息削減が見込まれます。月次返済額も{monthly_savings:,.0f}円削減されるため、借り換えを推奨します。"
    else:
        return f"借り換え費用を考慮すると、実質的な削減効果は{net_savings:,.0f}円とマイナスです。現状維持を推奨します。"


def calculate_early_repayment_benefit(
    current_loan_balance: float,
    annual_interest_rate: float,
    remaining_term_years: int,
    early_repayment_amount: float,
    early_repayment_penalty: float = 0
) -> Dict[str, Any]:
    """
    繰上返済の効果を計算
    
    Args:
        current_loan_balance: 現在の借入残高
        annual_interest_rate: 年利率（%）
        remaining_term_years: 残存期間（年）
        early_repayment_amount: 繰上返済額
        early_repayment_penalty: 繰上返済手数料
    
    Returns:
        繰上返済効果の辞書
    """
    # 現在の返済計画
    current_plan = calculate_loan_payment(
        principal=current_loan_balance,
        annual_interest_rate=annual_interest_rate,
        term_years=remaining_term_years
    )
    
    # 繰上返済後の残高
    new_balance = current_loan_balance - early_repayment_amount
    
    if new_balance <= 0:
        # 完済
        interest_savings = current_plan['total_interest']
        new_total_interest = 0
        new_monthly_payment = 0
    else:
        # 繰上返済後の返済計画
        new_plan = calculate_loan_payment(
            principal=new_balance,
            annual_interest_rate=annual_interest_rate,
            term_years=remaining_term_years
        )
        
        interest_savings = current_plan['total_interest'] - new_plan['total_interest']
        new_total_interest = new_plan['total_interest']
        new_monthly_payment = new_plan['payment_per_period']
    
    # 実質的な削減額
    net_savings = interest_savings - early_repayment_penalty
    
    return {
        'current_balance': current_loan_balance,
        'early_repayment_amount': early_repayment_amount,
        'new_balance': max(0, new_balance),
        'current_total_interest': current_plan['total_interest'],
        'new_total_interest': new_total_interest,
        'interest_savings': interest_savings,
        'early_repayment_penalty': early_repayment_penalty,
        'net_savings': net_savings,
        'current_monthly_payment': current_plan['payment_per_period'],
        'new_monthly_payment': new_monthly_payment,
        'recommendation': 'repay' if net_savings > 0 else 'keep'
    }


def evaluate_debt_capacity(
    annual_operating_income: float,
    annual_depreciation: float,
    existing_annual_debt_payment: float,
    max_dscr: float = 1.5
) -> Dict[str, Any]:
    """
    追加借入可能額を評価
    
    Args:
        annual_operating_income: 年間営業利益
        annual_depreciation: 年間減価償却費
        existing_annual_debt_payment: 既存の年間借入金返済額
        max_dscr: 目標DSCR
    
    Returns:
        借入可能額の評価結果
    """
    # 利用可能なキャッシュフロー
    available_cash_flow = annual_operating_income + annual_depreciation
    
    # 最大返済可能額
    max_debt_payment = available_cash_flow / max_dscr
    
    # 追加借入可能な年間返済額
    additional_payment_capacity = max_debt_payment - existing_annual_debt_payment
    
    return {
        'annual_operating_income': annual_operating_income,
        'annual_depreciation': annual_depreciation,
        'available_cash_flow': available_cash_flow,
        'existing_annual_debt_payment': existing_annual_debt_payment,
        'max_debt_payment': max_debt_payment,
        'additional_payment_capacity': additional_payment_capacity,
        'current_dscr': calculate_debt_service_coverage_ratio(
            annual_operating_income, existing_annual_debt_payment, annual_depreciation
        ) if existing_annual_debt_payment > 0 else 0
    }
