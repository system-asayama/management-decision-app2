"""
借入金許容限度額分析計算ロジック

企業の借入金許容限度額を分析し、適正な借入金額を算出します。
"""

def calculate_debt_capacity(total_assets, total_liabilities, total_equity, operating_income, interest_expense, annual_cash_flow):
    """
    借入金許容限度額を計算
    
    Args:
        total_assets: 総資産
        total_liabilities: 総負債
        total_equity: 純資産
        operating_income: 営業利益
        interest_expense: 支払利息
        annual_cash_flow: 年間キャッシュフロー（営業CF）
    
    Returns:
        dict: 借入金許容限度額分析結果
    """
    # 現在の自己資本比率
    equity_ratio = (total_equity / total_assets) * 100 if total_assets > 0 else 0
    
    # 現在の負債比率
    debt_ratio = (total_liabilities / total_equity) * 100 if total_equity > 0 else 0
    
    # 目標自己資本比率（30%を目標とする）
    target_equity_ratio = 30.0
    
    # 目標自己資本比率を維持するための許容負債額
    # 総資産 = 純資産 / 自己資本比率
    # 許容総資産 = 純資産 / 目標自己資本比率
    allowable_total_assets = (total_equity / target_equity_ratio) * 100 if target_equity_ratio > 0 else 0
    
    # 許容負債額 = 許容総資産 - 純資産
    allowable_total_liabilities = allowable_total_assets - total_equity
    
    # 追加借入可能額 = 許容負債額 - 現在の負債額
    additional_debt_capacity = allowable_total_liabilities - total_liabilities
    
    # 債務償還年数（現在の負債をキャッシュフローで返済するのに必要な年数）
    debt_service_years = total_liabilities / annual_cash_flow if annual_cash_flow > 0 else float('inf')
    
    # インタレストカバレッジレシオ（利息支払能力）
    # ICR = 営業利益 / 支払利息
    interest_coverage_ratio = operating_income / interest_expense if interest_expense > 0 else float('inf')
    
    # 安全な借入限度額（キャッシュフローの5年分を上限とする）
    safe_debt_limit = annual_cash_flow * 5
    
    # 最終的な借入許容限度額（追加借入可能額と安全な借入限度額の小さい方）
    final_debt_capacity = min(additional_debt_capacity, safe_debt_limit) if additional_debt_capacity > 0 else 0
    
    return {
        'current_equity_ratio': equity_ratio,
        'current_debt_ratio': debt_ratio,
        'target_equity_ratio': target_equity_ratio,
        'allowable_total_assets': allowable_total_assets,
        'allowable_total_liabilities': allowable_total_liabilities,
        'additional_debt_capacity': additional_debt_capacity,
        'debt_service_years': debt_service_years,
        'interest_coverage_ratio': interest_coverage_ratio,
        'safe_debt_limit': safe_debt_limit,
        'final_debt_capacity': final_debt_capacity,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'total_equity': total_equity,
        'operating_income': operating_income,
        'interest_expense': interest_expense,
        'annual_cash_flow': annual_cash_flow
    }


def calculate_debt_repayment_plan(debt_amount, annual_interest_rate, repayment_years):
    """
    借入金返済計画を計算
    
    Args:
        debt_amount: 借入金額
        annual_interest_rate: 年利率（%）
        repayment_years: 返済年数
    
    Returns:
        list: 年次返済計画
    """
    if debt_amount <= 0 or repayment_years <= 0:
        return []
    
    # 年利率を小数に変換
    rate = annual_interest_rate / 100
    
    # 元利均等返済の年間返済額を計算
    # 年間返済額 = 借入金額 × (利率 × (1 + 利率)^返済年数) / ((1 + 利率)^返済年数 - 1)
    if rate > 0:
        annual_payment = debt_amount * (rate * (1 + rate) ** repayment_years) / ((1 + rate) ** repayment_years - 1)
    else:
        annual_payment = debt_amount / repayment_years
    
    repayment_plan = []
    remaining_balance = debt_amount
    
    for year in range(1, repayment_years + 1):
        # 利息 = 残高 × 利率
        interest_payment = remaining_balance * rate
        
        # 元金 = 年間返済額 - 利息
        principal_payment = annual_payment - interest_payment
        
        # 残高を更新
        remaining_balance -= principal_payment
        
        # 最終年の調整（端数処理）
        if year == repayment_years:
            principal_payment += remaining_balance
            remaining_balance = 0
        
        repayment_plan.append({
            'year': year,
            'annual_payment': annual_payment,
            'principal_payment': principal_payment,
            'interest_payment': interest_payment,
            'remaining_balance': max(0, remaining_balance)
        })
    
    return repayment_plan


