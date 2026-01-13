"""
資金繰り計画の月次データをExcelから読み取るヘルパー
⑦初年度資金繰り計画、⑧2年度資金繰り計画、⑨3年度資金繰り計画
"""
from typing import Dict, List, Any
import openpyxl


def read_monthly_cash_flow_plan(wb, sheet_name: str) -> List[Dict[str, Any]]:
    """
    資金繰り計画シートから月次データを読み取る
    
    Args:
        wb: openpyxlのWorkbookオブジェクト
        sheet_name: シート名（例: '⑦初年度資金繰り計画'）
    
    Returns:
        月次データのリスト（12ヶ月分）
    """
    if sheet_name not in wb.sheetnames:
        raise ValueError(f'シート "{sheet_name}" が見つかりません')
    
    ws = wb[sheet_name]
    
    # 月次データを格納するリスト
    monthly_data = []
    
    # 列8〜19が1月〜12月のデータ
    for month in range(1, 13):
        col = 7 + month  # 列8=1月, 列9=2月, ..., 列19=12月
        
        data = {
            'month': month,
            # 月初残高
            'beginning_balance': _get_cell_value(ws, 4, col),
            # （１）手許現預金
            'cash': _get_cell_value(ws, 5, col),
            'ordinary_deposit_1': _get_cell_value(ws, 6, col),
            'ordinary_deposit_2': _get_cell_value(ws, 7, col),
            'ordinary_deposit_3': _get_cell_value(ws, 8, col),
            'cash_and_deposits_total': _get_cell_value(ws, 9, col),
            # （２）運用預金
            'time_deposit': _get_cell_value(ws, 10, col),
            'investment_deposits_total': _get_cell_value(ws, 12, col),
            # 収入
            'cash_sales': _get_cell_value(ws, 13, col),
            'accounts_receivable_collection': _get_cell_value(ws, 14, col),
            'notes_receivable_collection': _get_cell_value(ws, 15, col),
            'notes_discount': _get_cell_value(ws, 16, col),
            'other_cash_income': _get_cell_value(ws, 18, col),
            'income_total': _get_cell_value(ws, 19, col),
            # 仕入
            'cash_purchases': _get_cell_value(ws, 20, col),
            'accounts_payable_payment': _get_cell_value(ws, 21, col),
            'notes_payable_payment': _get_cell_value(ws, 22, col),
            'other_cash_expenses': _get_cell_value(ws, 25, col),
            'purchases_total': _get_cell_value(ws, 26, col),
            # 人件費
            'executive_compensation': _get_cell_value(ws, 27, col),
            'executive_statutory_welfare': _get_cell_value(ws, 28, col),
            'executive_retirement': _get_cell_value(ws, 29, col),
            'salaries': _get_cell_value(ws, 30, col),
            'temporary_wages': _get_cell_value(ws, 31, col),
            'bonuses': _get_cell_value(ws, 32, col),
            'employee_statutory_welfare': _get_cell_value(ws, 33, col),
            'employee_retirement': _get_cell_value(ws, 34, col),
            'welfare_expenses': _get_cell_value(ws, 35, col),
            'labor_cost_total': _get_cell_value(ws, 36, col),
            # その他経費
            'office_supplies': _get_cell_value(ws, 37, col),
            'consumables': _get_cell_value(ws, 38, col),
            'travel_expenses': _get_cell_value(ws, 39, col),
            'commission_fees': _get_cell_value(ws, 40, col),
            'entertainment_expenses': _get_cell_value(ws, 41, col),
            'insurance_premiums': _get_cell_value(ws, 42, col),
            'communication_expenses': _get_cell_value(ws, 43, col),
            'membership_fees': _get_cell_value(ws, 44, col),
            'vehicle_expenses': _get_cell_value(ws, 45, col),
            'books_and_publications': _get_cell_value(ws, 46, col),
            'advertising_expenses': _get_cell_value(ws, 47, col),
            'utilities': _get_cell_value(ws, 48, col),
            'rent': _get_cell_value(ws, 49, col),
            'repairs': _get_cell_value(ws, 50, col),
            'lease_expenses': _get_cell_value(ws, 51, col),
            'miscellaneous_expenses': _get_cell_value(ws, 54, col),
            'other_expenses_total': _get_cell_value(ws, 55, col),
            # 経費以外支出
            'marketable_securities': _get_cell_value(ws, 56, col),
            'tangible_fixed_assets': _get_cell_value(ws, 57, col),
            'intangible_fixed_assets': _get_cell_value(ws, 58, col),
            'investments_and_other_assets': _get_cell_value(ws, 59, col),
            'deferred_assets': _get_cell_value(ws, 60, col),
            'non_operating_expenses_total': _get_cell_value(ws, 62, col),
            # 支出計
            'expenses_total': _get_cell_value(ws, 63, col),
            # 差引計（収入－支出）
            'net_cash_flow': _get_cell_value(ws, 64, col),
            # ①月末残高
            'ending_balance': _get_cell_value(ws, 65, col),
            # ②月末残高－主要運転資金計画
            'ending_balance_minus_working_capital': _get_cell_value(ws, 66, col),
            # （１）手許現預金（月末）
            'ending_cash': _get_cell_value(ws, 67, col),
            'ending_ordinary_deposit_1': _get_cell_value(ws, 68, col),
            'ending_ordinary_deposit_2': _get_cell_value(ws, 69, col),
            'ending_ordinary_deposit_3': _get_cell_value(ws, 70, col),
            'ending_cash_and_deposits_total': _get_cell_value(ws, 71, col),
            # （２）運用預金（月末）
            'ending_time_deposit': _get_cell_value(ws, 72, col),
            'ending_investment_deposits_total': _get_cell_value(ws, 74, col),
        }
        
        monthly_data.append(data)
    
    return monthly_data


