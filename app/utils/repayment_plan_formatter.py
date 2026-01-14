"""
返済計画フォーマッターモジュール

返済計画や借換え効果をUI表示用に整形します。
"""

from typing import Dict, List, Any


def format_amortization_schedule_for_ui(
    schedule: List[Dict[str, Any]],
    payment_frequency: str = 'monthly'
) -> Dict[str, Any]:
    """
    償却スケジュールをUI表示用に整形
    
    Args:
        schedule: 償却スケジュールリスト
        payment_frequency: 返済頻度（'monthly', 'quarterly', 'annually'）
    
    Returns:
        dict: UI表示用の整形済みデータ
    """
    # 期間ラベルを生成
    if payment_frequency == 'monthly':
        period_label = '月'
    elif payment_frequency == 'quarterly':
        period_label = '四半期'
    else:
        period_label = '年'
    
    # テーブルデータを整形
    table_data = []
    for item in schedule:
        table_data.append({
            'period': item['period'],
            'period_label': f"{item['period']}{period_label}",
            'payment': round(item['payment'], 2),
            'payment_formatted': f"{item['payment']:,.0f}円",
            'principal_payment': round(item['principal_payment'], 2),
            'principal_payment_formatted': f"{item['principal_payment']:,.0f}円",
            'interest_payment': round(item['interest_payment'], 2),
            'interest_payment_formatted': f"{item['interest_payment']:,.0f}円",
            'remaining_balance': round(item['remaining_balance'], 2),
            'remaining_balance_formatted': f"{item['remaining_balance']:,.0f}円"
        })
    
    # サマリーを計算
    total_payment = sum(item['payment'] for item in schedule)
    total_principal = sum(item['principal_payment'] for item in schedule)
    total_interest = sum(item['interest_payment'] for item in schedule)
    
    return {
        'payment_frequency': payment_frequency,
        'period_label': period_label,
        'table_data': table_data,
        'summary': {
            'total_periods': len(schedule),
            'total_payment': round(total_payment, 2),
            'total_payment_formatted': f"{total_payment:,.0f}円",
            'total_principal': round(total_principal, 2),
            'total_principal_formatted': f"{total_principal:,.0f}円",
            'total_interest': round(total_interest, 2),
            'total_interest_formatted': f"{total_interest:,.0f}円"
        }
    }


