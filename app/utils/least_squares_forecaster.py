"""
最小二乗法による予測モジュール

過去のデータから最小二乗法（線形回帰）を用いて将来の値を予測します。
"""

from typing import List, Dict, Any, Tuple
import math


def calculate_least_squares(x_values: List[float], y_values: List[float]) -> Tuple[float, float]:
    """
    最小二乗法で線形回帰の傾きと切片を計算
    
    Args:
        x_values: X軸の値のリスト（例: 年度番号）
        y_values: Y軸の値のリスト（例: 売上高）
    
    Returns:
        (傾き, 切片)のタプル
    """
    if len(x_values) != len(y_values):
        raise ValueError("x_valuesとy_valuesの長さが一致しません")
    
    if len(x_values) < 2:
        raise ValueError("最小2つのデータポイントが必要です")
    
    n = len(x_values)
    
    # 平均値を計算
    x_mean = sum(x_values) / n
    y_mean = sum(y_values) / n
    
    # 傾き（slope）を計算
    numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
    denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        # 全てのx値が同じ場合
        slope = 0
    else:
        slope = numerator / denominator
    
    # 切片（intercept）を計算
    intercept = y_mean - slope * x_mean
    
    return slope, intercept


def predict_value(x: float, slope: float, intercept: float) -> float:
    """
    線形回帰式を用いて値を予測
    
    Args:
        x: 予測したいX値
        slope: 傾き
        intercept: 切片
    
    Returns:
        予測値
    """
    return slope * x + intercept


def calculate_r_squared(x_values: List[float], y_values: List[float], slope: float, intercept: float) -> float:
    """
    決定係数（R²）を計算
    
    Args:
        x_values: X軸の値のリスト
        y_values: Y軸の値のリスト
        slope: 傾き
        intercept: 切片
    
    Returns:
        決定係数（0～1の値、1に近いほど予測精度が高い）
    """
    if len(y_values) < 2:
        return 0.0
    
    # 実測値の平均
    y_mean = sum(y_values) / len(y_values)
    
    # 総平方和（SST: Total Sum of Squares）
    sst = sum((y - y_mean) ** 2 for y in y_values)
    
    if sst == 0:
        return 1.0
    
    # 残差平方和（SSE: Sum of Squared Errors）
    sse = sum((y_values[i] - predict_value(x_values[i], slope, intercept)) ** 2 for i in range(len(y_values)))
    
    # 決定係数
    r_squared = 1 - (sse / sst)
    
    return max(0.0, min(1.0, r_squared))


def forecast_sales(historical_data: List[Dict[str, Any]], forecast_years: int = 5) -> Dict[str, Any]:
    """
    売上高の予測を実行
    
    Args:
        historical_data: 過去のデータのリスト
            各データは以下のキーを持つ辞書:
            - year: 年度（整数）
            - sales: 売上高（数値）
        forecast_years: 予測する年数
    
    Returns:
        予測結果の辞書
    """
    if not historical_data or len(historical_data) < 2:
        raise ValueError("最小2年分の過去データが必要です")
    
    # データを年度順にソート
    sorted_data = sorted(historical_data, key=lambda x: x['year'])
    
    # X軸（年度番号）とY軸（売上高）を抽出
    x_values = [float(i) for i in range(len(sorted_data))]
    y_values = [float(d['sales']) for d in sorted_data]
    
    # 最小二乗法で傾きと切片を計算
    slope, intercept = calculate_least_squares(x_values, y_values)
    
    # 決定係数を計算
    r_squared = calculate_r_squared(x_values, y_values, slope, intercept)
    
    # 過去データの予測値を計算（グラフ表示用）
    historical_predictions = []
    for i, data in enumerate(sorted_data):
        predicted = predict_value(float(i), slope, intercept)
        historical_predictions.append({
            'year': data['year'],
            'actual': data['sales'],
            'predicted': predicted,
            'error': data['sales'] - predicted
        })
    
    # 将来の予測を計算
    future_predictions = []
    last_year = sorted_data[-1]['year']
    last_index = len(sorted_data) - 1
    
    for i in range(1, forecast_years + 1):
        predicted = predict_value(float(last_index + i), slope, intercept)
        future_predictions.append({
            'year': last_year + i,
            'predicted': max(0, predicted)  # 負の値にならないように
        })
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'historical_predictions': historical_predictions,
        'future_predictions': future_predictions,
        'equation': f'y = {slope:.2f}x + {intercept:.2f}'
    }


def forecast_multiple_metrics(historical_data: List[Dict[str, Any]], metrics: List[str], forecast_years: int = 5) -> Dict[str, Any]:
    """
    複数の財務指標を予測
    
    Args:
        historical_data: 過去のデータのリスト
            各データは以下のキーを持つ辞書:
            - year: 年度（整数）
            - その他の指標（metrics引数で指定）
        metrics: 予測する指標名のリスト（例: ['sales', 'operating_income', 'net_income']）
        forecast_years: 予測する年数
    
    Returns:
        指標ごとの予測結果の辞書
    """
    if not historical_data or len(historical_data) < 2:
        raise ValueError("最小2年分の過去データが必要です")
    
    results = {}
    
    for metric in metrics:
        # 指標のデータを抽出
        metric_data = []
        for data in historical_data:
            if metric in data:
                metric_data.append({
                    'year': data['year'],
                    'sales': data[metric]  # forecast_sales関数を再利用するため'sales'キーを使用
                })
        
        if len(metric_data) >= 2:
            try:
                # 予測を実行
                forecast_result = forecast_sales(metric_data, forecast_years)
                results[metric] = forecast_result
            except Exception as e:
                results[metric] = {'error': str(e)}
        else:
            results[metric] = {'error': '十分なデータがありません'}
    
    return results


