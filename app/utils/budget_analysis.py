"""
予算vs実績比較計算ロジック

予算と実績を比較し、達成率や差異を分析します。
"""

def calculate_variance(budget, actual):
    """
    予算と実績の差異を計算
    
    Args:
        budget: 予算値
        actual: 実績値
    
    Returns:
        dict: 差異分析結果
    """
    if budget is None or actual is None:
        return {
            'variance': 0,
            'variance_rate': 0,
            'achievement_rate': 0
        }
    
    # 差異 = 実績 - 予算
    variance = actual - budget
    
    # 差異率 = (実績 - 予算) / 予算 × 100
    variance_rate = (variance / budget) * 100 if budget != 0 else 0
    
    # 達成率 = 実績 / 予算 × 100
    achievement_rate = (actual / budget) * 100 if budget != 0 else 0
    
    return {
        'variance': variance,
        'variance_rate': variance_rate,
        'achievement_rate': achievement_rate
    }


def analyze_budget_vs_actual(budget_data, actual_data):
    """
    予算vs実績の包括的な分析
    
    Args:
        budget_data: 予算データ（dict）
        actual_data: 実績データ（dict）
    
    Returns:
        dict: 予算vs実績分析結果
    """
    result = {}
    
    # 損益計算書項目の分析
    pl_items = [
        ('sales', '売上高'),
        ('cost_of_sales', '売上原価'),
        ('gross_profit', '売上総利益'),
        ('operating_expenses', '販売費及び一般管理費'),
        ('operating_income', '営業利益'),
        ('ordinary_income', '経常利益'),
        ('net_income', '当期純利益')
    ]
    
    result['pl'] = {}
    for key, label in pl_items:
        budget_key = f'budget_{key}'
        actual_key = key
        
        budget_value = budget_data.get(budget_key, 0) or 0
        actual_value = actual_data.get(actual_key, 0) or 0
        
        variance_result = calculate_variance(budget_value, actual_value)
        
        result['pl'][key] = {
            'label': label,
            'budget': budget_value,
            'actual': actual_value,
            **variance_result
        }
    
    # 貸借対照表項目の分析
    bs_items = [
        ('total_assets', '総資産'),
        ('current_assets', '流動資産'),
        ('fixed_assets', '固定資産'),
        ('total_liabilities', '総負債'),
        ('current_liabilities', '流動負債'),
        ('fixed_liabilities', '固定負債'),
        ('total_equity', '純資産')
    ]
    
    result['bs'] = {}
    for key, label in bs_items:
        budget_key = f'budget_{key}'
        actual_key = key
        
        budget_value = budget_data.get(budget_key, 0) or 0
        actual_value = actual_data.get(actual_key, 0) or 0
        
        variance_result = calculate_variance(budget_value, actual_value)
        
        result['bs'][key] = {
            'label': label,
            'budget': budget_value,
            'actual': actual_value,
            **variance_result
        }
    
    return result


def calculate_budget_achievement_summary(budget_vs_actual_result):
    """
    予算達成度のサマリーを計算
    
    Args:
        budget_vs_actual_result: analyze_budget_vs_actualの結果
    
    Returns:
        dict: 予算達成度サマリー
    """
    # 重要指標の達成率を抽出
    sales_achievement = budget_vs_actual_result['pl']['sales']['achievement_rate']
    operating_income_achievement = budget_vs_actual_result['pl']['operating_income']['achievement_rate']
    ordinary_income_achievement = budget_vs_actual_result['pl']['ordinary_income']['achievement_rate']
    net_income_achievement = budget_vs_actual_result['pl']['net_income']['achievement_rate']
    
    # 総合評価を計算（4つの指標の平均）
    overall_achievement = (
        sales_achievement +
        operating_income_achievement +
        ordinary_income_achievement +
        net_income_achievement
    ) / 4
    
    # 評価レベルを判定
    if overall_achievement >= 100:
        evaluation = "優秀"
        evaluation_color = "success"
    elif overall_achievement >= 90:
        evaluation = "良好"
        evaluation_color = "info"
    elif overall_achievement >= 80:
        evaluation = "普通"
        evaluation_color = "warning"
    else:
        evaluation = "要改善"
        evaluation_color = "danger"
    
    return {
        'overall_achievement': overall_achievement,
        'evaluation': evaluation,
        'evaluation_color': evaluation_color,
        'sales_achievement': sales_achievement,
        'operating_income_achievement': operating_income_achievement,
        'ordinary_income_achievement': ordinary_income_achievement,
        'net_income_achievement': net_income_achievement
    }
