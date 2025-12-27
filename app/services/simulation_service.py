"""
シミュレーションサービス
複数年度の経営予測、内部留保シミュレーション、借入金許容限度額分析などを実行する
"""
from typing import Dict, Any, List
from decimal import Decimal


class SimulationService:
    """シミュレーションサービス"""
    
    @staticmethod
    def simulate_multi_year_plan(
        base_data: Dict[str, Any],
        assumptions: Dict[str, Any],
        years: int = 3
    ) -> List[Dict[str, Any]]:
        """
        複数年度の経営計画をシミュレーション
        
        Args:
            base_data: 基準年度のデータ
            assumptions: シミュレーション前提条件
            years: シミュレーション年数
        
        Returns:
            各年度のシミュレーション結果
        """
        results = []
        
        # 前提条件の取得
        sales_growth_rate = assumptions.get('sales_growth_rate', 0.05)  # 売上成長率（デフォルト5%）
        cost_ratio = assumptions.get('cost_ratio', 0.60)  # 売上原価率（デフォルト60%）
        operating_expense_ratio = assumptions.get('operating_expense_ratio', 0.25)  # 販管費率（デフォルト25%）
        tax_rate = assumptions.get('tax_rate', 0.30)  # 税率（デフォルト30%）
        dividend_payout_ratio = assumptions.get('dividend_payout_ratio', 0.30)  # 配当性向（デフォルト30%）
        
        # 基準年度のデータ
        current_sales = base_data.get('sales', 0)
        current_total_assets = base_data.get('total_assets', 0)
        current_net_assets = base_data.get('net_assets', 0)
        current_retained_earnings = base_data.get('retained_earnings', 0)
        
        for year in range(1, years + 1):
            # 売上高の予測
            projected_sales = current_sales * ((1 + sales_growth_rate) ** year)
            
            # 売上原価の予測
            projected_cost_of_sales = projected_sales * cost_ratio
            
            # 売上総利益
            projected_gross_profit = projected_sales - projected_cost_of_sales
            
            # 販売費及び一般管理費
            projected_operating_expenses = projected_sales * operating_expense_ratio
            
            # 営業利益
            projected_operating_income = projected_gross_profit - projected_operating_expenses
            
            # 経常利益（営業外損益は簡易計算で0とする）
            projected_ordinary_income = projected_operating_income
            
            # 税引前当期純利益
            projected_income_before_tax = projected_ordinary_income
            
            # 法人税等
            projected_income_tax = projected_income_before_tax * tax_rate
            
            # 当期純利益
            projected_net_income = projected_income_before_tax - projected_income_tax
            
            # 配当金
            projected_dividends = projected_net_income * dividend_payout_ratio
            
            # 内部留保（利益剰余金の増加）
            internal_reserve = projected_net_income - projected_dividends
            
            # 累積利益剰余金
            accumulated_retained_earnings = current_retained_earnings + (internal_reserve * year)
            
            # 自己資本の増加
            projected_net_assets = current_net_assets + (internal_reserve * year)
            
            # 総資産の予測（簡易計算: 売上高の伸び率に比例）
            projected_total_assets = current_total_assets * ((1 + sales_growth_rate) ** year)
            
            # 自己資本比率
            equity_ratio = (projected_net_assets / projected_total_assets * 100) if projected_total_assets > 0 else 0
            
            # ROE（自己資本経常利益率）
            roe = (projected_ordinary_income / projected_net_assets * 100) if projected_net_assets > 0 else 0
            
            # ROA（総資本経常利益率）
            roa = (projected_ordinary_income / projected_total_assets * 100) if projected_total_assets > 0 else 0
            
            results.append({
                'year': year,
                'sales': projected_sales,
                'cost_of_sales': projected_cost_of_sales,
                'gross_profit': projected_gross_profit,
                'operating_expenses': projected_operating_expenses,
                'operating_income': projected_operating_income,
                'ordinary_income': projected_ordinary_income,
                'income_before_tax': projected_income_before_tax,
                'income_tax': projected_income_tax,
                'net_income': projected_net_income,
                'dividends': projected_dividends,
                'internal_reserve': internal_reserve,
                'accumulated_retained_earnings': accumulated_retained_earnings,
                'net_assets': projected_net_assets,
                'total_assets': projected_total_assets,
                'equity_ratio': equity_ratio,
                'roe': roe,
                'roa': roa
            })
        
        return results
    
    @staticmethod
    def simulate_internal_reserve(
        base_data: Dict[str, Any],
        target_equity_ratio: float = 30.0,
        years: int = 5
    ) -> Dict[str, Any]:
        """
        内部留保シミュレーション
        目標自己資本比率を達成するために必要な内部留保額を計算
        
        Args:
            base_data: 基準年度のデータ
            target_equity_ratio: 目標自己資本比率（％）
            years: シミュレーション年数
        
        Returns:
            内部留保シミュレーション結果
        """
        current_total_assets = base_data.get('total_assets', 0)
        current_net_assets = base_data.get('net_assets', 0)
        current_equity_ratio = (current_net_assets / current_total_assets * 100) if current_total_assets > 0 else 0
        
        # 目標自己資本額
        target_net_assets = current_total_assets * (target_equity_ratio / 100)
        
        # 必要な内部留保額
        required_internal_reserve = target_net_assets - current_net_assets
        
        # 年間必要内部留保額
        annual_required_reserve = required_internal_reserve / years if years > 0 else 0
        
        # 年度別シミュレーション
        yearly_simulation = []
        accumulated_reserve = 0
        
        for year in range(1, years + 1):
            accumulated_reserve += annual_required_reserve
            projected_net_assets = current_net_assets + accumulated_reserve
            projected_equity_ratio = (projected_net_assets / current_total_assets * 100) if current_total_assets > 0 else 0
            
            yearly_simulation.append({
                'year': year,
                'annual_reserve': annual_required_reserve,
                'accumulated_reserve': accumulated_reserve,
                'net_assets': projected_net_assets,
                'equity_ratio': projected_equity_ratio
            })
        
        return {
            'current_equity_ratio': current_equity_ratio,
            'target_equity_ratio': target_equity_ratio,
            'current_net_assets': current_net_assets,
            'target_net_assets': target_net_assets,
            'required_internal_reserve': required_internal_reserve,
            'annual_required_reserve': annual_required_reserve,
            'years': years,
            'yearly_simulation': yearly_simulation
        }
    
    @staticmethod
    def calculate_borrowing_capacity(
        base_data: Dict[str, Any],
        assumptions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        借入金許容限度額を計算
        
        Args:
            base_data: 基準年度のデータ
            assumptions: 計算前提条件
        
        Returns:
            借入金許容限度額の分析結果
        """
        # 現在の財務データ
        current_total_assets = base_data.get('total_assets', 0)
        current_net_assets = base_data.get('net_assets', 0)
        current_total_debt = base_data.get('total_debt', 0)
        tangible_fixed_assets = base_data.get('tangible_fixed_assets', 0)
        ordinary_income = base_data.get('ordinary_income', 0)
        
        # 前提条件
        target_equity_ratio = assumptions.get('target_equity_ratio', 30.0)  # 目標自己資本比率（％）
        collateral_ratio = assumptions.get('collateral_ratio', 0.70)  # 担保掛目（デフォルト70%）
        debt_service_coverage_ratio = assumptions.get('debt_service_coverage_ratio', 1.5)  # 債務償還年数の逆数
        interest_rate = assumptions.get('interest_rate', 0.02)  # 金利（デフォルト2%）
        
        # 方法1: 自己資本比率から計算
        # 目標自己資本比率を維持できる総資産
        max_total_assets_by_equity = current_net_assets / (target_equity_ratio / 100) if target_equity_ratio > 0 else 0
        # 借入可能額
        borrowing_capacity_by_equity = max_total_assets_by_equity - current_total_assets
        
        # 方法2: 担保余力から計算
        # 担保評価額
        collateral_value = tangible_fixed_assets * collateral_ratio
        # 借入可能額（担保評価額 - 既存借入金）
        borrowing_capacity_by_collateral = collateral_value - current_total_debt
        
        # 方法3: 返済能力から計算
        # 年間返済可能額（経常利益 ÷ 債務償還年数）
        annual_repayment_capacity = ordinary_income * debt_service_coverage_ratio
        # 借入可能額（年間返済可能額を現在価値に換算）
        # 簡易計算: 年間返済可能額 × 10年
        borrowing_capacity_by_repayment = annual_repayment_capacity * 10
        
        # 総合判定（最も保守的な値を採用）
        final_borrowing_capacity = min(
            borrowing_capacity_by_equity,
            borrowing_capacity_by_collateral,
            borrowing_capacity_by_repayment
        )
        
        # 借入後の財務指標
        projected_total_debt = current_total_debt + final_borrowing_capacity
        projected_total_assets = current_total_assets + final_borrowing_capacity
        projected_equity_ratio = (current_net_assets / projected_total_assets * 100) if projected_total_assets > 0 else 0
        projected_debt_ratio = (projected_total_debt / projected_total_assets * 100) if projected_total_assets > 0 else 0
        
        return {
            'current_total_debt': current_total_debt,
            'borrowing_capacity_by_equity': borrowing_capacity_by_equity,
            'borrowing_capacity_by_collateral': borrowing_capacity_by_collateral,
            'borrowing_capacity_by_repayment': borrowing_capacity_by_repayment,
            'final_borrowing_capacity': final_borrowing_capacity,
            'projected_total_debt': projected_total_debt,
            'projected_total_assets': projected_total_assets,
            'projected_equity_ratio': projected_equity_ratio,
            'projected_debt_ratio': projected_debt_ratio,
            'limiting_factor': SimulationService._get_limiting_factor(
                borrowing_capacity_by_equity,
                borrowing_capacity_by_collateral,
                borrowing_capacity_by_repayment
            )
        }
    
    @staticmethod
    def _get_limiting_factor(equity_capacity, collateral_capacity, repayment_capacity) -> str:
        """借入限度額の制約要因を特定"""
        min_capacity = min(equity_capacity, collateral_capacity, repayment_capacity)
        
        if min_capacity == equity_capacity:
            return '自己資本比率'
        elif min_capacity == collateral_capacity:
            return '担保余力'
        else:
            return '返済能力'
    
    @staticmethod
    def simulate_break_even_analysis(
        base_data: Dict[str, Any],
        cost_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        損益分岐点分析
        
        Args:
            base_data: 基準年度のデータ
            cost_structure: 費用構造（固定費・変動費）
        
        Returns:
            損益分岐点分析結果
        """
        sales = base_data.get('sales', 0)
        variable_cost = cost_structure.get('variable_cost', 0)
        fixed_cost = cost_structure.get('fixed_cost', 0)
        
        # 変動費率
        variable_cost_ratio = (variable_cost / sales) if sales > 0 else 0
        
        # 限界利益率
        marginal_profit_ratio = 1 - variable_cost_ratio
        
        # 損益分岐点売上高
        break_even_sales = fixed_cost / marginal_profit_ratio if marginal_profit_ratio > 0 else 0
        
        # 損益分岐点比率
        break_even_ratio = (break_even_sales / sales * 100) if sales > 0 else 0
        
        # 安全余裕率
        safety_margin_ratio = 100 - break_even_ratio
        
        # 経営安全率（安全余裕率 ÷ 売上高）
        management_safety_ratio = ((sales - break_even_sales) / sales * 100) if sales > 0 else 0
        
        return {
            'sales': sales,
            'variable_cost': variable_cost,
            'fixed_cost': fixed_cost,
            'variable_cost_ratio': variable_cost_ratio * 100,
            'marginal_profit_ratio': marginal_profit_ratio * 100,
            'break_even_sales': break_even_sales,
            'break_even_ratio': break_even_ratio,
            'safety_margin_ratio': safety_margin_ratio,
            'management_safety_ratio': management_safety_ratio
        }
    
    @staticmethod
    def simulate_differential_analysis(
        base_scenario: Dict[str, Any],
        alternative_scenario: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        差額原価収益分析
        
        Args:
            base_scenario: 基準シナリオ
            alternative_scenario: 代替シナリオ
        
        Returns:
            差額原価収益分析結果
        """
        # 差額売上高
        differential_sales = alternative_scenario.get('sales', 0) - base_scenario.get('sales', 0)
        
        # 差額原価
        differential_cost = alternative_scenario.get('total_cost', 0) - base_scenario.get('total_cost', 0)
        
        # 差額利益
        differential_profit = differential_sales - differential_cost
        
        # 差額利益率
        differential_profit_ratio = (differential_profit / differential_sales * 100) if differential_sales > 0 else 0
        
        # 投資回収期間（追加投資がある場合）
        additional_investment = alternative_scenario.get('investment', 0) - base_scenario.get('investment', 0)
        payback_period = (additional_investment / differential_profit) if differential_profit > 0 else float('inf')
        
        return {
            'base_scenario': base_scenario,
            'alternative_scenario': alternative_scenario,
            'differential_sales': differential_sales,
            'differential_cost': differential_cost,
            'differential_profit': differential_profit,
            'differential_profit_ratio': differential_profit_ratio,
            'additional_investment': additional_investment,
            'payback_period': payback_period,
            'recommendation': 'alternative' if differential_profit > 0 else 'base'
        }
