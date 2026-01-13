"""
Excel読み取りヘルパー関数
運転資金・回転期間・資金繰り前提をExcelから読み取る
"""


def read_working_capital_assumptions(wb, fiscal_year_index):
    """
    ⑥主要運転資金計画シートから運転資金前提を読み取る
    
    Args:
        wb: openpyxlワークブック
        fiscal_year_index: 会計年度インデックス（0=初年度, 1=2年度, 2=3年度）
    
    Returns:
        dict: 運転資金前提データ
    """
    try:
        ws = wb['⑥主要運転資金計画']
    except KeyError:
        raise ValueError("シート '⑥主要運転資金計画' が見つかりません")
    
    # 列インデックス（初年度=9, 2年度=10, 3年度=11）
    col = 9 + fiscal_year_index
    
    def get_cell_value(row, column):
        """セルの値を取得（Noneの場合は0.0を返す）"""
        value = ws.cell(row, column).value
        if value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    return {
        'cash_turnover_period': get_cell_value(6, col),
        'receivables_turnover_period': get_cell_value(11, col),
        'inventory_turnover_period': get_cell_value(16, col),
        'payables_turnover_period': get_cell_value(22, col),
        'cash_increase': get_cell_value(8, col),
        'receivables_increase': get_cell_value(13, col),
        'inventory_increase': get_cell_value(18, col),
        'payables_increase': get_cell_value(24, col)
    }


def read_debt_repayment_assumptions(wb, fiscal_year_index):
    """
    ⑩資金調達返済計画（1）シートから返済スケジュール前提を読み取る
    
    Args:
        wb: openpyxlワークブック
        fiscal_year_index: 会計年度インデックス（0=初年度, 1=2年度, 2=3年度）
    
    Returns:
        dict: 返済スケジュール前提データ
    """
    # シート名（初年度=⑩, 2年度=⑪, 3年度=⑫）
    sheet_names = ['⑩資金調達返済計画（1）', '⑪資金調達返済計画（2）', '⑫資金調達返済計画（3）']
    
    try:
        ws = wb[sheet_names[fiscal_year_index]]
    except KeyError:
        raise ValueError(f"シート '{sheet_names[fiscal_year_index]}' が見つかりません")
    
    # 列11（K列）の固定位置
    col = 11
    
    def get_cell_value(row, column):
        """セルの値を取得（Noneの場合は0.0を返す）"""
        value = ws.cell(row, column).value
        if value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    return {
        'beginning_balance': get_cell_value(14, col),
        'borrowing_amount': get_cell_value(15, col),
        'principal_repayment': get_cell_value(16, col),
        'ending_balance': get_cell_value(17, col),
        'interest_payment': get_cell_value(18, col),
        'average_interest_rate': get_cell_value(39, col)
    }


def import_working_capital_and_debt_assumptions(wb, company_id, fiscal_year_ids, db, validate=True):
    """
    運転資金前提と返済スケジュール前提をExcelから一括インポート
    
    Args:
        wb: openpyxlワークブック
        company_id: 企業ID
        fiscal_year_ids: 会計年度IDのリスト（[初年度ID, 2年度ID, 3年度ID]）
        db: データベースセッション
    
    Returns:
        dict: インポート結果
    """
    from ..models_decision import WorkingCapitalAssumption, DebtRepaymentAssumption
    from .data_validation import validate_all_assumptions
    
    results = {
        'working_capital_assumptions': [],
        'debt_repayment_assumptions': [],
        'validation': {'valid': True, 'errors': [], 'warnings': []}
    }
    
    # 3年度分のデータを読み取る
    for i, fiscal_year_id in enumerate(fiscal_year_ids):
        # 運転資金前提を読み取る
        try:
            wc_data = read_working_capital_assumptions(wb, i)
            
            # 既存データを削除
            db.query(WorkingCapitalAssumption).filter(
                WorkingCapitalAssumption.company_id == company_id,
                WorkingCapitalAssumption.fiscal_year_id == fiscal_year_id
            ).delete()
            
            # 新規データを作成
            wc_assumption = WorkingCapitalAssumption(
                company_id=company_id,
                fiscal_year_id=fiscal_year_id,
                **wc_data
            )
            db.add(wc_assumption)
            results['working_capital_assumptions'].append(wc_data)
        except Exception as e:
            print(f"運転資金前提の読み取りエラー（年度{i+1}）: {e}")
        
        # 返済スケジュール前提を読み取る
        try:
            debt_data = read_debt_repayment_assumptions(wb, i)
            
            # 既存データを削除
            db.query(DebtRepaymentAssumption).filter(
                DebtRepaymentAssumption.company_id == company_id,
                DebtRepaymentAssumption.fiscal_year_id == fiscal_year_id
            ).delete()
            
            # 新規データを作成
            debt_assumption = DebtRepaymentAssumption(
                company_id=company_id,
                fiscal_year_id=fiscal_year_id,
                **debt_data
            )
            db.add(debt_assumption)
            results['debt_repayment_assumptions'].append(debt_data)
        except Exception as e:
            print(f"返済スケジュール前提の読み取りエラー（年度{i+1}）: {e}")
    
    # データ検証
    if validate:
        validation_result = validate_all_assumptions(
            results['working_capital_assumptions'],
            results['debt_repayment_assumptions']
        )
        results['validation'] = validation_result
        
        # エラーがある場合はロールバック
        if not validation_result['valid']:
            db.rollback()
            raise ValueError(f"データ検証エラー: {', '.join(validation_result['errors'])}")
    
    db.commit()
    
    return results
