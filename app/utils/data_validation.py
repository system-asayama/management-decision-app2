"""
データ検証ヘルパー関数
運転資金前提と返済スケジュール前提のデータを検証
"""


class ValidationError(Exception):
    """検証エラー"""
    pass


def validate_working_capital_assumption(data):
    """
    運転資金前提データを検証
    
    Args:
        data: 運転資金前提データ
    
    Returns:
        dict: 検証結果 {'valid': bool, 'errors': [], 'warnings': []}
    
    Raises:
        ValidationError: 致命的なエラーがある場合
    """
    errors = []
    warnings = []
    
    # 回転期間の検証
    turnover_periods = {
        'cash_turnover_period': '現預金回転期間',
        'receivables_turnover_period': '売掛債権回転期間',
        'inventory_turnover_period': '棚卸資産回転期間',
        'payables_turnover_period': '買掛債務回転期間'
    }
    
    for key, name in turnover_periods.items():
        value = data.get(key, 0)
        
        # 負の値チェック
        if value < 0:
            errors.append(f'{name}が負の値です: {value}')
        
        # 異常に大きい値チェック（12ヶ月以上）
        if value > 12:
            warnings.append(f'{name}が12ヶ月を超えています: {value}')
        
        # ゼロチェック（警告のみ）
        if value == 0:
            warnings.append(f'{name}がゼロです')
    
    # 運転資金増減額の検証
    increases = {
        'cash_increase': '手許現預金増加額',
        'receivables_increase': '売掛債権増加額',
        'inventory_increase': '棚卸資産増加額',
        'payables_increase': '買掛債務増加額'
    }
    
    for key, name in increases.items():
        value = data.get(key, 0)
        
        # 異常に大きい値チェック（10億円以上）
        if abs(value) > 1000000000:
            warnings.append(f'{name}が異常に大きい値です: {value:,}')
    
    # 債務債権回転期間差異のチェック
    receivables_period = data.get('receivables_turnover_period', 0)
    payables_period = data.get('payables_turnover_period', 0)
    
    if receivables_period > 0 and payables_period > 0:
        diff = payables_period - receivables_period
        if diff < 0:
            warnings.append(
                f'債務債権回転期間差異が負です（買掛債務回転期間 {payables_period} - '
                f'売掛債権回転期間 {receivables_period} = {diff}）。'
                f'資金繰りが厳しい可能性があります。'
            )
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }


def validate_debt_repayment_assumption(data):
    """
    返済スケジュール前提データを検証
    
    Args:
        data: 返済スケジュール前提データ
    
    Returns:
        dict: 検証結果 {'valid': bool, 'errors': [], 'warnings': []}
    
    Raises:
        ValidationError: 致命的なエラーがある場合
    """
    errors = []
    warnings = []
    
    beginning_balance = data.get('beginning_balance', 0)
    borrowing_amount = data.get('borrowing_amount', 0)
    principal_repayment = data.get('principal_repayment', 0)
    ending_balance = data.get('ending_balance', 0)
    interest_payment = data.get('interest_payment', 0)
    average_interest_rate = data.get('average_interest_rate', 0)
    
    # 負の値チェック
    if beginning_balance < 0:
        errors.append(f'借入金期首残高が負の値です: {beginning_balance:,}')
    
    if borrowing_amount < 0:
        errors.append(f'借入金借入額が負の値です: {borrowing_amount:,}')
    
    if principal_repayment < 0:
        errors.append(f'借入金元本返済額が負の値です: {principal_repayment:,}')
    
    if ending_balance < 0:
        errors.append(f'借入金期末残高が負の値です: {ending_balance:,}')
    
    if interest_payment < 0:
        errors.append(f'支払利息が負の値です: {interest_payment:,}')
    
    if average_interest_rate < 0:
        errors.append(f'平均金利が負の値です: {average_interest_rate}')
    
    # 借入金の整合性チェック
    calculated_ending_balance = beginning_balance + borrowing_amount - principal_repayment
    
    # 許容誤差を1円とする
    if abs(calculated_ending_balance - ending_balance) > 1:
        errors.append(
            f'借入金の整合性エラー: 期首残高 {beginning_balance:,} + '
            f'借入額 {borrowing_amount:,} - 返済額 {principal_repayment:,} = '
            f'{calculated_ending_balance:,} ≠ 期末残高 {ending_balance:,}'
        )
    
    # 平均金利の妥当性チェック
    if average_interest_rate > 0.2:  # 20%以上
        warnings.append(f'平均金利が異常に高いです: {average_interest_rate*100:.2f}%')
    
    if average_interest_rate > 0 and interest_payment == 0:
        warnings.append('平均金利が設定されていますが、支払利息がゼロです')
    
    if average_interest_rate == 0 and interest_payment > 0:
        warnings.append('支払利息が発生していますが、平均金利がゼロです')
    
    # 平均金利と支払利息の整合性チェック
    if average_interest_rate > 0 and (beginning_balance + ending_balance) > 0:
        average_balance = (beginning_balance + ending_balance) / 2
        calculated_interest = average_balance * average_interest_rate
        
        # 許容誤差を10%とする
        if abs(calculated_interest - interest_payment) > calculated_interest * 0.1:
            warnings.append(
                f'支払利息の計算が合いません: 平均残高 {average_balance:,.0f} × '
                f'平均金利 {average_interest_rate*100:.2f}% = {calculated_interest:,.0f} ≠ '
                f'支払利息 {interest_payment:,}'
            )
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }


def validate_all_assumptions(working_capital_data, debt_repayment_data):
    """
    すべての前提データを一括検証
    
    Args:
        working_capital_data: 運転資金前提データのリスト
        debt_repayment_data: 返済スケジュール前提データのリスト
    
    Returns:
        dict: 検証結果
    """
    all_errors = []
    all_warnings = []
    
    # 運転資金前提を検証
    for i, wc_data in enumerate(working_capital_data):
        result = validate_working_capital_assumption(wc_data)
        
        if not result['valid']:
            for error in result['errors']:
                all_errors.append(f'運転資金前提（年度{i+1}）: {error}')
        
        for warning in result['warnings']:
            all_warnings.append(f'運転資金前提（年度{i+1}）: {warning}')
    
    # 返済スケジュール前提を検証
    for i, debt_data in enumerate(debt_repayment_data):
        result = validate_debt_repayment_assumption(debt_data)
        
        if not result['valid']:
            for error in result['errors']:
                all_errors.append(f'返済スケジュール前提（年度{i+1}）: {error}')
        
        for warning in result['warnings']:
            all_warnings.append(f'返済スケジュール前提（年度{i+1}）: {warning}')
    
    return {
        'valid': len(all_errors) == 0,
        'errors': all_errors,
        'warnings': all_warnings
    }