def _get_cell_value(ws, row: int, col: int) -> float:
    """
    セルの値を取得（数値として）
    
    Args:
        ws: ワークシート
        row: 行番号（1始まり）
        col: 列番号（1始まり）
    
    Returns:
        セルの値（数値）、Noneの場合は0.0
    """
    value = ws.cell(row, col).value
    if value is None:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def import_monthly_cash_flow_plans(
    wb,
    company_id: int,
    fiscal_year_ids: List[int],
    db
) -> Dict[str, Any]:
    """
    3年度分の資金繰り計画をExcelから読み取り、データベースに保存
    
    Args:
        wb: openpyxlのWorkbookオブジェクト
        company_id: 企業ID
        fiscal_year_ids: 会計年度IDのリスト（3つ）
        db: データベースセッション
    
    Returns:
        インポート結果
    """
    from ..models_decision import MonthlyCashFlowPlan
    
    if len(fiscal_year_ids) != 3:
        raise ValueError('fiscal_year_idsは3つ必要です')
    
    sheet_names = [
        '⑦初年度資金繰り計画',
        '⑧2年度資金繰り計画',
        '⑨3年度資金繰り計画'
    ]
    
    results = []
    
    for i, (fiscal_year_id, sheet_name) in enumerate(zip(fiscal_year_ids, sheet_names)):
        try:
            # Excelから月次データを読み取る
            monthly_data = read_monthly_cash_flow_plan(wb, sheet_name)
            
            # 既存データを削除
            db.query(MonthlyCashFlowPlan).filter(
                MonthlyCashFlowPlan.company_id == company_id,
                MonthlyCashFlowPlan.fiscal_year_id == fiscal_year_id
            ).delete()
            
            # 新しいデータを挿入
            for data in monthly_data:
                record = MonthlyCashFlowPlan(
                    company_id=company_id,
                    fiscal_year_id=fiscal_year_id,
                    **data
                )
                db.add(record)
            
            db.commit()
            
            results.append({
                'fiscal_year_id': fiscal_year_id,
                'sheet_name': sheet_name,
                'status': 'success',
                'records_imported': len(monthly_data)
            })
            
        except Exception as e:
            db.rollback()
            results.append({
                'fiscal_year_id': fiscal_year_id,
                'sheet_name': sheet_name,
                'status': 'error',
                'error': str(e)
            })
    
    return {
        'company_id': company_id,
        'results': results
    }


