"""
予実差異分析・通知機能モジュール

予算と実績の差異を分析し、予算超過や資金不足時にアラートを生成します。
"""

from typing import Dict, List, Any, Optional


class BudgetVarianceAnalyzer:
    """予実差異分析クラス"""
    
    @staticmethod
    def analyze_variance(
        budget_data: Dict[str, Any],
        actual_data: Dict[str, Any],
        variance_threshold: float = 5.0
    ) -> Dict[str, Any]:
        """
        予実差異を分析
        
        Args:
            budget_data: 予算データ
            actual_data: 実績データ
            variance_threshold: 差異の警告閾値（%）
        
        Returns:
            dict: 差異分析結果
        """
        variance_result = {
            'year': actual_data.get('year', 0),
            'items': [],
            'alerts': []
        }
        
        # 主要項目の差異を計算
        items_to_analyze = [
            ('sales', '売上高'),
            ('cost_of_sales', '売上原価'),
            ('gross_profit', '売上総利益'),
            ('sg_a_expenses', '販売費及び一般管理費'),
            ('operating_income', '営業利益'),
            ('ordinary_income', '経常利益'),
            ('net_income', '当期純利益')
        ]
        
        for item_key, item_name in items_to_analyze:
            budget_value = budget_data.get(item_key, 0)
            actual_value = actual_data.get(item_key, 0)
            
            # 差異を計算
            variance_amount = actual_value - budget_value
            
            if budget_value != 0:
                variance_rate = (variance_amount / budget_value) * 100
            else:
                variance_rate = 0 if variance_amount == 0 else float('inf')
            
            # 差異の評価
            if abs(variance_rate) >= variance_threshold:
                if variance_rate > 0:
                    if item_key in ['sales', 'gross_profit', 'operating_income', 'ordinary_income', 'net_income']:
                        status = 'favorable'  # 好ましい差異
                        status_label = '好調'
                    else:
                        status = 'unfavorable'  # 好ましくない差異
                        status_label = '超過'
                else:
                    if item_key in ['sales', 'gross_profit', 'operating_income', 'ordinary_income', 'net_income']:
                        status = 'unfavorable'
                        status_label = '未達'
                    else:
                        status = 'favorable'
                        status_label = '削減'
            else:
                status = 'within_threshold'
                status_label = '許容範囲'
            
            variance_item = {
                'item_key': item_key,
                'item_name': item_name,
                'budget_value': budget_value,
                'actual_value': actual_value,
                'variance_amount': variance_amount,
                'variance_rate': variance_rate,
                'status': status,
                'status_label': status_label
            }
            
            variance_result['items'].append(variance_item)
            
            # アラートの生成
            if status == 'unfavorable' and abs(variance_rate) >= variance_threshold:
                alert = {
                    'type': 'budget_variance',
                    'severity': 'warning' if abs(variance_rate) < 10 else 'critical',
                    'item_name': item_name,
                    'message': f"{item_name}が予算比{variance_rate:+.2f}%の差異があります",
                    'variance_rate': variance_rate,
                    'variance_amount': variance_amount
                }
                variance_result['alerts'].append(alert)
        
        return variance_result
    
    @staticmethod
    def check_cash_shortage(
        simulation_result: Dict[str, Any],
        minimum_cash_balance: float = 0
    ) -> List[Dict[str, Any]]:
        """
        資金不足をチェック
        
        Args:
            simulation_result: シミュレーション結果
            minimum_cash_balance: 最低現金残高
        
        Returns:
            list: 資金不足アラートのリスト
        """
        alerts = []
        
        for year_result in simulation_result.get('years', []):
            cash_balance = year_result.get('cf', {}).get('ending_cash_balance', 0)
            
            if cash_balance < minimum_cash_balance:
                alert = {
                    'type': 'cash_shortage',
                    'severity': 'critical',
                    'year': year_result.get('year', 0),
                    'message': f"{year_result.get('year', 0)}年度の現金残高が{cash_balance:,.0f}円となり、最低残高{minimum_cash_balance:,.0f}円を下回ります",
                    'cash_balance': cash_balance,
                    'shortage_amount': minimum_cash_balance - cash_balance
                }
                alerts.append(alert)
        
        return alerts
    
    @staticmethod
    def check_debt_service_coverage(
        simulation_result: Dict[str, Any],
        minimum_dscr: float = 1.2
    ) -> List[Dict[str, Any]]:
        """
        債務返済能力をチェック
        
        Args:
            simulation_result: シミュレーション結果
            minimum_dscr: 最低債務返済カバー率
        
        Returns:
            list: 債務返済能力アラートのリスト
        """
        alerts = []
        
        for year_result in simulation_result.get('years', []):
            operating_cash_flow = year_result.get('cf', {}).get('operating_cash_flow', 0)
            
            # 簡易的なDSCRの計算（営業CF ÷ 債務返済額）
            # 実際の実装では、より詳細な計算が必要
            financing_cf = abs(year_result.get('cf', {}).get('financing_cash_flow', 0))
            
            if financing_cf > 0:
                dscr = operating_cash_flow / financing_cf
                
                if dscr < minimum_dscr:
                    alert = {
                        'type': 'debt_service_coverage',
                        'severity': 'warning' if dscr >= 1.0 else 'critical',
                        'year': year_result.get('year', 0),
                        'message': f"{year_result.get('year', 0)}年度の債務返済カバー率が{dscr:.2f}倍となり、基準値{minimum_dscr:.2f}倍を下回ります",
                        'dscr': dscr,
                        'operating_cash_flow': operating_cash_flow,
                        'debt_service': financing_cf
                    }
                    alerts.append(alert)
        
        return alerts
    
    @staticmethod
    def generate_comprehensive_alerts(
        budget_data: Dict[str, Any],
        actual_data: Dict[str, Any],
        simulation_result: Dict[str, Any],
        variance_threshold: float = 5.0,
        minimum_cash_balance: float = 0,
        minimum_dscr: float = 1.2
    ) -> Dict[str, Any]:
        """
        包括的なアラートを生成
        
        Args:
            budget_data: 予算データ
            actual_data: 実績データ
            simulation_result: シミュレーション結果
            variance_threshold: 差異の警告閾値（%）
            minimum_cash_balance: 最低現金残高
            minimum_dscr: 最低債務返済カバー率
        
        Returns:
            dict: 包括的なアラート情報
        """
        all_alerts = []
        
        # 予実差異アラート
        if budget_data and actual_data:
            variance_result = BudgetVarianceAnalyzer.analyze_variance(
                budget_data, actual_data, variance_threshold
            )
            all_alerts.extend(variance_result.get('alerts', []))
        
        # 資金不足アラート
        cash_shortage_alerts = BudgetVarianceAnalyzer.check_cash_shortage(
            simulation_result, minimum_cash_balance
        )
        all_alerts.extend(cash_shortage_alerts)
        
        # 債務返済能力アラート
        dscr_alerts = BudgetVarianceAnalyzer.check_debt_service_coverage(
            simulation_result, minimum_dscr
        )
        all_alerts.extend(dscr_alerts)
        
        # アラートを重要度順にソート
        severity_order = {'critical': 0, 'warning': 1, 'info': 2}
        all_alerts.sort(key=lambda x: severity_order.get(x.get('severity', 'info'), 3))
        
        return {
            'total_alerts': len(all_alerts),
            'critical_count': len([a for a in all_alerts if a.get('severity') == 'critical']),
            'warning_count': len([a for a in all_alerts if a.get('severity') == 'warning']),
            'alerts': all_alerts
        }
    
    @staticmethod
    def format_variance_for_ui(variance_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        予実差異分析結果をUI表示用に整形
        
        Args:
            variance_result: 差異分析結果
        
        Returns:
            dict: UI表示用の整形済みデータ
        """
        formatted_items = []
        
        for item in variance_result.get('items', []):
            formatted_items.append({
                'item_name': item['item_name'],
                'budget_value': round(item['budget_value'], 2),
                'budget_value_formatted': f"{item['budget_value']:,.0f}円",
                'actual_value': round(item['actual_value'], 2),
                'actual_value_formatted': f"{item['actual_value']:,.0f}円",
                'variance_amount': round(item['variance_amount'], 2),
                'variance_amount_formatted': f"{item['variance_amount']:+,.0f}円",
                'variance_rate': round(item['variance_rate'], 2),
                'variance_rate_formatted': f"{item['variance_rate']:+.2f}%",
                'status': item['status'],
                'status_label': item['status_label']
            })
        
        return {
            'year': variance_result.get('year', 0),
            'items': formatted_items,
            'alerts': variance_result.get('alerts', [])
        }