def format_refinancing_comparison_for_ui(
    refinancing_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    借換え効果比較をUI表示用に整形
    
    Args:
        refinancing_result: 借換え効果の計算結果
    
    Returns:
        dict: UI表示用の整形済みデータ
    """
    return {
        'comparison_table': [
            {
                'item': '総利息額',
                'current': f"{refinancing_result['current_total_interest']:,.0f}円",
                'new': f"{refinancing_result['new_total_interest']:,.0f}円",
                'difference': f"{refinancing_result['interest_savings']:,.0f}円"
            },
            {
                'item': '月次返済額',
                'current': f"{refinancing_result['current_monthly_payment']:,.0f}円",
                'new': f"{refinancing_result['new_monthly_payment']:,.0f}円",
                'difference': f"{refinancing_result['monthly_payment_savings']:,.0f}円"
            }
        ],
        'cost_benefit': {
            'interest_savings': round(refinancing_result['interest_savings'], 2),
            'interest_savings_formatted': f"{refinancing_result['interest_savings']:,.0f}円",
            'refinancing_cost': round(refinancing_result['refinancing_cost'], 2),
            'refinancing_cost_formatted': f"{refinancing_result['refinancing_cost']:,.0f}円",
            'net_savings': round(refinancing_result['net_savings'], 2),
            'net_savings_formatted': f"{refinancing_result['net_savings']:,.0f}円"
        },
        'recommendation': {
            'action': refinancing_result['recommendation'],
            'action_label': '借換えを推奨' if refinancing_result['recommendation'] == 'refinance' else '現状維持を推奨',
            'text': refinancing_result['recommendation_text']
        }
    }


def format_early_repayment_for_ui(
    early_repayment_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    繰上返済効果をUI表示用に整形
    
    Args:
        early_repayment_result: 繰上返済効果の計算結果
    
    Returns:
        dict: UI表示用の整形済みデータ
    """
    return {
        'balance_comparison': [
            {
                'item': '現在の残高',
                'amount': f"{early_repayment_result['current_balance']:,.0f}円"
            },
            {
                'item': '繰上返済額',
                'amount': f"{early_repayment_result['early_repayment_amount']:,.0f}円"
            },
            {
                'item': '返済後の残高',
                'amount': f"{early_repayment_result['new_balance']:,.0f}円"
            }
        ],
        'interest_comparison': [
            {
                'item': '総利息額',
                'current': f"{early_repayment_result['current_total_interest']:,.0f}円",
                'new': f"{early_repayment_result['new_total_interest']:,.0f}円",
                'savings': f"{early_repayment_result['interest_savings']:,.0f}円"
            },
            {
                'item': '月次返済額',
                'current': f"{early_repayment_result['current_monthly_payment']:,.0f}円",
                'new': f"{early_repayment_result['new_monthly_payment']:,.0f}円",
                'savings': f"{early_repayment_result['current_monthly_payment'] - early_repayment_result['new_monthly_payment']:,.0f}円"
            }
        ],
        'cost_benefit': {
            'interest_savings': round(early_repayment_result['interest_savings'], 2),
            'interest_savings_formatted': f"{early_repayment_result['interest_savings']:,.0f}円",
            'early_repayment_penalty': round(early_repayment_result['early_repayment_penalty'], 2),
            'early_repayment_penalty_formatted': f"{early_repayment_result['early_repayment_penalty']:,.0f}円",
            'net_savings': round(early_repayment_result['net_savings'], 2),
            'net_savings_formatted': f"{early_repayment_result['net_savings']:,.0f}円"
        },
        'recommendation': {
            'action': early_repayment_result['recommendation'],
            'action_label': '繰上返済を推奨' if early_repayment_result['recommendation'] == 'repay' else '現状維持を推奨'
        }
    }


def format_multiple_loans_for_ui(
    multiple_loans_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    複数ローンの統合計算結果をUI表示用に整形
    
    Args:
        multiple_loans_result: 複数ローンの統合計算結果
    
    Returns:
        dict: UI表示用の整形済みデータ
    """
    # 各ローンの詳細を整形
    loan_details_formatted = []
    for loan in multiple_loans_result['loan_details']:
        loan_details_formatted.append({
            'name': loan['name'],
            'principal': round(loan['principal'], 2),
            'principal_formatted': f"{loan['principal']:,.0f}円",
            'annual_interest_rate': loan['annual_interest_rate'],
            'annual_interest_rate_formatted': f"{loan['annual_interest_rate']:.2f}%",
            'term_years': loan['term_years'],
            'payment_per_period': round(loan['payment_per_period'], 2),
            'payment_per_period_formatted': f"{loan['payment_per_period']:,.0f}円",
            'total_payment': round(loan['total_payment'], 2),
            'total_payment_formatted': f"{loan['total_payment']:,.0f}円",
            'total_interest': round(loan['total_interest'], 2),
            'total_interest_formatted': f"{loan['total_interest']:,.0f}円"
        })
    
    return {
        'loan_details': loan_details_formatted,
        'summary': {
            'total_principal': round(multiple_loans_result['total_principal'], 2),
            'total_principal_formatted': f"{multiple_loans_result['total_principal']:,.0f}円",
            'total_payment': round(multiple_loans_result['total_payment'], 2),
            'total_payment_formatted': f"{multiple_loans_result['total_payment']:,.0f}円",
            'total_interest': round(multiple_loans_result['total_interest'], 2),
            'total_interest_formatted': f"{multiple_loans_result['total_interest']:,.0f}円"
        }
    }


def format_cash_flow_table_for_ui(
    cash_flow_table: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    資金繰り表をUI表示用に整形
    
    Args:
        cash_flow_table: 資金繰り表データ
    
    Returns:
        dict: UI表示用の整形済みデータ
    """
    table_data = []
    
    for row in cash_flow_table:
        table_data.append({
            'month': row['month'],
            'month_label': f"{row['month']}月",
            'beginning_balance': round(row['beginning_balance'], 2),
            'beginning_balance_formatted': f"{row['beginning_balance']:,.0f}円",
            'operating_inflow': round(row['operating_inflow'], 2),
            'operating_inflow_formatted': f"{row['operating_inflow']:,.0f}円",
            'operating_outflow': round(row['operating_outflow'], 2),
            'operating_outflow_formatted': f"{row['operating_outflow']:,.0f}円",
            'net_operating_cf': round(row['net_operating_cf'], 2),
            'net_operating_cf_formatted': f"{row['net_operating_cf']:,.0f}円",
            'investment_inflow': round(row['investment_inflow'], 2),
            'investment_inflow_formatted': f"{row['investment_inflow']:,.0f}円",
            'investment_outflow': round(row['investment_outflow'], 2),
            'investment_outflow_formatted': f"{row['investment_outflow']:,.0f}円",
            'net_investment_cf': round(row['net_investment_cf'], 2),
            'net_investment_cf_formatted': f"{row['net_investment_cf']:,.0f}円",
            'financing_inflow': round(row['financing_inflow'], 2),
            'financing_inflow_formatted': f"{row['financing_inflow']:,.0f}円",
            'financing_outflow': round(row['financing_outflow'], 2),
            'financing_outflow_formatted': f"{row['financing_outflow']:,.0f}円",
            'net_financing_cf': round(row['net_financing_cf'], 2),
            'net_financing_cf_formatted': f"{row['net_financing_cf']:,.0f}円",
            'net_cash_flow': round(row['net_cash_flow'], 2),
            'net_cash_flow_formatted': f"{row['net_cash_flow']:,.0f}円",
            'ending_balance': round(row['ending_balance'], 2),
            'ending_balance_formatted': f"{row['ending_balance']:,.0f}円",
            'is_shortage': row['is_shortage'],
            'shortage_amount': round(row['shortage_amount'], 2) if row['is_shortage'] else 0,
            'shortage_amount_formatted': f"{row['shortage_amount']:,.0f}円" if row['is_shortage'] else '-',
            'status': 'critical' if row['ending_balance'] < 0 else ('warning' if row['is_shortage'] else 'normal')
        })
    
    return {
        'table_data': table_data,
        'column_headers': [
            {'key': 'month_label', 'label': '月'},
            {'key': 'beginning_balance_formatted', 'label': '期首残高'},
            {'key': 'net_operating_cf_formatted', 'label': '営業CF'},
            {'key': 'net_investment_cf_formatted', 'label': '投資CF'},
            {'key': 'net_financing_cf_formatted', 'label': '財務CF'},
            {'key': 'net_cash_flow_formatted', 'label': '純CF'},
            {'key': 'ending_balance_formatted', 'label': '期末残高'},
            {'key': 'status', 'label': 'ステータス'}
        ]
    }
