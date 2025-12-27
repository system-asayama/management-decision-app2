"""
財務諸表組換えサービス
標準的な財務諸表を経営分析用の組換え財務諸表に変換する

Excelの「組換え手順」を参考に実装
"""
from typing import Dict, Any


class RestructuringService:
    """財務諸表組換えサービス"""
    
    @staticmethod
    def restructure_pl(pl_data: Dict[str, Any], additional_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        損益計算書を組換える
        
        Args:
            pl_data: 標準的なP/Lデータ
            additional_data: 追加データ（製造原価報告書のデータなど）
        
        Returns:
            組換え後のP/Lデータ
        """
        if additional_data is None:
            additional_data = {}
        
        # 基本項目
        sales = pl_data.get('sales', 0)
        cost_of_sales = pl_data.get('cost_of_sales', 0)
        gross_profit = pl_data.get('gross_profit', 0)
        
        # 売上総利益の計算（念のため再計算）
        if gross_profit == 0:
            gross_profit = sales - cost_of_sales
        
        # 外部経費調整（製造原価報告書から）
        labor_cost_manufacturing = additional_data.get('labor_cost_manufacturing', 0)
        depreciation_manufacturing = additional_data.get('depreciation_manufacturing', 0)
        repair_cost_manufacturing = additional_data.get('repair_cost_manufacturing', 0)
        external_expense_adjustment = labor_cost_manufacturing + depreciation_manufacturing + repair_cost_manufacturing
        
        # 粗付加価値 = 売上総利益 + 外部経費調整
        gross_added_value = gross_profit + external_expense_adjustment
        
        # 人件費（製造原価報告書 + P/L）
        labor_cost_pl = additional_data.get('labor_cost_pl', 0)
        personnel_expenses = pl_data.get('personnel_expenses', 0)
        total_labor_cost = labor_cost_manufacturing + labor_cost_pl + personnel_expenses
        
        # 役員報酬
        executive_compensation = pl_data.get('executive_compensation', 0)
        executive_welfare = additional_data.get('executive_welfare', 0)
        total_executive_compensation = executive_compensation + executive_welfare
        
        # 資本再生費（減価償却費 + 修繕費）
        depreciation_pl = pl_data.get('depreciation', 0)
        repair_cost_pl = additional_data.get('repair_cost_pl', 0)
        capital_regeneration_cost = depreciation_manufacturing + repair_cost_manufacturing + depreciation_pl + repair_cost_pl
        
        # 研究開発費
        research_development_expenses = pl_data.get('research_development_expenses', 0)
        
        # 一般経費（固定費と変動費に区分）
        # 変動費: 販売手数料、荷造発送費、運送費、見本費、保管費等（売上に比例）
        variable_expenses = additional_data.get('variable_expenses', 0)
        # 固定費: 一般経費 - 変動費
        operating_expenses = pl_data.get('operating_expenses', 0)
        fixed_expenses = operating_expenses - variable_expenses
        
        # 営業利益
        operating_income = pl_data.get('operating_income', 0)
        
        # 金融損益 = 受取利息 - 支払利息
        interest_income = pl_data.get('interest_income', 0)
        interest_expense = pl_data.get('interest_expense', 0)
        financial_profit_loss = interest_income - interest_expense
        
        # 営業外収益・費用
        non_operating_income = pl_data.get('non_operating_income', 0)
        non_operating_expenses = pl_data.get('non_operating_expenses', 0)
        
        # 経常利益
        ordinary_income = pl_data.get('ordinary_income', 0)
        if ordinary_income == 0:
            ordinary_income = operating_income + non_operating_income - non_operating_expenses
        
        # 特別損益
        extraordinary_income = pl_data.get('extraordinary_income', 0)
        extraordinary_loss = pl_data.get('extraordinary_loss', 0)
        
        # 税引前当期純利益
        income_before_tax = pl_data.get('income_before_tax', 0)
        if income_before_tax == 0:
            income_before_tax = ordinary_income + extraordinary_income - extraordinary_loss
        
        # 法人税等
        income_taxes = pl_data.get('income_tax', 0)
        
        # 当期純利益
        net_income = pl_data.get('net_income', 0)
        if net_income == 0:
            net_income = income_before_tax - income_taxes
        
        # 販売費及び一般管理費
        selling_general_admin_expenses = pl_data.get('operating_expenses', 0)
        
        return {
            'sales': sales,
            'cost_of_sales': cost_of_sales,
            'gross_profit': gross_profit,
            'gross_added_value': gross_added_value,
            'external_expense_adjustment': external_expense_adjustment,
            'total_labor_cost': total_labor_cost,
            'executive_compensation': total_executive_compensation,
            'capital_regeneration_cost': capital_regeneration_cost,
            'research_development_expenses': research_development_expenses,
            'variable_expenses': variable_expenses,
            'fixed_expenses': fixed_expenses,
            'selling_general_admin_expenses': selling_general_admin_expenses,
            'operating_income': operating_income,
            'financial_profit_loss': financial_profit_loss,
            'non_operating_income': non_operating_income,
            'non_operating_expenses': non_operating_expenses,
            'ordinary_income': ordinary_income,
            'extraordinary_income': extraordinary_income,
            'extraordinary_loss': extraordinary_loss,
            'income_before_tax': income_before_tax,
            'income_taxes': income_taxes,
            'net_income': net_income
        }
    
    @staticmethod
    def restructure_bs(bs_data: Dict[str, Any], additional_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        貸借対照表を組換える
        
        Args:
            bs_data: 標準的なB/Sデータ
            additional_data: 追加データ
        
        Returns:
            組換え後のB/Sデータ
        """
        if additional_data is None:
            additional_data = {}
        
        # 流動資産の内訳
        cash_and_deposits = additional_data.get('cash_and_deposits', 0)
        time_deposits = additional_data.get('time_deposits', 0)
        
        # 手許現預金 = 現金 + 小口現金 + 受取小切手 + 利息のつかない預金
        cash_on_hand = cash_and_deposits - time_deposits
        
        # 運用預金 = 手許現預金以外の預金（定期預金、定期積金、外貨預金）
        investment_deposits = time_deposits
        
        # 売掛債権 = 売掛金 + 受取手形 + 未収金
        accounts_receivable = additional_data.get('accounts_receivable', 0)
        notes_receivable = additional_data.get('notes_receivable', 0)
        other_receivables = additional_data.get('other_receivables', 0)
        trade_receivables = accounts_receivable + notes_receivable + other_receivables
        
        # 棚卸資産 = 製品 + 仕掛品 + 材料 + 貯蔵品
        merchandise_inventory = additional_data.get('merchandise_inventory', 0)
        work_in_process = additional_data.get('work_in_process', 0)
        raw_materials = additional_data.get('raw_materials', 0)
        supplies = additional_data.get('supplies', 0)
        inventory_assets = merchandise_inventory + work_in_process + raw_materials + supplies
        
        # 貸倒引当金（流動資産から控除）
        allowance_for_doubtful_accounts = additional_data.get('allowance_for_doubtful_accounts', 0)
        
        # 流動資産合計
        current_assets = bs_data.get('current_assets', 0)
        
        # 有形固定資産
        tangible_fixed_assets = additional_data.get('tangible_fixed_assets', 0)
        if tangible_fixed_assets == 0:
            tangible_fixed_assets = bs_data.get('fixed_assets', 0)
        
        # 無形固定資産
        intangible_fixed_assets = additional_data.get('intangible_fixed_assets', 0)
        
        # 投資その他の資産
        investments_and_other_assets = additional_data.get('investments_and_other_assets', 0)
        
        # 固定資産合計
        fixed_assets = tangible_fixed_assets + intangible_fixed_assets + investments_and_other_assets
        
        # 資産合計
        total_assets = current_assets + fixed_assets
        
        # 買掛債務 = 買掛金 + 支払手形 + 未払金
        accounts_payable = additional_data.get('accounts_payable', 0)
        notes_payable = additional_data.get('notes_payable', 0)
        other_payables = additional_data.get('other_payables', 0)
        trade_payables = accounts_payable + notes_payable + other_payables
        
        # 短期借入金（1年以内返済の長期借入金を含む）
        short_term_borrowings = additional_data.get('short_term_borrowings', 0)
        current_portion_of_long_term_debt = additional_data.get('current_portion_of_long_term_debt', 0)
        total_short_term_debt = short_term_borrowings + current_portion_of_long_term_debt
        
        # その他流動負債
        other_current_liabilities = additional_data.get('other_current_liabilities', 0)
        
        # 流動負債合計
        current_liabilities = bs_data.get('current_liabilities', 0)
        
        # 長期借入金（役員借入金は別表示）
        long_term_borrowings = additional_data.get('long_term_borrowings', 0)
        executive_borrowings = additional_data.get('executive_borrowings', 0)
        long_term_debt_excluding_executive = long_term_borrowings - executive_borrowings
        
        # その他固定負債
        other_fixed_liabilities = additional_data.get('other_fixed_liabilities', 0)
        
        # 固定負債合計
        fixed_liabilities = bs_data.get('fixed_liabilities', 0)
        
        # 負債合計
        total_liabilities = current_liabilities + fixed_liabilities
        
        # 純資産
        capital = bs_data.get('capital', 0)
        retained_earnings = bs_data.get('retained_earnings', 0)
        net_assets = capital + retained_earnings
        
        # 負債純資産合計
        total_liabilities_and_net_assets = total_liabilities + net_assets
        
        return {
            'cash_on_hand': cash_on_hand,
            'investment_deposits': investment_deposits,
            'trade_receivables': trade_receivables,
            'inventory_assets': inventory_assets,
            'allowance_for_doubtful_accounts': allowance_for_doubtful_accounts,
            'current_assets': current_assets,
            'tangible_fixed_assets': tangible_fixed_assets,
            'intangible_fixed_assets': intangible_fixed_assets,
            'investments_and_other_assets': investments_and_other_assets,
            'fixed_assets': fixed_assets,
            'total_assets': total_assets,
            'trade_payables': trade_payables,
            'total_short_term_debt': total_short_term_debt,
            'other_current_liabilities': other_current_liabilities,
            'current_liabilities': current_liabilities,
            'long_term_debt_excluding_executive': long_term_debt_excluding_executive,
            'executive_borrowings': executive_borrowings,
            'other_fixed_liabilities': other_fixed_liabilities,
            'fixed_liabilities': fixed_liabilities,
            'total_liabilities': total_liabilities,
            'capital': capital,
            'retained_earnings': retained_earnings,
            'net_assets': net_assets,
            'total_liabilities_and_net_assets': total_liabilities_and_net_assets
        }
    
    @staticmethod
    def calculate_added_value_components(restructured_pl: Dict[str, Any]) -> Dict[str, Any]:
        """
        付加価値の構成要素を計算
        
        Args:
            restructured_pl: 組換え後のP/Lデータ
        
        Returns:
            付加価値の構成要素
        """
        gross_added_value = restructured_pl.get('gross_added_value', 0)
        total_labor_cost = restructured_pl.get('total_labor_cost', 0)
        executive_compensation = restructured_pl.get('executive_compensation', 0)
        capital_regeneration_cost = restructured_pl.get('capital_regeneration_cost', 0)
        research_development_expenses = restructured_pl.get('research_development_expenses', 0)
        financial_profit_loss = restructured_pl.get('financial_profit_loss', 0)
        
        # 純付加価値 = 粗付加価値 - 減価償却費
        net_added_value = gross_added_value - capital_regeneration_cost
        
        # 付加価値配分
        # 労働分配率 = 人件費 / 粗付加価値
        labor_distribution_ratio = (total_labor_cost / gross_added_value * 100) if gross_added_value > 0 else 0
        
        # 役員報酬配分率 = 役員報酬 / 粗付加価値
        executive_distribution_ratio = (executive_compensation / gross_added_value * 100) if gross_added_value > 0 else 0
        
        # 資本再生費配分率 = 資本再生費 / 粗付加価値
        capital_distribution_ratio = (capital_regeneration_cost / gross_added_value * 100) if gross_added_value > 0 else 0
        
        return {
            'gross_added_value': gross_added_value,
            'net_added_value': net_added_value,
            'total_labor_cost': total_labor_cost,
            'executive_compensation': executive_compensation,
            'capital_regeneration_cost': capital_regeneration_cost,
            'research_development_expenses': research_development_expenses,
            'financial_profit_loss': financial_profit_loss,
            'labor_distribution_ratio': labor_distribution_ratio,
            'executive_distribution_ratio': executive_distribution_ratio,
            'capital_distribution_ratio': capital_distribution_ratio
        }