def get_monthly_cash_flow_plan(
    company_id: int,
    fiscal_year_id: int,
    db
) -> List[Dict[str, Any]]:
    """
    資金繰り計画の月次データを取得
    
    Args:
        company_id: 企業ID
        fiscal_year_id: 会計年度ID
        db: データベースセッション
    
    Returns:
        月次データのリスト（12ヶ月分）
    """
    from ..models_decision import MonthlyCashFlowPlan
    
    records = db.query(MonthlyCashFlowPlan).filter(
        MonthlyCashFlowPlan.company_id == company_id,
        MonthlyCashFlowPlan.fiscal_year_id == fiscal_year_id
    ).order_by(MonthlyCashFlowPlan.month).all()
    
    return [
        {
            'month': record.month,
            'beginning_balance': float(record.beginning_balance or 0),
            'cash': float(record.cash or 0),
            'ordinary_deposit_1': float(record.ordinary_deposit_1 or 0),
            'ordinary_deposit_2': float(record.ordinary_deposit_2 or 0),
            'ordinary_deposit_3': float(record.ordinary_deposit_3 or 0),
            'cash_and_deposits_total': float(record.cash_and_deposits_total or 0),
            'time_deposit': float(record.time_deposit or 0),
            'investment_deposits_total': float(record.investment_deposits_total or 0),
            'cash_sales': float(record.cash_sales or 0),
            'accounts_receivable_collection': float(record.accounts_receivable_collection or 0),
            'notes_receivable_collection': float(record.notes_receivable_collection or 0),
            'notes_discount': float(record.notes_discount or 0),
            'other_cash_income': float(record.other_cash_income or 0),
            'income_total': float(record.income_total or 0),
            'cash_purchases': float(record.cash_purchases or 0),
            'accounts_payable_payment': float(record.accounts_payable_payment or 0),
            'notes_payable_payment': float(record.notes_payable_payment or 0),
            'other_cash_expenses': float(record.other_cash_expenses or 0),
            'purchases_total': float(record.purchases_total or 0),
            'executive_compensation': float(record.executive_compensation or 0),
            'executive_statutory_welfare': float(record.executive_statutory_welfare or 0),
            'executive_retirement': float(record.executive_retirement or 0),
            'salaries': float(record.salaries or 0),
            'temporary_wages': float(record.temporary_wages or 0),
            'bonuses': float(record.bonuses or 0),
            'employee_statutory_welfare': float(record.employee_statutory_welfare or 0),
            'employee_retirement': float(record.employee_retirement or 0),
            'welfare_expenses': float(record.welfare_expenses or 0),
            'labor_cost_total': float(record.labor_cost_total or 0),
            'office_supplies': float(record.office_supplies or 0),
            'consumables': float(record.consumables or 0),
            'travel_expenses': float(record.travel_expenses or 0),
            'commission_fees': float(record.commission_fees or 0),
            'entertainment_expenses': float(record.entertainment_expenses or 0),
            'insurance_premiums': float(record.insurance_premiums or 0),
            'communication_expenses': float(record.communication_expenses or 0),
            'membership_fees': float(record.membership_fees or 0),
            'vehicle_expenses': float(record.vehicle_expenses or 0),
            'books_and_publications': float(record.books_and_publications or 0),
            'advertising_expenses': float(record.advertising_expenses or 0),
            'utilities': float(record.utilities or 0),
            'rent': float(record.rent or 0),
            'repairs': float(record.repairs or 0),
            'lease_expenses': float(record.lease_expenses or 0),
            'miscellaneous_expenses': float(record.miscellaneous_expenses or 0),
            'other_expenses_total': float(record.other_expenses_total or 0),
            'marketable_securities': float(record.marketable_securities or 0),
            'tangible_fixed_assets': float(record.tangible_fixed_assets or 0),
            'intangible_fixed_assets': float(record.intangible_fixed_assets or 0),
            'investments_and_other_assets': float(record.investments_and_other_assets or 0),
            'deferred_assets': float(record.deferred_assets or 0),
            'non_operating_expenses_total': float(record.non_operating_expenses_total or 0),
            'expenses_total': float(record.expenses_total or 0),
            'net_cash_flow': float(record.net_cash_flow or 0),
            'ending_balance': float(record.ending_balance or 0),
            'ending_balance_minus_working_capital': float(record.ending_balance_minus_working_capital or 0),
            'ending_cash': float(record.ending_cash or 0),
            'ending_ordinary_deposit_1': float(record.ending_ordinary_deposit_1 or 0),
            'ending_ordinary_deposit_2': float(record.ending_ordinary_deposit_2 or 0),
            'ending_ordinary_deposit_3': float(record.ending_ordinary_deposit_3 or 0),
            'ending_cash_and_deposits_total': float(record.ending_cash_and_deposits_total or 0),
            'ending_time_deposit': float(record.ending_time_deposit or 0),
            'ending_investment_deposits_total': float(record.ending_investment_deposits_total or 0),
        }
        for record in records
    ]
