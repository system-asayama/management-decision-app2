"""
経営シミュレーション計算ロジック
"""

from typing import Dict, List, Optional
from decimal import Decimal


class SimulationCalculator:
    """経営シミュレーション計算クラス"""
    
    @staticmethod
    def forecast_financials(
        base_sales: float,
        base_operating_income: float,
        base_ordinary_income: float,
        base_net_income: float,
        base_total_assets: float,
        base_total_liabilities: float,
        base_total_equity: float,
        forecast_years: int,
        sales_growth_rate: float,
        operating_margin: Optional[float] = None,
        ordinary_margin: Optional[float] = None,
        net_margin: Optional[float] = None,
        asset_turnover: Optional[float] = None,
        debt_ratio: Optional[float] = None
    ) -> List[Dict]:
        """
        財務予測を実行
        
        Args:
            base_sales: ベース年度の売上高
            base_operating_income: ベース年度の営業利益
            base_ordinary_income: ベース年度の経常利益
            base_net_income: ベース年度の当期純利益
            base_total_assets: ベース年度の総資産
            base_total_liabilities: ベース年度の総負債
            base_total_equity: ベース年度の純資産
            forecast_years: 予測年数
            sales_growth_rate: 売上高成長率（%）
            operating_margin: 営業利益率（%）、Noneの場合はベース年度の比率を維持
            ordinary_margin: 経常利益率（%）、Noneの場合はベース年度の比率を維持
            net_margin: 当期純利益率（%）、Noneの場合はベース年度の比率を維持
            asset_turnover: 総資産回転率、Noneの場合はベース年度の比率を維持
            debt_ratio: 負債比率（%）、Noneの場合はベース年度の比率を維持
        
        Returns:
            予測結果のリスト
        """
        results = []
        
        # ベース年度の比率を計算
        base_operating_margin = (base_operating_income / base_sales * 100) if base_sales > 0 else 0
        base_ordinary_margin = (base_ordinary_income / base_sales * 100) if base_sales > 0 else 0
        base_net_margin = (base_net_income / base_sales * 100) if base_sales > 0 else 0
        base_asset_turnover = (base_sales / base_total_assets) if base_total_assets > 0 else 1.0
        base_debt_ratio = (base_total_liabilities / base_total_equity * 100) if base_total_equity > 0 else 100
        
        # 使用する比率を決定
        target_operating_margin = operating_margin if operating_margin is not None else base_operating_margin
        target_ordinary_margin = ordinary_margin if ordinary_margin is not None else base_ordinary_margin
        target_net_margin = net_margin if net_margin is not None else base_net_margin
        target_asset_turnover = asset_turnover if asset_turnover is not None else base_asset_turnover
        target_debt_ratio = debt_ratio if debt_ratio is not None else base_debt_ratio
        
        # 成長率を小数に変換
        growth_rate = sales_growth_rate / 100
        
        # 各年度の予測を計算
        current_sales = base_sales
        current_equity = base_total_equity
        
        for year in range(1, forecast_years + 1):
            # 売上高の予測
            current_sales = current_sales * (1 + growth_rate)
            
            # 利益の予測
            operating_income = current_sales * (target_operating_margin / 100)
            ordinary_income = current_sales * (target_ordinary_margin / 100)
            net_income = current_sales * (target_net_margin / 100)
            
            # 純資産の予測（前年度純資産 + 当期純利益）
            current_equity = current_equity + net_income
            
            # 総資産の予測（売上高 ÷ 総資産回転率）
            total_assets = current_sales / target_asset_turnover if target_asset_turnover > 0 else current_sales
            
            # 総負債の予測（純資産 × 負債比率）
            total_liabilities = current_equity * (target_debt_ratio / 100)
            
            # バランス調整（総資産 = 総負債 + 純資産）
            if total_assets < (total_liabilities + current_equity):
                total_assets = total_liabilities + current_equity
            else:
                # 総資産が大きい場合は負債を調整
                total_liabilities = total_assets - current_equity
            
            results.append({
                'year_offset': year,
                'sales': round(current_sales, 2),
                'operating_income': round(operating_income, 2),
                'ordinary_income': round(ordinary_income, 2),
                'net_income': round(net_income, 2),
                'total_assets': round(total_assets, 2),
                'total_liabilities': round(total_liabilities, 2),
                'total_equity': round(current_equity, 2)
            })
        
        return results
    
    @staticmethod
    def create_scenario_forecasts(
        base_sales: float,
        base_operating_income: float,
        base_ordinary_income: float,
        base_net_income: float,
        base_total_assets: float,
        base_total_liabilities: float,
        base_total_equity: float,
        forecast_years: int,
        base_growth_rate: float
    ) -> Dict[str, List[Dict]]:
        """
        3つのシナリオ（楽観・標準・悲観）の予測を作成
        
        Args:
            base_sales: ベース年度の売上高
            base_operating_income: ベース年度の営業利益
            base_ordinary_income: ベース年度の経常利益
            base_net_income: ベース年度の当期純利益
            base_total_assets: ベース年度の総資産
            base_total_liabilities: ベース年度の総負債
            base_total_equity: ベース年度の純資産
            forecast_years: 予測年数
            base_growth_rate: 標準シナリオの成長率（%）
        
        Returns:
            シナリオ別の予測結果
        """
        # 楽観シナリオ: 成長率 +50%
        optimistic = SimulationCalculator.forecast_financials(
            base_sales, base_operating_income, base_ordinary_income, base_net_income,
            base_total_assets, base_total_liabilities, base_total_equity,
            forecast_years, base_growth_rate * 1.5
        )
        
        # 標準シナリオ
        standard = SimulationCalculator.forecast_financials(
            base_sales, base_operating_income, base_ordinary_income, base_net_income,
            base_total_assets, base_total_liabilities, base_total_equity,
            forecast_years, base_growth_rate
        )
        
        # 悲観シナリオ: 成長率 -50%
        pessimistic = SimulationCalculator.forecast_financials(
            base_sales, base_operating_income, base_ordinary_income, base_net_income,
            base_total_assets, base_total_liabilities, base_total_equity,
            forecast_years, base_growth_rate * 0.5
        )
        
        return {
            'optimistic': optimistic,
            'standard': standard,
            'pessimistic': pessimistic
        }
    
    @staticmethod
    def calculate_financial_ratios(forecast_data: List[Dict]) -> List[Dict]:
        """
        予測データから財務指標を計算
        
        Args:
            forecast_data: 予測データのリスト
        
        Returns:
            財務指標を含む予測データのリスト
        """
        results = []
        
        for data in forecast_data:
            sales = data['sales']
            operating_income = data['operating_income']
            ordinary_income = data['ordinary_income']
            net_income = data['net_income']
            total_assets = data['total_assets']
            total_equity = data['total_equity']
            
            # 財務指標を計算
            operating_margin = (operating_income / sales * 100) if sales > 0 else 0
            ordinary_margin = (ordinary_income / sales * 100) if sales > 0 else 0
            net_margin = (net_income / sales * 100) if sales > 0 else 0
            roa = (net_income / total_assets * 100) if total_assets > 0 else 0
            roe = (net_income / total_equity * 100) if total_equity > 0 else 0
            equity_ratio = (total_equity / total_assets * 100) if total_assets > 0 else 0
            
            results.append({
                **data,
                'operating_margin': round(operating_margin, 2),
                'ordinary_margin': round(ordinary_margin, 2),
                'net_margin': round(net_margin, 2),
                'roa': round(roa, 2),
                'roe': round(roe, 2),
                'equity_ratio': round(equity_ratio, 2)
            })
        
        return results
