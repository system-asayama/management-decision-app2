"""
BSシートから土地・有価証券の時価を読み取るモジュール
"""

def read_land_and_securities_market_value(wb, fiscal_year_index):
    """
    ＢＳの組換えシートから土地と有価証券の時価を読み取る
    
    Args:
        wb: openpyxlワークブック
        fiscal_year_index: 会計年度インデックス（0=初年度, 1=2年度, 2=3年度）
    
    Returns:
        dict: {
            'land_market_value': 土地の時価,
            'securities_market_value': 有価証券の時価
        }
    """
    # シート名（初年度=ＢＳの組換え, 2年度=ＢＳの組換え (2), 3年度=ＢＳの組換え (3)）
    sheet_names = ['ＢＳの組換え', 'ＢＳの組換え (2)', 'ＢＳの組換え (3)']
    
    try:
        ws = wb[sheet_names[fiscal_year_index]]
    except KeyError:
        raise ValueError(f"シート '{sheet_names[fiscal_year_index]}' が見つかりません")
    
    def get_cell_value(row, column):
        """セルの値を取得（Noneの場合は0.0を返す）"""
        value = ws.cell(row, column).value
        if value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    # 土地の時価（Row 26, Column F）
    # Excelの「その他」の行が土地の時価を表している可能性があるが、
    # 実際には資金力-1シートのRow 8に土地の時価がある
    # ここでは資金力-1シートから読み取る
    
    # 資金力-1シートから読み取る
    try:
        ws_capital = wb['資金力-1借入金許容限度額']
        
        # 土地の時価（Row 8, Column K/L/M）
        # 列インデックス（初年度=K=11, 2年度=L=12, 3年度=M=13）
        col = 11 + fiscal_year_index
        land_market_value = get_cell_value_from_sheet(ws_capital, 8, col)
        
        # 有価証券の時価（Row 9, Column K/L/M）
        securities_market_value = get_cell_value_from_sheet(ws_capital, 9, col)
        
        return {
            'land_market_value': land_market_value,
            'securities_market_value': securities_market_value
        }
    except KeyError:
        # 資金力-1シートが見つからない場合は、BSシートから土地の簿価を取得
        # Row 26, Column F（土地の簿価）
        land_book_value = get_cell_value(26, 6)  # F列 = 6
        
        # Row 32, Column F（投資有価証券の簿価）
        securities_book_value = get_cell_value(32, 6)
        
        return {
            'land_market_value': land_book_value,
            'securities_market_value': securities_book_value
        }


def get_cell_value_from_sheet(ws, row, column):
    """指定されたシートからセルの値を取得"""
    value = ws.cell(row, column).value
    if value is None:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def import_bs_market_values(wb, company_id, fiscal_year_ids, db):
    """
    土地・有価証券の時価をExcelから一括インポートしてBSに反映
    
    Args:
        wb: openpyxlワークブック
        company_id: 企業ID
        fiscal_year_ids: 会計年度IDのリスト（[初年度ID, 2年度ID, 3年度ID]）
        db: データベースセッション
    
    Returns:
        dict: インポート結果
    """
    from ..models_decision import BalanceSheet
    
    results = {
        'balance_sheets': [],
        'success': True
    }
    
    # 3年度分のデータを読み取る
    for i, fiscal_year_id in enumerate(fiscal_year_ids):
        try:
            # 土地・有価証券の時価を読み取る
            market_values = read_land_and_securities_market_value(wb, i)
            
            # BSを取得
            bs = db.query(BalanceSheet).filter(
                BalanceSheet.fiscal_year_id == fiscal_year_id
            ).first()
            
            if bs:
                # 既存のBSを更新
                bs.land_market_value = int(market_values['land_market_value'])
                bs.securities_market_value = int(market_values['securities_market_value'])
            else:
                # BSが存在しない場合は新規作成（通常はあり得ない）
                bs = BalanceSheet(
                    fiscal_year_id=fiscal_year_id,
                    land_market_value=int(market_values['land_market_value']),
                    securities_market_value=int(market_values['securities_market_value'])
                )
                db.add(bs)
            
            results['balance_sheets'].append({
                'fiscal_year_id': fiscal_year_id,
                'land_market_value': market_values['land_market_value'],
                'securities_market_value': market_values['securities_market_value']
            })
        except Exception as e:
            print(f"土地・有価証券の時価の読み取りエラー（年度{i+1}）: {e}")
            results['success'] = False
    
    if results['success']:
        db.commit()
    else:
        db.rollback()
    
    return results
