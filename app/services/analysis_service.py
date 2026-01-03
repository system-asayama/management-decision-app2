"""
経営分析サービス
4つの視点（成長力、収益力、資金力、生産力）から経営指標を計算する
"""
from typing import Dict, Any, List


class AnalysisService:
    """経営分析サービス"""
    
    @staticmethod
    def calculate_growth_indicators(current_data: Dict[str, Any], previous_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        成長力の指標を計算
        
        Args:
            current_data: 当年度のデータ
            previous_data: 前年度のデータ
        
        Returns:
            成長力の指標
        """
        def growth_rate(current, previous):
            """成長率を計算（％）"""
            if previous == 0:
                return 0
            return ((current / previous) - 1) * 100
        
        return {
            'sales_growth_rate': growth_rate(
                current_data.get('sales', 0),
                previous_data.get('sales', 0)
            ),
            'cost_of_sales_growth_rate': growth_rate(
                current_data.get('cost_of_sales', 0),
                previous_data.get('cost_of_sales', 0)
            ),
            'added_value_growth_rate': growth_rate(
                current_data.get('gross_added_value', 0),
                previous_data.get('gross_added_value', 0)
            ),
            'labor_cost_growth_rate': growth_rate(
                current_data.get('total_labor_cost', 0),
                previous_data.get('total_labor_cost', 0)
            ),
            'executive_compensation_growth_rate': growth_rate(
                current_data.get('executive_compensation', 0),
                previous_data.get('executive_compensation', 0)
            ),
            'capital_regeneration_growth_rate': growth_rate(
                current_data.get('capital_regeneration_cost', 0),
                previous_data.get('capital_regeneration_cost', 0)
            ),
            'research_development_growth_rate': growth_rate(
                current_data.get('research_development_expenses', 0),
                previous_data.get('research_development_expenses', 0)
            ),
            'general_expenses_growth_rate': growth_rate(
                current_data.get('general_expenses', 0),
                previous_data.get('general_expenses', 0)
            ),
            'fixed_assets_growth_rate': growth_rate(
                current_data.get('fixed_assets', 0),
                previous_data.get('fixed_assets', 0)
            ),
            'liabilities_growth_rate': growth_rate(
                current_data.get('total_liabilities', 0),
                previous_data.get('total_liabilities', 0)
            ),
            'income_before_tax_growth_rate': growth_rate(
                current_data.get('income_before_tax', 0),
                previous_data.get('income_before_tax', 0)
            ),
            'equity_growth_rate': growth_rate(
                current_data.get('net_assets', 0),
                previous_data.get('net_assets', 0)
            )
        }
    
    @staticmethod
    def calculate_profitability_indicators(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        収益力の指標を計算
        
        Args:
            data: 財務データ
        
        Returns:
            収益力の指標
        """
        sales = data.get('sales', 0)
        ordinary_income = data.get('ordinary_income', 0)
        operating_income = data.get('operating_income', 0)
        gross_profit = data.get('gross_profit', 0)
        gross_added_value = data.get('gross_added_value', 0)
        cost_of_sales = data.get('cost_of_sales', 0)
        
        total_assets = data.get('total_assets', 0)
        net_assets = data.get('net_assets', 0)
        
        # 経営資本 = 総資本 - 有価証券 - 短期貸付金 - 投資用資産
        # 簡易計算として総資本を使用
        operating_capital = total_assets
        
        # 限界利益 = 売上高 - 変動費
        variable_expenses = data.get('variable_expenses', 0)
        marginal_profit = sales - variable_expenses
        
        return {
            # ① 総資本経常利益率 = 経常利益 ÷ 総資本
            'return_on_assets': (ordinary_income / total_assets * 100) if total_assets > 0 else 0,
            # a. 売上高経常利益率 = 経常利益 ÷ 売上高
            'ordinary_income_to_sales_ratio': (ordinary_income / sales * 100) if sales > 0 else 0,
            # b. 総資本回転率 = 売上高 ÷ 総資本
            'total_assets_turnover': (sales / total_assets) if total_assets > 0 else 0,
            
            # ② 自己資本経常利益率 = 経常利益 ÷ 自己資本
            'return_on_equity': (ordinary_income / net_assets * 100) if net_assets > 0 else 0,
            # b. 自己資本回転率 = 売上高 ÷ 自己資本
            'equity_turnover': (sales / net_assets) if net_assets > 0 else 0,
            
            # ③ 経営資本営業利益率 = 営業利益 ÷ 経営資本
            'return_on_operating_capital': (operating_income / operating_capital * 100) if operating_capital > 0 else 0,
            # a. 売上高営業利益率 = 営業利益 ÷ 売上高
            'operating_income_to_sales_ratio': (operating_income / sales * 100) if sales > 0 else 0,
            # b. 経営資本回転率 = 売上高 ÷ 経営資本
            'operating_capital_turnover': (sales / operating_capital) if operating_capital > 0 else 0,
            
            # ④ 売上高総利益率 = 売上総利益 ÷ 売上高
            'gross_profit_margin': (gross_profit / sales * 100) if sales > 0 else 0,
            
            # ⑤ 売上高付加価値率 = 付加価値 ÷ 売上高
            'added_value_to_sales_ratio': (gross_added_value / sales * 100) if sales > 0 else 0,
            
            # ⑥ 限界利益率 = 限界利益 ÷ 売上高
            'marginal_profit_ratio': (marginal_profit / sales * 100) if sales > 0 else 0,
            
            # ⑦ 売上高売上原価率 = 売上原価 ÷ 売上高
            'cost_of_sales_ratio': (cost_of_sales / sales * 100) if sales > 0 else 0
        }
    
    @staticmethod
    def calculate_financial_strength_indicators(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        資金力の指標を計算
        
        Args:
            data: 財務データ
        
        Returns:
            資金力の指標
        """
        # 資産
        current_assets = data.get('current_assets', 0)
        fixed_assets = data.get('fixed_assets', 0)
        total_assets = data.get('total_assets', 0)
        cash_on_hand = data.get('cash_on_hand', 0)
        trade_receivables = data.get('trade_receivables', 0)
        inventory_assets = data.get('inventory_assets', 0)
        tangible_fixed_assets = data.get('tangible_fixed_assets', 0)
        
        # 負債
        current_liabilities = data.get('current_liabilities', 0)
        fixed_liabilities = data.get('fixed_liabilities', 0)
        total_liabilities = data.get('total_liabilities', 0)
        trade_payables = data.get('trade_payables', 0)
        total_short_term_debt = data.get('total_short_term_debt', 0)
        long_term_debt = data.get('long_term_debt_excluding_executive', 0)
        
        # 純資産
        net_assets = data.get('net_assets', 0)
        
        # 売上高（回転率計算用）
        sales = data.get('sales', 0)
        cost_of_sales = data.get('cost_of_sales', 0)
        
        # 当座資産 = 現預金 + 売掛債権
        quick_assets = cash_on_hand + trade_receivables
        
        # 総借入金
        total_debt = total_short_term_debt + long_term_debt
        
        # 非償却資産（土地など）- 簡易計算として固定資産の30%と仮定
        non_depreciable_assets = tangible_fixed_assets * 0.3
        
        # 償却資産
        depreciable_assets = tangible_fixed_assets - non_depreciable_assets
        
        return {
            # 資金調達源泉の健全性
            # ① 自己調達率（自己資本比率） = 自己資本 ÷ 総資本
            'equity_ratio': (net_assets / total_assets * 100) if total_assets > 0 else 0,
            # ② 金融調達率 = 借入金 ÷ 総資本
            'debt_ratio': (total_debt / total_assets * 100) if total_assets > 0 else 0,
            # ④ 信用調達率 = 買掛債務 ÷ 総資本
            'trade_payables_ratio': (trade_payables / total_assets * 100) if total_assets > 0 else 0,
            
            # 資金調達余力
            # ⑤ 借入金依存率 = 借入金 ÷ 総資本
            'borrowing_dependency_ratio': (total_debt / total_assets * 100) if total_assets > 0 else 0,
            # ⑥ 担保余力 = (有形固定資産 - 借入金) ÷ 有形固定資産
            'collateral_margin': ((tangible_fixed_assets - total_debt) / tangible_fixed_assets * 100) if tangible_fixed_assets > 0 else 0,
            
            # 資金運用能力
            # ⑧ 現預金回転期間 = 現預金 ÷ (売上高 ÷ 365)
            'cash_turnover_days': (cash_on_hand / (sales / 365)) if sales > 0 else 0,
            # ⑨ 売掛債権回転率 = 売上高 ÷ 売掛債権
            'receivables_turnover': (sales / trade_receivables) if trade_receivables > 0 else 0,
            # ⑩ 売掛債権回転期間 = 売掛債権 ÷ (売上高 ÷ 365)
            'receivables_turnover_days': (trade_receivables / (sales / 365)) if sales > 0 else 0,
            # ⑪ 買掛債務回転率 = 売上原価 ÷ 買掛債務
            'payables_turnover': (cost_of_sales / trade_payables) if trade_payables > 0 else 0,
            # ⑫ 買掛債務回転期間 = 買掛債務 ÷ (売上原価 ÷ 365)
            'payables_turnover_days': (trade_payables / (cost_of_sales / 365)) if cost_of_sales > 0 else 0,
            # ⑬ 棚卸資産回転率 = 売上原価 ÷ 棚卸資産
            'inventory_turnover': (cost_of_sales / inventory_assets) if inventory_assets > 0 else 0,
            # ⑭ 棚卸資産回転期間 = 棚卸資産 ÷ (売上原価 ÷ 365)
            'inventory_turnover_days': (inventory_assets / (cost_of_sales / 365)) if cost_of_sales > 0 else 0,
            
            # 資金返済能力（短期）
            # ⑮ 流動比率 = 流動資産 ÷ 流動負債
            'current_ratio': (current_assets / current_liabilities * 100) if current_liabilities > 0 else 0,
            # ⑯ 当座比率 = 当座資産 ÷ 流動負債
            'quick_ratio': (quick_assets / current_liabilities * 100) if current_liabilities > 0 else 0,
            # ⑰ 現預金比率 = 現預金 ÷ 流動負債
            'cash_ratio': (cash_on_hand / current_liabilities * 100) if current_liabilities > 0 else 0,
            
            # 資金返済能力（長期）
            # ⑱ 長期適合率 = 固定資産 ÷ (自己資本 + 固定負債)
            'fixed_assets_ratio': (fixed_assets / (net_assets + fixed_liabilities) * 100) if (net_assets + fixed_liabilities) > 0 else 0,
            # ⑲ 非償却資産自己資本比率 = 非償却資産 ÷ 自己資本
            'non_depreciable_assets_to_equity_ratio': (non_depreciable_assets / net_assets * 100) if net_assets > 0 else 0,
            # ⑳ 償却資産長期負債比率 = 償却資産 ÷ 固定負債
            'depreciable_assets_to_long_term_debt_ratio': (depreciable_assets / fixed_liabilities * 100) if fixed_liabilities > 0 else 0
        }
    
    @staticmethod
    def calculate_productivity_indicators(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生産力の指標を計算
        
        Args:
            data: 財務データ
        
        Returns:
            生産力の指標
        """
        sales = data.get('sales', 0)
        gross_added_value = data.get('gross_added_value', 0)
        total_labor_cost = data.get('total_labor_cost', 0)
        income_before_tax = data.get('income_before_tax', 0)
        
        total_assets = data.get('total_assets', 0)
        tangible_fixed_assets = data.get('tangible_fixed_assets', 0)
        
        # 従業員数
        employee_count = data.get('employee_count', 1)  # デフォルト1（ゼロ除算回避）
        
        # 平均設備残高（簡易計算として有形固定資産を使用）
        average_equipment_balance = tangible_fixed_assets
        
        return {
            # ① 総資本付加価値率 = 粗付加価値 ÷ 総資本
            'added_value_to_total_assets_ratio': (gross_added_value / total_assets * 100) if total_assets > 0 else 0,
            # a. 売上高付加価値率 = 粗付加価値 ÷ 売上高
            'added_value_to_sales_ratio': (gross_added_value / sales * 100) if sales > 0 else 0,
            # b. 総資本回転率 = 売上高 ÷ 総資本
            'total_assets_turnover': (sales / total_assets) if total_assets > 0 else 0,
            
            # ② 付加価値労働生産性 = 粗付加価値 ÷ 平均従業員数
            'labor_productivity': (gross_added_value / employee_count) if employee_count > 0 else 0,
            # b. 従業員一人当り売上高 = 売上高 ÷ 平均従業員数
            'sales_per_employee': (sales / employee_count) if employee_count > 0 else 0,
            
            # ③ 利益生産性 = 税引前当期純利益 ÷ 平均従業員数
            'profit_per_employee': (income_before_tax / employee_count) if employee_count > 0 else 0,
            
            # ④ 労働分配率 = 総人件費 ÷ 粗付加価値
            'labor_distribution_ratio': (total_labor_cost / gross_added_value * 100) if gross_added_value > 0 else 0,
            
            # ⑤ 設備投資効率 = 粗付加価値 ÷ 平均設備残高
            'equipment_investment_efficiency': (gross_added_value / average_equipment_balance * 100) if average_equipment_balance > 0 else 0,
            
            # ⑥ 労働装備高 = 平均設備残高 ÷ 平均従業員数
            'equipment_per_employee': (average_equipment_balance / employee_count) if employee_count > 0 else 0
        }
    
    @staticmethod
    def calculate_all_indicators(current_data: Dict[str, Any], previous_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        すべての経営指標を計算
        
        Args:
            current_data: 当年度のデータ
            previous_data: 前年度のデータ（成長力計算用、オプション）
        
        Returns:
            すべての経営指標
        """
        result = {
            'profitability': AnalysisService.calculate_profitability_indicators(current_data),
            'financial_strength': AnalysisService.calculate_financial_strength_indicators(current_data),
            'productivity': AnalysisService.calculate_productivity_indicators(current_data)
        }
        
        if previous_data:
            result['growth'] = AnalysisService.calculate_growth_indicators(current_data, previous_data)
        
        return result
