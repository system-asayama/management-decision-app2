"""
借入金許容限度額分析 - Method1とMethod3
Excelの資金力シートの数式をそのまま実装
"""

from ..db import SessionLocal
from ..models_decision import (
    FiscalYear, ProfitLossStatement, BalanceSheet
)


def calculate_debt_capacity_method1(fiscal_year_id):
    """
    Method1: 借入金許容限度額（資金力-1借入金許容限度額）
    
    Excelの数式:
    1. 金融調達率より = 総資本 × 30%
    2. 借入金依存率より = 年間売上高 × 20%
    3. 担保力より = (土地（時価） + 有価証券（時価）) × 50%
    
    Args:
        fiscal_year_id: 会計年度ID
    
    Returns:
        dict: {
            'method1_financial_procurement': 金融調達率による許容額,
            'method1_debt_dependence': 借入金依存率による許容額,
            'method1_collateral': 担保力による許容額,
            'total_assets': 総資本,
            'sales': 売上高,
            'land_value': 土地（時価）,
            'securities_value': 有価証券（時価）
        }
    """
    db = SessionLocal()
    
    try:
        # 会計年度を取得
        fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == fiscal_year_id
        ).first()
        
        if not fiscal_year:
            raise ValueError(f"会計年度ID {fiscal_year_id} が見つかりません")
        
        # PLを取得
        pl = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == fiscal_year_id
        ).first()
        
        # BSを取得
        bs = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not pl or not bs:
            raise ValueError(f"会計年度ID {fiscal_year_id} のPL/BSが見つかりません")
        
        # 基礎データ
        total_assets = float(bs.total_assets or 0)  # 総資本
        sales = float(pl.sales or 0)  # 売上高
        
        # 土地と有価証券（BSから取得）
        land_value = float(getattr(bs, 'land_market_value', 0) or 0)  # 土地（時価）
        securities_value = float(getattr(bs, 'securities_market_value', 0) or 0)  # 有価証券（時価）
        
        # Excelの数式どおりに計算
        # 1. 金融調達率より = 総資本 × 30%
        method1_financial_procurement = total_assets * 0.3
        
        # 2. 借入金依存率より = 年間売上高 × 20%
        method1_debt_dependence = sales * 0.2
        
        # 3. 担保力より = (土地（時価） + 有価証券（時価）) × 50%
        method1_collateral = (land_value + securities_value) * 0.5
        
        return {
            'method1_financial_procurement': round(method1_financial_procurement, 2),
            'method1_debt_dependence': round(method1_debt_dependence, 2),
            'method1_collateral': round(method1_collateral, 2),
            'total_assets': round(total_assets, 2),
            'sales': round(sales, 2),
            'land_value': round(land_value, 2),
            'securities_value': round(securities_value, 2)
        }
        
    except Exception as e:
        raise Exception(f"Method1計算エラー: {str(e)}")
    finally:
        db.close()


