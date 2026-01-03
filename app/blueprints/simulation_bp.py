"""
シミュレーションAPI Blueprint
複数年度の経営予測、内部留保シミュレーション、借入金許容限度額分析などを提供
"""
from flask import Blueprint, request, jsonify
from app.db import SessionLocal
from app.models_decision import (
    FiscalYear, ProfitLossStatement, BalanceSheet,
    Simulation, SimulationResult
)
from app.services.simulation_service import SimulationService
from datetime import datetime

simulation_bp = Blueprint('simulation', __name__, url_prefix='/api/simulation')


def get_base_data(fiscal_year_id: int, db):
    """
    会計年度の基準データを取得
    
    Args:
        fiscal_year_id: 会計年度ID
        db: データベースセッション
    
    Returns:
        基準データの辞書
    """
    # P/Lデータ
    pl = db.query(ProfitLossStatement).filter(
        ProfitLossStatement.fiscal_year_id == fiscal_year_id
    ).first()
    
    # B/Sデータ
    bs = db.query(BalanceSheet).filter(
        BalanceSheet.fiscal_year_id == fiscal_year_id
    ).first()
    
    if not pl or not bs:
        return None
    
    return {
        'sales': pl.sales,
        'cost_of_sales': pl.cost_of_sales,
        'gross_profit': pl.gross_profit,
        'operating_expenses': pl.operating_expenses,
        'operating_income': pl.operating_income,
        'ordinary_income': pl.ordinary_income,
        'income_before_tax': pl.income_before_tax,
        'net_income': pl.net_income,
        'total_assets': bs.total_assets,
        'current_assets': bs.current_assets,
        'fixed_assets': bs.fixed_assets,
        'tangible_fixed_assets': bs.fixed_assets * 0.8,  # 簡易計算
        'net_assets': bs.total_equity,
        'retained_earnings': bs.retained_earnings,
        'total_liabilities': bs.total_liabilities,
        'total_debt': bs.total_liabilities * 0.5  # 簡易計算
    }


