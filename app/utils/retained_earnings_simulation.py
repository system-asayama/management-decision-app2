"""
内部留保シミュレーション計算ロジック
"""


def simulate_retained_earnings(
    current_net_assets: float,
    annual_net_income: float,
    dividend_payout_ratio: float,
    years: int,
    growth_rate: float = 0.0
) -> dict:
    """
    内部留保のシミュレーションを実行
    
    Args:
        current_net_assets: 現在の純資産
        annual_net_income: 年間当期純利益
        dividend_payout_ratio: 配当性向（0.0〜1.0）
        years: シミュレーション年数
        growth_rate: 利益成長率（0.0〜1.0）
    
    Returns:
        dict: シミュレーション結果
    """
    results = []
    net_assets = current_net_assets
    net_income = annual_net_income
    
    for year in range(1, years + 1):
        # 配当金を計算
        dividend = net_income * dividend_payout_ratio
        
        # 内部留保額を計算
        retained_earnings = net_income - dividend
        
        # 純資産を更新
        net_assets += retained_earnings
        
        # 結果を記録
        results.append({
            'year': year,
            'net_income': round(net_income, 2),
            'dividend': round(dividend, 2),
            'retained_earnings': round(retained_earnings, 2),
            'net_assets': round(net_assets, 2),
            'net_assets_growth_rate': round((retained_earnings / current_net_assets) * 100, 2) if current_net_assets > 0 else 0
        })
        
        # 次年度の利益を計算（成長率を適用）
        net_income *= (1 + growth_rate)
    
    # 累積内部留保額を計算
    total_retained_earnings = sum(r['retained_earnings'] for r in results)
    total_dividend = sum(r['dividend'] for r in results)
    final_net_assets = results[-1]['net_assets'] if results else current_net_assets
    
    return {
        'simulation_results': results,
        'summary': {
            'initial_net_assets': round(current_net_assets, 2),
            'final_net_assets': round(final_net_assets, 2),
            'total_retained_earnings': round(total_retained_earnings, 2),
            'total_dividend': round(total_dividend, 2),
            'net_assets_increase': round(final_net_assets - current_net_assets, 2),
            'net_assets_increase_rate': round(((final_net_assets - current_net_assets) / current_net_assets) * 100, 2) if current_net_assets > 0 else 0
        }
    }


def calculate_target_net_assets(
    target_equity_ratio: float,
    total_assets: float
) -> float:
    """
    目標自己資本比率から必要な純資産を計算
    
    Args:
        target_equity_ratio: 目標自己資本比率（0.0〜1.0）
        total_assets: 総資産
    
    Returns:
        float: 必要な純資産
    """
    return total_assets * target_equity_ratio


def calculate_years_to_target(
    current_net_assets: float,
    target_net_assets: float,
    annual_retained_earnings: float
) -> float:
    """
    目標純資産に到達するまでの年数を計算
    
    Args:
        current_net_assets: 現在の純資産
        target_net_assets: 目標純資産
        annual_retained_earnings: 年間内部留保額
    
    Returns:
        float: 到達年数
    """
    if annual_retained_earnings <= 0:
        return float('inf')
    
    shortage = target_net_assets - current_net_assets
    if shortage <= 0:
        return 0
    
    return shortage / annual_retained_earnings


def optimize_dividend_payout(
    annual_net_income: float,
    target_retained_earnings: float
) -> dict:
    """
    目標内部留保額から最適な配当性向を計算
    
    Args:
        annual_net_income: 年間当期純利益
        target_retained_earnings: 目標内部留保額
    
    Returns:
        dict: 最適な配当性向と配当金額
    """
    if annual_net_income <= 0:
        return {
            'optimal_payout_ratio': 0.0,
            'dividend': 0.0,
            'retained_earnings': 0.0
        }
    
    # 目標内部留保額が利益を超える場合は配当なし
    if target_retained_earnings >= annual_net_income:
        return {
            'optimal_payout_ratio': 0.0,
            'dividend': 0.0,
            'retained_earnings': annual_net_income
        }
    
    # 最適な配当性向を計算
    retained_earnings = target_retained_earnings
    dividend = annual_net_income - retained_earnings
    payout_ratio = dividend / annual_net_income
    
    return {
        'optimal_payout_ratio': round(payout_ratio, 4),
        'dividend': round(dividend, 2),
        'retained_earnings': round(retained_earnings, 2)
    }


