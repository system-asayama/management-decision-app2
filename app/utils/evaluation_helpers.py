"""
評価ヘルパー関数
前年比較により評価記号（◎◯△×）を返す
"""


def evaluate_yoy(value_this_year, value_prev_year):
    """
    前年比較により評価記号を返す
    
    Args:
        value_this_year: 当年の値
        value_prev_year: 前年の値
    
    Returns:
        dict: {
            'ratio': float,  # 前年比（%）
            'grade': str     # 評価記号（◎◯△×）
        }
    
    評価基準:
        - +10%以上：◎
        - 0〜+10%：◯
        - 0〜-10%：△
        - -10%未満：×
    """
    # 値をfloatに変換
    try:
        this_year = float(value_this_year) if value_this_year is not None else 0.0
        prev_year = float(value_prev_year) if value_prev_year is not None else 0.0
    except (ValueError, TypeError):
        this_year = 0.0
        prev_year = 0.0
    
    # 前年が0の場合の処理
    if prev_year == 0:
        if this_year > 0:
            ratio = 100.0  # 前年0から増加した場合は+100%とする
            grade = '◎'
        elif this_year == 0:
            ratio = 0.0
            grade = '◯'
        else:
            ratio = -100.0  # 前年0から減少した場合は-100%とする
            grade = '×'
    else:
        # 前年比を計算（%）
        ratio = ((this_year - prev_year) / prev_year) * 100.0
        
        # 評価記号を決定
        if ratio >= 10.0:
            grade = '◎'
        elif ratio >= 0.0:
            grade = '◯'
        elif ratio >= -10.0:
            grade = '△'
        else:
            grade = '×'
    
    return {
        'ratio': round(ratio, 2),
        'grade': grade
    }


def evaluate_multiple_indicators(indicators_this_year, indicators_prev_year):
    """
    複数の指標を一括評価する
    
    Args:
        indicators_this_year: dict - 当年の指標（キー: 指標名、値: 数値）
        indicators_prev_year: dict - 前年の指標（キー: 指標名、値: 数値）
    
    Returns:
        dict: {
            指標名: {
                'thisYear': float,
                'prevYear': float,
                'ratio': float,
                'grade': str
            }
        }
    """
    results = {}
    
    # すべての指標名を取得（当年と前年の和集合）
    all_indicators = set(indicators_this_year.keys()) | set(indicators_prev_year.keys())
    
    for indicator_name in all_indicators:
        this_year_value = indicators_this_year.get(indicator_name, 0.0)
        prev_year_value = indicators_prev_year.get(indicator_name, 0.0)
        
        evaluation = evaluate_yoy(this_year_value, prev_year_value)
        
        results[indicator_name] = {
            'thisYear': float(this_year_value) if this_year_value is not None else 0.0,
            'prevYear': float(prev_year_value) if prev_year_value is not None else 0.0,
            'ratio': evaluation['ratio'],
            'grade': evaluation['grade']
        }
    
    return results