@simulation_bp.route('/multi-year/<int:fiscal_year_id>', methods=['POST'])
def simulate_multi_year(fiscal_year_id):
    """複数年度の経営計画をシミュレーション"""
    data = request.get_json()
    
    db = SessionLocal()
    try:
        # 基準データを取得
        base_data = get_base_data(fiscal_year_id, db)
        if not base_data:
            return jsonify({'error': '基準年度の財務データが見つかりません'}), 404
        
        # シミュレーション前提条件
        assumptions = data.get('assumptions', {})
        years = data.get('years', 3)
        
        # シミュレーション実行
        results = SimulationService.simulate_multi_year_plan(base_data, assumptions, years)
        
        # シミュレーション設定を保存
        simulation = Simulation(
            fiscal_year_id=fiscal_year_id,
            simulation_type='multi_year',
            assumptions=str(assumptions),
            years=years
        )
        db.add(simulation)
        db.commit()
        
        # シミュレーション結果を保存
        for result in results:
            sim_result = SimulationResult(
                simulation_id=simulation.id,
                year=result['year'],
                sales=result['sales'],
                operating_income=result['operating_income'],
                ordinary_income=result['ordinary_income'],
                net_income=result['net_income'],
                total_assets=result['total_assets'],
                net_assets=result['net_assets'],
                equity_ratio=result['equity_ratio'],
                roe=result['roe'],
                roa=result['roa']
            )
            db.add(sim_result)
        
        db.commit()
        
        return jsonify({
            'simulation_id': simulation.id,
            'fiscal_year_id': fiscal_year_id,
            'years': years,
            'results': results
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@simulation_bp.route('/internal-reserve/<int:fiscal_year_id>', methods=['POST'])
def simulate_internal_reserve(fiscal_year_id):
    """内部留保シミュレーション"""
    data = request.get_json()
    
    db = SessionLocal()
    try:
        # 基準データを取得
        base_data = get_base_data(fiscal_year_id, db)
        if not base_data:
            return jsonify({'error': '基準年度の財務データが見つかりません'}), 404
        
        # シミュレーション条件
        target_equity_ratio = data.get('target_equity_ratio', 30.0)
        years = data.get('years', 5)
        
        # シミュレーション実行
        result = SimulationService.simulate_internal_reserve(base_data, target_equity_ratio, years)
        
        return jsonify({
            'fiscal_year_id': fiscal_year_id,
            'result': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@simulation_bp.route('/borrowing-capacity/<int:fiscal_year_id>', methods=['POST'])
def calculate_borrowing_capacity(fiscal_year_id):
    """借入金許容限度額を計算"""
    data = request.get_json()
    
    db = SessionLocal()
    try:
        # 基準データを取得
        base_data = get_base_data(fiscal_year_id, db)
        if not base_data:
            return jsonify({'error': '基準年度の財務データが見つかりません'}), 404
        
        # 計算前提条件
        assumptions = data.get('assumptions', {})
        
        # 借入金許容限度額を計算
        result = SimulationService.calculate_borrowing_capacity(base_data, assumptions)
        
        return jsonify({
            'fiscal_year_id': fiscal_year_id,
            'result': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@simulation_bp.route('/break-even/<int:fiscal_year_id>', methods=['POST'])
def simulate_break_even(fiscal_year_id):
    """損益分岐点分析"""
    data = request.get_json()
    
    db = SessionLocal()
    try:
        # 基準データを取得
        base_data = get_base_data(fiscal_year_id, db)
        if not base_data:
            return jsonify({'error': '基準年度の財務データが見つかりません'}), 404
        
        # 費用構造
        cost_structure = data.get('cost_structure', {})
        
        # 損益分岐点分析を実行
        result = SimulationService.simulate_break_even_analysis(base_data, cost_structure)
        
        return jsonify({
            'fiscal_year_id': fiscal_year_id,
            'result': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@simulation_bp.route('/differential-analysis', methods=['POST'])
def simulate_differential_analysis():
    """差額原価収益分析"""
    data = request.get_json()
    
    if 'base_scenario' not in data or 'alternative_scenario' not in data:
        return jsonify({'error': 'base_scenarioとalternative_scenarioは必須です'}), 400
    
    try:
        # 差額原価収益分析を実行
        result = SimulationService.simulate_differential_analysis(
            data['base_scenario'],
            data['alternative_scenario']
        )
        
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@simulation_bp.route('/list/<int:fiscal_year_id>', methods=['GET'])
def list_simulations(fiscal_year_id):
    """会計年度のシミュレーション一覧を取得"""
    db = SessionLocal()
    try:
        simulations = db.query(Simulation).filter(
            Simulation.fiscal_year_id == fiscal_year_id
        ).all()
        
        result = []
        for sim in simulations:
            result.append({
                'id': sim.id,
                'simulation_type': sim.simulation_type,
                'assumptions': sim.assumptions,
                'years': sim.years,
                'created_at': sim.created_at.isoformat() if sim.created_at else None
            })
        
        return jsonify({'simulations': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@simulation_bp.route('/<int:simulation_id>', methods=['GET'])
def get_simulation(simulation_id):
    """シミュレーション結果を取得"""
    db = SessionLocal()
    try:
        simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
        if not simulation:
            return jsonify({'error': 'シミュレーションが見つかりません'}), 404
        
        # シミュレーション結果を取得
        results = db.query(SimulationResult).filter(
            SimulationResult.simulation_id == simulation_id
        ).order_by(SimulationResult.year).all()
        
        result_data = []
        for result in results:
            result_data.append({
                'year': result.year,
                'sales': result.sales,
                'operating_income': result.operating_income,
                'ordinary_income': result.ordinary_income,
                'net_income': result.net_income,
                'total_assets': result.total_assets,
                'net_assets': result.net_assets,
                'equity_ratio': result.equity_ratio,
                'roe': result.roe,
                'roa': result.roa
            })
        
        return jsonify({
            'simulation': {
                'id': simulation.id,
                'fiscal_year_id': simulation.fiscal_year_id,
                'simulation_type': simulation.simulation_type,
                'assumptions': simulation.assumptions,
                'years': simulation.years,
                'created_at': simulation.created_at.isoformat() if simulation.created_at else None
            },
            'results': result_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@simulation_bp.route('/<int:simulation_id>', methods=['DELETE'])
def delete_simulation(simulation_id):
    """シミュレーションを削除"""
    db = SessionLocal()
    try:
        simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
        if not simulation:
            return jsonify({'error': 'シミュレーションが見つかりません'}), 404
        
        # 関連する結果も削除
        db.query(SimulationResult).filter(SimulationResult.simulation_id == simulation_id).delete()
        db.delete(simulation)
        db.commit()
        
        return jsonify({'message': 'シミュレーションを削除しました'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