def calculate_growth_rate(historical_data: List[Dict[str, Any]], metric: str = 'sales') -> float:
    """
    平均成長率を計算
    
    Args:
        historical_data: 過去のデータのリスト
        metric: 計算する指標名
    
    Returns:
        平均成長率（%）
    """
    if not historical_data or len(historical_data) < 2:
        return 0.0
    
    sorted_data = sorted(historical_data, key=lambda x: x['year'])
    
    growth_rates = []
    for i in range(1, len(sorted_data)):
        prev_value = float(sorted_data[i-1].get(metric, 0))
        curr_value = float(sorted_data[i].get(metric, 0))
        
        if prev_value > 0:
            growth_rate = ((curr_value - prev_value) / prev_value) * 100
            growth_rates.append(growth_rate)
    
    if not growth_rates:
        return 0.0
    
    return sum(growth_rates) / len(growth_rates)


def calculate_trend_strength(r_squared: float) -> str:
    """
    トレンドの強さを評価
    
    Args:
        r_squared: 決定係数
    
    Returns:
        トレンドの強さの説明
    """
    if r_squared >= 0.9:
        return "非常に強い"
    elif r_squared >= 0.7:
        return "強い"
    elif r_squared >= 0.5:
        return "中程度"
    elif r_squared >= 0.3:
        return "弱い"
    else:
        return "非常に弱い"


def analyze_cost_structure(sales_data: List[float], cost_data: List[float]) -> Dict[str, Any]:
    """
    費用構造を分析し、固定費と変動費率を推定
    
    Args:
        sales_data: 売上高のリスト
        cost_data: 費用のリスト
    
    Returns:
        固定費と変動費率を含む辞書
    """
    if len(sales_data) != len(cost_data):
        raise ValueError("売上データと費用データの長さが一致しません")
    
    if len(sales_data) < 2:
        raise ValueError("最小2つのデータポイントが必要です")
    
    # X軸（売上高）とY軸（費用）で回帰分析
    # Y = aX + b
    # a: 変動費率（Variable Cost Ratio）
    # b: 固定費（Fixed Cost）
    
    variable_cost_ratio, fixed_cost = calculate_least_squares(sales_data, cost_data)
    
    # 決定係数を計算
    r_squared = calculate_r_squared(sales_data, cost_data, variable_cost_ratio, fixed_cost)
    
    # 損益分岐点売上高を計算
    # 損益分岐点 = 固定費 / (1 - 変動費率)
    if variable_cost_ratio < 1.0:
        break_even_sales = fixed_cost / (1 - variable_cost_ratio)
    else:
        break_even_sales = None  # 変動費率が100%以上の場合は損益分岐点なし
    
    return {
        'variable_cost_ratio': variable_cost_ratio,
        'fixed_cost': fixed_cost,
        'r_squared': r_squared,
        'break_even_sales': break_even_sales,
        'equation': f'費用 = {variable_cost_ratio:.4f} × 売上高 + {fixed_cost:.2f}',
        'interpretation': {
            'variable_cost_ratio_percent': variable_cost_ratio * 100,
            'contribution_margin_ratio': (1 - variable_cost_ratio) * 100 if variable_cost_ratio < 1.0 else 0
        }
    }


def forecast_costs(historical_data: List[Dict[str, Any]], cost_metric: str, forecast_years: int = 5) -> Dict[str, Any]:
    """
    費用の予測を実行
    
    Args:
        historical_data: 過去のデータのリスト
            各データは以下のキーを持つ辞書:
            - year: 年度（整数）
            - sales: 売上高（数値）
            - cost_metric: 費用項目（例: 'cost_of_sales', 'operating_expenses'）
        cost_metric: 予測する費用項目名
        forecast_years: 予測する年数
    
    Returns:
        予測結果の辞書（固定費と変動費率を含む）
    """
    if not historical_data or len(historical_data) < 2:
        raise ValueError("最小2年分の過去データが必要です")
    
    # データを年度順にソート
    sorted_data = sorted(historical_data, key=lambda x: x['year'])
    
    # 売上高と費用を抽出
    sales_data = [float(d['sales']) for d in sorted_data]
    cost_data = [float(d.get(cost_metric, 0)) for d in sorted_data]
    
    # 費用構造を分析（固定費と変動費率）
    cost_structure = analyze_cost_structure(sales_data, cost_data)
    
    # 売上高の予測
    sales_forecast = forecast_sales(
        [{'year': d['year'], 'sales': d['sales']} for d in sorted_data],
        forecast_years
    )
    
    # 費用の予測（売上高の予測値 × 変動費率 + 固定費）
    future_cost_predictions = []
    for sales_pred in sales_forecast['future_predictions']:
        predicted_cost = (
            sales_pred['predicted'] * cost_structure['variable_cost_ratio'] +
            cost_structure['fixed_cost']
        )
        future_cost_predictions.append({
            'year': sales_pred['year'],
            'predicted_sales': sales_pred['predicted'],
            'predicted_cost': max(0, predicted_cost)
        })
    
    # 過去データの予測値を計算
    historical_cost_predictions = []
    for i, data in enumerate(sorted_data):
        predicted_cost = (
            data['sales'] * cost_structure['variable_cost_ratio'] +
            cost_structure['fixed_cost']
        )
        actual_cost = data.get(cost_metric, 0)
        historical_cost_predictions.append({
            'year': data['year'],
            'actual_sales': data['sales'],
            'actual_cost': actual_cost,
            'predicted_cost': predicted_cost,
            'error': actual_cost - predicted_cost
        })
    
    return {
        'cost_structure': cost_structure,
        'sales_forecast': sales_forecast,
        'historical_cost_predictions': historical_cost_predictions,
        'future_cost_predictions': future_cost_predictions
    }