def simulate_retained_earnings_scenarios(
    current_net_assets: float,
    annual_net_income: float,
    dividend_payout_ratios: list,
    years: int,
    growth_rate: float = 0.0
) -> dict:
    """
    複数の配当性向シナリオで内部留保シミュレーションを実行
    
    Args:
        current_net_assets: 現在の純資産
        annual_net_income: 年間当期純利益
        dividend_payout_ratios: 配当性向のリスト（例: [0.2, 0.3, 0.4]）
        years: シミュレーション年数
        growth_rate: 利益成長率（0.0〜1.0）
    
    Returns:
        dict: シナリオごとのシミュレーション結果
    """
    scenarios = []
    
    for i, payout_ratio in enumerate(dividend_payout_ratios, 1):
        # 各シナリオでシミュレーションを実行
        result = simulate_retained_earnings(
            current_net_assets=current_net_assets,
            annual_net_income=annual_net_income,
            dividend_payout_ratio=payout_ratio,
            years=years,
            growth_rate=growth_rate
        )
        
        # シナリオ情報を追加
        scenarios.append({
            'scenario_id': i,
            'scenario_name': f'シナリオ{i}',
            'dividend_payout_ratio': payout_ratio,
            'simulation_results': result['simulation_results'],
            'summary': result['summary']
        })
    
    return {
        'scenarios': scenarios,
        'parameters': {
            'current_net_assets': round(current_net_assets, 2),
            'annual_net_income': round(annual_net_income, 2),
            'years': years,
            'growth_rate': growth_rate
        }
    }


def simulate_internal_reserve_usage(
    current_net_assets: float,
    current_total_assets: float,
    current_liabilities: float,
    annual_net_income: float,
    dividend_payout_ratio: float,
    reinvestment_ratio: float,
    years: int,
    growth_rate: float = 0.0
) -> dict:
    """
    内部留保の使途（再投資 vs 負債返済）をシミュレーション
    
    Args:
        current_net_assets: 現在の純資産
        current_total_assets: 現在の総資産
        current_liabilities: 現在の負債
        annual_net_income: 年間当期純利益
        dividend_payout_ratio: 配当性向（0.0〜1.0）
        reinvestment_ratio: 再投資比率（0.0〜1.0）、残りは負債返済
        years: シミュレーション年数
        growth_rate: 利益成長率（0.0〜1.0）
    
    Returns:
        dict: シミュレーション結果（PL/BS推移を含む）
    """
    results = []
    net_assets = current_net_assets
    total_assets = current_total_assets
    liabilities = current_liabilities
    net_income = annual_net_income
    
    for year in range(1, years + 1):
        # 配当金を計算
        dividend = net_income * dividend_payout_ratio
        
        # 内部留保額を計算
        retained_earnings = net_income - dividend
        
        # 内部留保を再投資と負債返済に振り分け
        reinvestment_amount = retained_earnings * reinvestment_ratio
        debt_repayment_amount = retained_earnings * (1 - reinvestment_ratio)
        
        # BS更新
        # 再投資額は固定資産増加として資産に反映
        total_assets += reinvestment_amount
        
        # 負債返済額は負債を減少
        liabilities = max(0, liabilities - debt_repayment_amount)
        
        # 純資産を更新（内部留保額分増加）
        net_assets += retained_earnings
        
        # 自己資本比率を計算
        equity_ratio = (net_assets / total_assets * 100) if total_assets > 0 else 0
        
        # 負債比率を計算
        debt_ratio = (liabilities / total_assets * 100) if total_assets > 0 else 0
        
        # 結果を記録
        results.append({
            'year': year,
            'net_income': round(net_income, 2),
            'dividend': round(dividend, 2),
            'retained_earnings': round(retained_earnings, 2),
            'reinvestment_amount': round(reinvestment_amount, 2),
            'debt_repayment_amount': round(debt_repayment_amount, 2),
            'total_assets': round(total_assets, 2),
            'liabilities': round(liabilities, 2),
            'net_assets': round(net_assets, 2),
            'equity_ratio': round(equity_ratio, 2),
            'debt_ratio': round(debt_ratio, 2)
        })
        
        # 次年度の利益を計算（成長率を適用）
        net_income *= (1 + growth_rate)
    
    # 累積値を計算
    total_retained_earnings = sum(r['retained_earnings'] for r in results)
    total_reinvestment = sum(r['reinvestment_amount'] for r in results)
    total_debt_repayment = sum(r['debt_repayment_amount'] for r in results)
    total_dividend = sum(r['dividend'] for r in results)
    final_net_assets = results[-1]['net_assets'] if results else current_net_assets
    final_liabilities = results[-1]['liabilities'] if results else current_liabilities
    final_total_assets = results[-1]['total_assets'] if results else current_total_assets
    
    return {
        'simulation_results': results,
        'summary': {
            'initial_net_assets': round(current_net_assets, 2),
            'initial_total_assets': round(current_total_assets, 2),
            'initial_liabilities': round(current_liabilities, 2),
            'final_net_assets': round(final_net_assets, 2),
            'final_total_assets': round(final_total_assets, 2),
            'final_liabilities': round(final_liabilities, 2),
            'total_retained_earnings': round(total_retained_earnings, 2),
            'total_reinvestment': round(total_reinvestment, 2),
            'total_debt_repayment': round(total_debt_repayment, 2),
            'total_dividend': round(total_dividend, 2),
            'net_assets_increase': round(final_net_assets - current_net_assets, 2),
            'net_assets_increase_rate': round(((final_net_assets - current_net_assets) / current_net_assets) * 100, 2) if current_net_assets > 0 else 0,
            'liabilities_decrease': round(current_liabilities - final_liabilities, 2),
            'liabilities_decrease_rate': round(((current_liabilities - final_liabilities) / current_liabilities) * 100, 2) if current_liabilities > 0 else 0
        }
    }