def evaluate_debt_health(equity_ratio, debt_ratio, debt_service_years, interest_coverage_ratio):
    """
    借入金健全性を評価
    
    Args:
        equity_ratio: 自己資本比率
        debt_ratio: 負債比率
        debt_service_years: 債務償還年数
        interest_coverage_ratio: インタレストカバレッジレシオ
    
    Returns:
        dict: 健全性評価結果
    """
    # 自己資本比率の評価
    if equity_ratio >= 50:
        equity_evaluation = "優良"
        equity_color = "success"
    elif equity_ratio >= 30:
        equity_evaluation = "良好"
        equity_color = "info"
    elif equity_ratio >= 20:
        equity_evaluation = "普通"
        equity_color = "warning"
    else:
        equity_evaluation = "要注意"
        equity_color = "danger"
    
    # 債務償還年数の評価
    if debt_service_years <= 3:
        debt_service_evaluation = "優良"
        debt_service_color = "success"
    elif debt_service_years <= 5:
        debt_service_evaluation = "良好"
        debt_service_color = "info"
    elif debt_service_years <= 10:
        debt_service_evaluation = "普通"
        debt_service_color = "warning"
    else:
        debt_service_evaluation = "要注意"
        debt_service_color = "danger"
    
    # インタレストカバレッジレシオの評価
    if interest_coverage_ratio >= 10:
        icr_evaluation = "優良"
        icr_color = "success"
    elif interest_coverage_ratio >= 5:
        icr_evaluation = "良好"
        icr_color = "info"
    elif interest_coverage_ratio >= 2:
        icr_evaluation = "普通"
        icr_color = "warning"
    else:
        icr_evaluation = "要注意"
        icr_color = "danger"
    
    # 総合評価（3つの指標の平均）
    score = 0
    if equity_evaluation == "優良": score += 4
    elif equity_evaluation == "良好": score += 3
    elif equity_evaluation == "普通": score += 2
    else: score += 1
    
    if debt_service_evaluation == "優良": score += 4
    elif debt_service_evaluation == "良好": score += 3
    elif debt_service_evaluation == "普通": score += 2
    else: score += 1
    
    if icr_evaluation == "優良": score += 4
    elif icr_evaluation == "良好": score += 3
    elif icr_evaluation == "普通": score += 2
    else: score += 1
    
    average_score = score / 3
    
    if average_score >= 3.5:
        overall_evaluation = "優良"
        overall_color = "success"
    elif average_score >= 2.5:
        overall_evaluation = "良好"
        overall_color = "info"
    elif average_score >= 1.5:
        overall_evaluation = "普通"
        overall_color = "warning"
    else:
        overall_evaluation = "要注意"
        overall_color = "danger"
    
    return {
        'equity_evaluation': equity_evaluation,
        'equity_color': equity_color,
        'debt_service_evaluation': debt_service_evaluation,
        'debt_service_color': debt_service_color,
        'icr_evaluation': icr_evaluation,
        'icr_color': icr_color,
        'overall_evaluation': overall_evaluation,
        'overall_color': overall_color
    }


def calculate_debt_capacity_method2(gross_profit, operating_income, interest_expense, average_interest_rate, target_interest_burden_ratio=0.10):
    """
    資金力-2: 安全金利法による借入金許容限度額を計算
    
    Excel の「資金力-2」シートの計算式を実装。
    年間支払利息を売上総利益の一定割合以下に抑えるという手法。
    
    Args:
        gross_profit: 売上総利益
        operating_income: 営業利益
        interest_expense: 現在の支払利息
        average_interest_rate: 平均金利（%）
        target_interest_burden_ratio: 目標利息負担率（デフォルト: 0.10 = 10%）
    
    Returns:
        dict: 資金力-2分析結果
    """
    # 現在の利息負担率 = 支払利息 / 売上総利益
    current_interest_burden_ratio = interest_expense / gross_profit if gross_profit > 0 else 0
    
    # 安全な利息支払額 = 売上総利益 × 目標利息負担率
    safe_interest_payment = gross_profit * target_interest_burden_ratio
    
    # 許容負債額 = 安全な利息支払額 / 平均金利
    average_interest_rate_decimal = average_interest_rate / 100
    allowable_debt = safe_interest_payment / average_interest_rate_decimal if average_interest_rate_decimal > 0 else 0
    
    # 現在の推定負債額 = 現在の支払利息 / 平均金利
    current_estimated_debt = interest_expense / average_interest_rate_decimal if average_interest_rate_decimal > 0 else 0
    
    # 追加借入可能額 = 許容負債額 - 現在の推定負債額
    additional_borrowing_capacity = allowable_debt - current_estimated_debt
    
    # インタレストカバレッジレシオ = 営業利益 / 支払利息
    interest_coverage_ratio = operating_income / interest_expense if interest_expense > 0 else float('inf')
    
    # 評価
    if current_interest_burden_ratio <= target_interest_burden_ratio:
        evaluation = "安全"
        evaluation_color = "success"
    elif current_interest_burden_ratio <= target_interest_burden_ratio * 1.5:
        evaluation = "注意"
        evaluation_color = "warning"
    else:
        evaluation = "危険"
        evaluation_color = "danger"
    
    return {
        'method': 'Method2: 安全金利法',
        'gross_profit': gross_profit,
        'operating_income': operating_income,
        'current_interest_expense': interest_expense,
        'current_interest_burden_ratio': current_interest_burden_ratio,
        'current_interest_burden_ratio_percent': current_interest_burden_ratio * 100,
        'target_interest_burden_ratio': target_interest_burden_ratio,
        'target_interest_burden_ratio_percent': target_interest_burden_ratio * 100,
        'safe_interest_payment': safe_interest_payment,
        'average_interest_rate': average_interest_rate,
        'allowable_debt': allowable_debt,
        'current_estimated_debt': current_estimated_debt,
        'additional_borrowing_capacity': additional_borrowing_capacity,
        'interest_coverage_ratio': interest_coverage_ratio,
        'evaluation': evaluation,
        'evaluation_color': evaluation_color
    }
