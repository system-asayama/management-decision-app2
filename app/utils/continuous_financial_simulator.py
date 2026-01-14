"""
連続財務シミュレーションモジュール

個別計画（労務費、設備投資、運転資金、資金調達）を統合し、
3年分の連続財務シミュレーションを実行します。
"""

from typing import Dict, List, Any, Optional


class ContinuousFinancialSimulator:
    """連続財務シミュレータークラス"""
    
    @staticmethod
    def simulate_multi_year_financials(
        base_financials: Dict[str, Any],
        integrated_plan: Dict[str, Any],
        sales_growth_rates: List[float],
        cost_of_sales_ratios: List[float],
        sg_a_ratios: List[float]
    ) -> Dict[str, Any]:
        """
        多年度財務シミュレーションを実行
        
        Args:
            base_financials: 基準年度の財務データ
            integrated_plan: 統合計画データ
            sales_growth_rates: 各年度の売上高成長率（%）のリスト
            cost_of_sales_ratios: 各年度の売上原価率（%）のリスト
            sg_a_ratios: 各年度の販管費率（%）のリスト
        
        Returns:
            dict: シミュレーション結果
        """
        results = {
            'base_year': integrated_plan['base_year'],
            'years': []
        }
        
        # 基準年度の財務データ
        current_sales = base_financials.get('sales', 0)
        current_total_assets = base_financials.get('total_assets', 0)
        current_total_liabilities = base_financials.get('total_liabilities', 0)
        current_total_equity = base_financials.get('total_equity', 0)
        current_cash = base_financials.get('cash', 0)
        
        # 各年度のシミュレーションを実行
        for year_offset, year_plan in enumerate(integrated_plan['years']):
            # 売上高の予測
            if year_offset < len(sales_growth_rates):
                growth_rate = sales_growth_rates[year_offset] / 100
            else:
                growth_rate = 0
            
            current_sales = current_sales * (1 + growth_rate)
            
            # 売上原価の予測
            if year_offset < len(cost_of_sales_ratios):
                cost_of_sales_ratio = cost_of_sales_ratios[year_offset] / 100
            else:
                cost_of_sales_ratio = 0.7  # デフォルト70%
            
            cost_of_sales = current_sales * cost_of_sales_ratio
            gross_profit = current_sales - cost_of_sales
            
            # 販管費の予測（個別計画の労務費を反映）
            labor_cost = year_plan['labor_cost']['total_labor_cost']
            
            if year_offset < len(sg_a_ratios):
                sg_a_ratio = sg_a_ratios[year_offset] / 100
            else:
                sg_a_ratio = 0.2  # デフォルト20%
            
            # 販管費 = 労務費 + その他販管費
            other_sg_a = current_sales * sg_a_ratio - labor_cost
            if other_sg_a < 0:
                other_sg_a = 0
            
            total_sg_a = labor_cost + other_sg_a
            
            # 営業利益の予測
            operating_income = gross_profit - total_sg_a
            
            # 減価償却費（設備投資計画から）
            depreciation = year_plan['capital_investment']['depreciation']
            
            # 営業外損益（資金調達計画の利息支払いを反映）
            interest_expense = year_plan['financing']['interest_payment']
            non_operating_income = 0  # 簡略化のため0とする
            non_operating_expense = interest_expense
            
            # 経常利益の予測
            ordinary_income = operating_income + non_operating_income - non_operating_expense
            
            # 税引前当期純利益（特別損益は0と仮定）
            income_before_tax = ordinary_income
            
            # 法人税等（税率30%と仮定）
            tax_rate = 0.3
            tax_expense = max(0, income_before_tax * tax_rate)
            
            # 当期純利益
            net_income = income_before_tax - tax_expense
            
            # キャッシュフローの予測
            operating_cash_flow = net_income + depreciation
            
            # 投資キャッシュフロー（設備投資計画から）
            capital_investment = year_plan['capital_investment']['total_investment']
            investing_cash_flow = -capital_investment
            
            # 財務キャッシュフロー（資金調達計画から）
            new_borrowing = year_plan['financing']['new_borrowing']
            principal_repayment = year_plan['financing']['principal_repayment']
            financing_cash_flow = new_borrowing - principal_repayment
            
            # 現金残高の予測
            net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
            current_cash = current_cash + net_cash_flow
            
            # 運転資金の変動（運転資金計画から）
            net_working_capital = year_plan['working_capital']['net_working_capital']
            
            # 総資産の予測
            fixed_assets = base_financials.get('fixed_assets', 0) + capital_investment - depreciation
            current_assets = current_cash + net_working_capital
            current_total_assets = fixed_assets + current_assets
            
            # 負債・純資産の予測
            current_total_liabilities = year_plan['financing']['total_debt_balance'] + base_financials.get('other_liabilities', 0)
            current_total_equity = current_total_equity + net_income
            
            # バランス調整
            if current_total_assets != (current_total_liabilities + current_total_equity):
                adjustment = current_total_assets - (current_total_liabilities + current_total_equity)
                current_total_equity += adjustment
            
            # 年度結果を記録
            year_result = {
                'year': year_plan['year'],
                'year_offset': year_offset,
                'pl': {
                    'sales': current_sales,
                    'cost_of_sales': cost_of_sales,
                    'gross_profit': gross_profit,
                    'gross_profit_margin': (gross_profit / current_sales * 100) if current_sales > 0 else 0,
                    'sg_a_expenses': total_sg_a,
                    'labor_cost': labor_cost,
                    'other_sg_a': other_sg_a,
                    'operating_income': operating_income,
                    'operating_margin': (operating_income / current_sales * 100) if current_sales > 0 else 0,
                    'non_operating_income': non_operating_income,
                    'non_operating_expense': non_operating_expense,
                    'ordinary_income': ordinary_income,
                    'ordinary_margin': (ordinary_income / current_sales * 100) if current_sales > 0 else 0,
                    'income_before_tax': income_before_tax,
                    'tax_expense': tax_expense,
                    'net_income': net_income,
                    'net_margin': (net_income / current_sales * 100) if current_sales > 0 else 0
                },
                'bs': {
                    'total_assets': current_total_assets,
                    'current_assets': current_assets,
                    'fixed_assets': fixed_assets,
                    'cash': current_cash,
                    'net_working_capital': net_working_capital,
                    'total_liabilities': current_total_liabilities,
                    'total_debt': year_plan['financing']['total_debt_balance'],
                    'total_equity': current_total_equity
                },
                'cf': {
                    'operating_cash_flow': operating_cash_flow,
                    'investing_cash_flow': investing_cash_flow,
                    'financing_cash_flow': financing_cash_flow,
                    'net_cash_flow': net_cash_flow,
                    'ending_cash_balance': current_cash
                },
                'ratios': {
                    'roe': (net_income / current_total_equity * 100) if current_total_equity > 0 else 0,
                    'roa': (net_income / current_total_assets * 100) if current_total_assets > 0 else 0,
                    'debt_equity_ratio': (current_total_liabilities / current_total_equity * 100) if current_total_equity > 0 else 0,
                    'current_ratio': (current_assets / current_total_liabilities * 100) if current_total_liabilities > 0 else 0
                }
            }
            
            results['years'].append(year_result)
        
        return results
    
    @staticmethod
    def format_simulation_for_ui(simulation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        シミュレーション結果をUI表示用に整形
        
        Args:
            simulation_result: シミュレーション結果
        
        Returns:
            dict: UI表示用の整形済みデータ
        """
        formatted_years = []
        
        for year_result in simulation_result['years']:
            formatted_years.append({
                'year': year_result['year'],
                'year_label': f"{year_result['year']}年度",
                'pl': {
                    'sales': round(year_result['pl']['sales'], 2),
                    'sales_formatted': f"{year_result['pl']['sales']:,.0f}円",
                    'gross_profit': round(year_result['pl']['gross_profit'], 2),
                    'gross_profit_formatted': f"{year_result['pl']['gross_profit']:,.0f}円",
                    'gross_profit_margin': round(year_result['pl']['gross_profit_margin'], 2),
                    'gross_profit_margin_formatted': f"{year_result['pl']['gross_profit_margin']:.2f}%",
                    'operating_income': round(year_result['pl']['operating_income'], 2),
                    'operating_income_formatted': f"{year_result['pl']['operating_income']:,.0f}円",
                    'operating_margin': round(year_result['pl']['operating_margin'], 2),
                    'operating_margin_formatted': f"{year_result['pl']['operating_margin']:.2f}%",
                    'ordinary_income': round(year_result['pl']['ordinary_income'], 2),
                    'ordinary_income_formatted': f"{year_result['pl']['ordinary_income']:,.0f}円",
                    'ordinary_margin': round(year_result['pl']['ordinary_margin'], 2),
                    'ordinary_margin_formatted': f"{year_result['pl']['ordinary_margin']:.2f}%",
                    'net_income': round(year_result['pl']['net_income'], 2),
                    'net_income_formatted': f"{year_result['pl']['net_income']:,.0f}円",
                    'net_margin': round(year_result['pl']['net_margin'], 2),
                    'net_margin_formatted': f"{year_result['pl']['net_margin']:.2f}%"
                },
                'bs': {
                    'total_assets': round(year_result['bs']['total_assets'], 2),
                    'total_assets_formatted': f"{year_result['bs']['total_assets']:,.0f}円",
                    'total_liabilities': round(year_result['bs']['total_liabilities'], 2),
                    'total_liabilities_formatted': f"{year_result['bs']['total_liabilities']:,.0f}円",
                    'total_equity': round(year_result['bs']['total_equity'], 2),
                    'total_equity_formatted': f"{year_result['bs']['total_equity']:,.0f}円",
                    'cash': round(year_result['bs']['cash'], 2),
                    'cash_formatted': f"{year_result['bs']['cash']:,.0f}円"
                },
                'cf': {
                    'operating_cash_flow': round(year_result['cf']['operating_cash_flow'], 2),
                    'operating_cash_flow_formatted': f"{year_result['cf']['operating_cash_flow']:,.0f}円",
                    'investing_cash_flow': round(year_result['cf']['investing_cash_flow'], 2),
                    'investing_cash_flow_formatted': f"{year_result['cf']['investing_cash_flow']:,.0f}円",
                    'financing_cash_flow': round(year_result['cf']['financing_cash_flow'], 2),
                    'financing_cash_flow_formatted': f"{year_result['cf']['financing_cash_flow']:,.0f}円",
                    'net_cash_flow': round(year_result['cf']['net_cash_flow'], 2),
                    'net_cash_flow_formatted': f"{year_result['cf']['net_cash_flow']:,.0f}円",
                    'ending_cash_balance': round(year_result['cf']['ending_cash_balance'], 2),
                    'ending_cash_balance_formatted': f"{year_result['cf']['ending_cash_balance']:,.0f}円"
                },
                'ratios': {
                    'roe': round(year_result['ratios']['roe'], 2),
                    'roe_formatted': f"{year_result['ratios']['roe']:.2f}%",
                    'roa': round(year_result['ratios']['roa'], 2),
                    'roa_formatted': f"{year_result['ratios']['roa']:.2f}%",
                    'debt_equity_ratio': round(year_result['ratios']['debt_equity_ratio'], 2),
                    'debt_equity_ratio_formatted': f"{year_result['ratios']['debt_equity_ratio']:.2f}%"
                }
            })
        
        return {
            'base_year': simulation_result['base_year'],
            'years': formatted_years
        }