def simulate_internal_reserve_scenarios(
    current_net_assets: float,
    current_total_assets: float,
    current_liabilities: float,
    annual_net_income: float,
    dividend_payout_ratio: float,
    reinvestment_ratios: list,
    years: int,
    growth_rate: float = 0.0
) -> dict:
    """
    複数の再投資比率シナリオで内部留保使途をシミュレーション
    
    Args:
        current_net_assets: 現在の純資産
        current_total_assets: 現在の総資産
        current_liabilities: 現在の負債
        annual_net_income: 年間当期純利益
        dividend_payout_ratio: 配当性向（0.0〜1.0）
        reinvestment_ratios: 再投資比率のリスト（例: [0.3, 0.5, 0.7]）
        years: シミュレーション年数
        growth_rate: 利益成長率（0.0〜1.0）
    
    Returns:
        dict: シナリオごとのシミュレーション結果
    """
    scenarios = []
    
    for i, reinvestment_ratio in enumerate(reinvestment_ratios, 1):
        # 各シナリオでシミュレーションを実行
        result = simulate_internal_reserve_usage(
            current_net_assets=current_net_assets,
            current_total_assets=current_total_assets,
            current_liabilities=current_liabilities,
            annual_net_income=annual_net_income,
            dividend_payout_ratio=dividend_payout_ratio,
            reinvestment_ratio=reinvestment_ratio,
            years=years,
            growth_rate=growth_rate
        )
        
        # シナリオ名を生成
        if reinvestment_ratio >= 0.7:
            scenario_name = '再投資重視'
        elif reinvestment_ratio >= 0.5:
            scenario_name = 'バランス型'
        else:
            scenario_name = '返済重視'
        
        # シナリオ情報を追加
        scenarios.append({
            'scenario_id': i,
            'scenario_name': scenario_name,
            'reinvestment_ratio': reinvestment_ratio,
            'debt_repayment_ratio': round(1 - reinvestment_ratio, 2),
            'simulation_results': result['simulation_results'],
            'summary': result['summary']
        })
    
    return {
        'scenarios': scenarios,
        'parameters': {
            'current_net_assets': round(current_net_assets, 2),
            'current_total_assets': round(current_total_assets, 2),
            'current_liabilities': round(current_liabilities, 2),
            'annual_net_income': round(annual_net_income, 2),
            'dividend_payout_ratio': dividend_payout_ratio,
            'years': years,
            'growth_rate': growth_rate
        }
    }