def calculate_debt_capacity_method3(fiscal_year_id, standard_gross_profit_interest_rate=None):
    """
    Method3: 借入金許容限度額（資金力--3借入金許容限度額分析）
    
    Excelの数式:
    許容限度額 = 売上総利益 × 標準売上総利益金融費用率 ÷ 平均金利
    
    Args:
        fiscal_year_id: 会計年度ID
        standard_gross_profit_interest_rate: 標準売上総利益金融費用率（デフォルト: 0.0188）
    
    Returns:
        dict: {
            'method3_allowable_debt': 許容限度額,
            'gross_profit': 売上総利益,
            'standard_rate': 標準売上総利益金融費用率,
            'average_interest_rate': 平均金利,
            'interest_bearing_debt': 有利子負債,
            'surplus': 余裕額,
            'surplus_ratio': 余裕率
        }
    """
    db = SessionLocal()
    
    try:
        # 標準売上総利益金融費用率のデフォルト値（Excelより）
        if standard_gross_profit_interest_rate is None:
            standard_gross_profit_interest_rate = 0.0188
        
        # 会計年度を取得
        fiscal_year = db.query(FiscalYear).filter(
            FiscalYear.id == fiscal_year_id
        ).first()
        
        if not fiscal_year:
            raise ValueError(f"会計年度ID {fiscal_year_id} が見つかりません")
        
        # PLを取得
        pl = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == fiscal_year_id
        ).first()
        
        # BSを取得
        bs = db.query(BalanceSheet).filter(
            BalanceSheet.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not pl or not bs:
            raise ValueError(f"会計年度ID {fiscal_year_id} のPL/BSが見つかりません")
        
        # 基礎データ
        gross_profit = float(pl.gross_profit or 0)  # 売上総利益
        
        # 金融費用（営業外費用を金融費用とみなす）
        interest_expense = float(pl.non_operating_expenses or 0)
        
        # 有利子負債（BSから計算）
        # 有利子負債 = 短期借入金 + 長期借入金（BSモデルに項目がない場合は概算）
        # 注: BSモデルに借入金の項目がない場合は、固定負債の一部とみなす
        interest_bearing_debt = float(bs.fixed_liabilities or 0) * 0.5  # 概算
        
        # 平均金利を計算
        if interest_bearing_debt > 0:
            average_interest_rate = interest_expense / interest_bearing_debt
        else:
            average_interest_rate = 0.0172  # デフォルト値（Excelの3期平均金利）
        
        # Excelの数式どおりに計算
        # 許容限度額 = 売上総利益 × 標準売上総利益金融費用率 ÷ 平均金利
        if average_interest_rate > 0:
            method3_allowable_debt = (gross_profit * standard_gross_profit_interest_rate) / average_interest_rate
        else:
            method3_allowable_debt = 0.0
        
        # 余裕額 = 許容限度額 - 有利子負債
        surplus = method3_allowable_debt - interest_bearing_debt
        
        # 余裕率 = 余裕額 ÷ 許容限度額
        if method3_allowable_debt > 0:
            surplus_ratio = surplus / method3_allowable_debt
        else:
            surplus_ratio = 0.0
        
        return {
            'method3_allowable_debt': round(method3_allowable_debt, 2),
            'gross_profit': round(gross_profit, 2),
            'standard_rate': round(standard_gross_profit_interest_rate, 4),
            'average_interest_rate': round(average_interest_rate, 4),
            'interest_bearing_debt': round(interest_bearing_debt, 2),
            'surplus': round(surplus, 2),
            'surplus_ratio': round(surplus_ratio, 4)
        }
        
    except Exception as e:
        raise Exception(f"Method3計算エラー: {str(e)}")
    finally:
        db.close()



def calculate_debt_capacity_rate_table(fiscal_year_id, standard_gross_profit_interest_rate=0.10):
    """
    資金力--4: 金利階段表による借入金許容限度額
    
    利率を0.5%刻みで0.5%〜8%まで変化させ、
    それぞれの平均金利に対してMethod3の計算式を適用して許容借入額をテーブルで返す。
    
    Args:
        fiscal_year_id: 会計年度ID
        standard_gross_profit_interest_rate: 標準売上総利益金融費用率（デフォルト: 0.10 = 10%）
    
    Returns:
        dict: {
            'rate_table': [
                {
                    'interest_rate': 金利（%）,
                    'interest_rate_decimal': 金利（小数）,
                    'allowable_debt': 許容借入額,
                    'annual_interest_payment': 年間支払利息
                },
                ...
            ],
            'gross_profit': 売上総利益,
            'standard_rate': 標準売上総利益金融費用率
        }
    """
    db = SessionLocal()
    
    try:
        # PLを取得
        pl = db.query(ProfitLossStatement).filter(
            ProfitLossStatement.fiscal_year_id == fiscal_year_id
        ).first()
        
        if not pl:
            raise ValueError(f"会計年度ID {fiscal_year_id} のPLが見つかりません")
        
        # 売上総利益
        gross_profit = float(pl.gross_profit or 0)
        
        # 標準売上総利益金融費用率（デフォルト: 10%）
        if standard_gross_profit_interest_rate is None:
            standard_gross_profit_interest_rate = 0.10
        
        # 金利階段表を作成（0.5%〜8.0%、0.5%刻み）
        rate_table = []
        for rate_percent in range(5, 85, 5):  # 5 = 0.5%, 85 = 8.5%（8.0%まで）
            interest_rate_percent = rate_percent / 10.0  # 0.5, 1.0, 1.5, ...
            interest_rate_decimal = interest_rate_percent / 100.0  # 0.005, 0.01, 0.015, ...
            
            # Method3の計算式: 許容限度額 = 売上総利益 × 標準率 ÷ 平均金利
            if interest_rate_decimal > 0:
                allowable_debt = (gross_profit * standard_gross_profit_interest_rate) / interest_rate_decimal
                annual_interest_payment = allowable_debt * interest_rate_decimal
            else:
                allowable_debt = 0.0
                annual_interest_payment = 0.0
            
            rate_table.append({
                'interest_rate': round(interest_rate_percent, 1),
                'interest_rate_decimal': round(interest_rate_decimal, 4),
                'allowable_debt': round(allowable_debt, 2),
                'annual_interest_payment': round(annual_interest_payment, 2)
            })
        
        return {
            'rate_table': rate_table,
            'gross_profit': round(gross_profit, 2),
            'standard_rate': standard_gross_profit_interest_rate,
            'standard_rate_percent': round(standard_gross_profit_interest_rate * 100, 2)
        }
        
    except Exception as e:
        raise Exception(f"金利階段表計算エラー: {str(e)}")
    finally:
        db.close()
