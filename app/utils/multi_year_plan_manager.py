"""
多年度計画統合管理モジュール

労務費計画、設備投資計画、運転資金計画、資金調達返済計画を統合し、
3期分の総合経営計画を管理します。
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class MultiYearPlanManager:
    """多年度計画統合管理クラス"""
    
    @staticmethod
    def create_integrated_plan(
        company_id: int,
        base_year: int,
        labor_cost_plans: List[Dict[str, Any]],
        capital_investment_plans: List[Dict[str, Any]],
        working_capital_plans: List[Dict[str, Any]],
        financing_plans: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        統合計画を作成
        
        Args:
            company_id: 企業ID
            base_year: 基準年度
            labor_cost_plans: 労務費計画のリスト（3年分）
            capital_investment_plans: 設備投資計画のリスト（3年分）
            working_capital_plans: 運転資金計画のリスト（3年分）
            financing_plans: 資金調達返済計画のリスト（3年分）
        
        Returns:
            dict: 統合計画データ
        """
        integrated_plan = {
            'company_id': company_id,
            'base_year': base_year,
            'years': []
        }
        
        # 3年分の計画を統合
        for year_offset in range(3):
            year = base_year + year_offset
            
            # 各計画から該当年度のデータを取得
            labor_plan = labor_cost_plans[year_offset] if year_offset < len(labor_cost_plans) else {}
            capital_plan = capital_investment_plans[year_offset] if year_offset < len(capital_investment_plans) else {}
            working_plan = working_capital_plans[year_offset] if year_offset < len(working_capital_plans) else {}
            financing_plan = financing_plans[year_offset] if year_offset < len(financing_plans) else {}
            
            year_plan = {
                'year': year,
                'year_offset': year_offset,
                'labor_cost': {
                    'employee_count': labor_plan.get('employee_count', 0),
                    'total_labor_cost': labor_plan.get('total_labor_cost', 0),
                    'average_salary': labor_plan.get('average_salary', 0),
                    'social_insurance': labor_plan.get('social_insurance', 0),
                    'welfare_expenses': labor_plan.get('welfare_expenses', 0)
                },
                'capital_investment': {
                    'total_investment': capital_plan.get('total_investment', 0),
                    'depreciation': capital_plan.get('depreciation', 0),
                    'useful_life': capital_plan.get('useful_life', 0),
                    'investment_items': capital_plan.get('investment_items', [])
                },
                'working_capital': {
                    'accounts_receivable': working_plan.get('accounts_receivable', 0),
                    'inventory': working_plan.get('inventory', 0),
                    'accounts_payable': working_plan.get('accounts_payable', 0),
                    'net_working_capital': working_plan.get('net_working_capital', 0),
                    'cash_conversion_cycle': working_plan.get('cash_conversion_cycle', 0)
                },
                'financing': {
                    'new_borrowing': financing_plan.get('new_borrowing', 0),
                    'principal_repayment': financing_plan.get('principal_repayment', 0),
                    'interest_payment': financing_plan.get('interest_payment', 0),
                    'total_debt_balance': financing_plan.get('total_debt_balance', 0),
                    'debt_service_coverage_ratio': financing_plan.get('debt_service_coverage_ratio', 0)
                }
            }
            
            integrated_plan['years'].append(year_plan)
        
        return integrated_plan
    
    @staticmethod
    def calculate_plan_summary(integrated_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        計画のサマリーを計算
        
        Args:
            integrated_plan: 統合計画データ
        
        Returns:
            dict: サマリーデータ
        """
        summary = {
            'total_labor_cost_3years': 0,
            'total_capital_investment_3years': 0,
            'total_depreciation_3years': 0,
            'total_interest_payment_3years': 0,
            'total_principal_repayment_3years': 0,
            'average_working_capital': 0,
            'final_debt_balance': 0
        }
        
        for year_plan in integrated_plan['years']:
            summary['total_labor_cost_3years'] += year_plan['labor_cost']['total_labor_cost']
            summary['total_capital_investment_3years'] += year_plan['capital_investment']['total_investment']
            summary['total_depreciation_3years'] += year_plan['capital_investment']['depreciation']
            summary['total_interest_payment_3years'] += year_plan['financing']['interest_payment']
            summary['total_principal_repayment_3years'] += year_plan['financing']['principal_repayment']
            summary['average_working_capital'] += year_plan['working_capital']['net_working_capital']
        
        # 平均運転資金を計算
        if len(integrated_plan['years']) > 0:
            summary['average_working_capital'] /= len(integrated_plan['years'])
        
        # 最終年度の借入残高を取得
        if len(integrated_plan['years']) > 0:
            summary['final_debt_balance'] = integrated_plan['years'][-1]['financing']['total_debt_balance']
        
        return summary
    
    @staticmethod
    def validate_plan(integrated_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        計画の妥当性を検証
        
        Args:
            integrated_plan: 統合計画データ
        
        Returns:
            dict: 検証結果
        """
        warnings = []
        errors = []
        
        for year_plan in integrated_plan['years']:
            year = year_plan['year']
            
            # 労務費の妥当性チェック
            if year_plan['labor_cost']['total_labor_cost'] <= 0:
                warnings.append(f"{year}年度: 労務費が0以下です")
            
            # 設備投資の妥当性チェック
            if year_plan['capital_investment']['total_investment'] < 0:
                errors.append(f"{year}年度: 設備投資額が負の値です")
            
            # 運転資金の妥当性チェック
            if year_plan['working_capital']['net_working_capital'] < 0:
                warnings.append(f"{year}年度: 正味運転資本が負の値です（資金繰りに注意）")
            
            # 資金調達の妥当性チェック
            if year_plan['financing']['debt_service_coverage_ratio'] < 1.0 and year_plan['financing']['debt_service_coverage_ratio'] > 0:
                warnings.append(f"{year}年度: 債務返済カバー率が1.0未満です（返済能力に懸念）")
            
            if year_plan['financing']['total_debt_balance'] < 0:
                errors.append(f"{year}年度: 借入残高が負の値です")
        
        return {
            'is_valid': len(errors) == 0,
            'warnings': warnings,
            'errors': errors
        }
    
    @staticmethod
    def format_plan_for_ui(integrated_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        計画データをUI表示用に整形
        
        Args:
            integrated_plan: 統合計画データ
        
        Returns:
            dict: UI表示用の整形済みデータ
        """
        formatted_years = []
        
        for year_plan in integrated_plan['years']:
            formatted_years.append({
                'year': year_plan['year'],
                'year_label': f"{year_plan['year']}年度",
                'labor_cost': {
                    'employee_count': year_plan['labor_cost']['employee_count'],
                    'total_labor_cost': round(year_plan['labor_cost']['total_labor_cost'], 2),
                    'total_labor_cost_formatted': f"{year_plan['labor_cost']['total_labor_cost']:,.0f}円",
                    'average_salary': round(year_plan['labor_cost']['average_salary'], 2),
                    'average_salary_formatted': f"{year_plan['labor_cost']['average_salary']:,.0f}円"
                },
                'capital_investment': {
                    'total_investment': round(year_plan['capital_investment']['total_investment'], 2),
                    'total_investment_formatted': f"{year_plan['capital_investment']['total_investment']:,.0f}円",
                    'depreciation': round(year_plan['capital_investment']['depreciation'], 2),
                    'depreciation_formatted': f"{year_plan['capital_investment']['depreciation']:,.0f}円"
                },
                'working_capital': {
                    'net_working_capital': round(year_plan['working_capital']['net_working_capital'], 2),
                    'net_working_capital_formatted': f"{year_plan['working_capital']['net_working_capital']:,.0f}円",
                    'cash_conversion_cycle': round(year_plan['working_capital']['cash_conversion_cycle'], 2),
                    'cash_conversion_cycle_formatted': f"{year_plan['working_capital']['cash_conversion_cycle']:.1f}日"
                },
                'financing': {
                    'new_borrowing': round(year_plan['financing']['new_borrowing'], 2),
                    'new_borrowing_formatted': f"{year_plan['financing']['new_borrowing']:,.0f}円",
                    'principal_repayment': round(year_plan['financing']['principal_repayment'], 2),
                    'principal_repayment_formatted': f"{year_plan['financing']['principal_repayment']:,.0f}円",
                    'interest_payment': round(year_plan['financing']['interest_payment'], 2),
                    'interest_payment_formatted': f"{year_plan['financing']['interest_payment']:,.0f}円",
                    'total_debt_balance': round(year_plan['financing']['total_debt_balance'], 2),
                    'total_debt_balance_formatted': f"{year_plan['financing']['total_debt_balance']:,.0f}円"
                }
            })
        
        # サマリーを計算
        summary = MultiYearPlanManager.calculate_plan_summary(integrated_plan)
        
        formatted_summary = {
            'total_labor_cost_3years': round(summary['total_labor_cost_3years'], 2),
            'total_labor_cost_3years_formatted': f"{summary['total_labor_cost_3years']:,.0f}円",
            'total_capital_investment_3years': round(summary['total_capital_investment_3years'], 2),
            'total_capital_investment_3years_formatted': f"{summary['total_capital_investment_3years']:,.0f}円",
            'total_depreciation_3years': round(summary['total_depreciation_3years'], 2),
            'total_depreciation_3years_formatted': f"{summary['total_depreciation_3years']:,.0f}円",
            'total_interest_payment_3years': round(summary['total_interest_payment_3years'], 2),
            'total_interest_payment_3years_formatted': f"{summary['total_interest_payment_3years']:,.0f}円",
            'total_principal_repayment_3years': round(summary['total_principal_repayment_3years'], 2),
            'total_principal_repayment_3years_formatted': f"{summary['total_principal_repayment_3years']:,.0f}円",
            'average_working_capital': round(summary['average_working_capital'], 2),
            'average_working_capital_formatted': f"{summary['average_working_capital']:,.0f}円",
            'final_debt_balance': round(summary['final_debt_balance'], 2),
            'final_debt_balance_formatted': f"{summary['final_debt_balance']:,.0f}円"
        }
        
        return {
            'company_id': integrated_plan['company_id'],
            'base_year': integrated_plan['base_year'],
            'years': formatted_years,
            'summary': formatted_summary
        }
