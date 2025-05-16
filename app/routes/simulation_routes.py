from flask import Blueprint, jsonify, request
from app.models.simulation import Simulation

simulation_bp = Blueprint('simulation', __name__)

@simulation_bp.route('/', methods=['GET'])
def get_simulations():
    """Get all simulations"""
    simulations = Simulation.get_all()
    return jsonify(simulations)

@simulation_bp.route('/<int:simulation_id>', methods=['GET'])
def get_simulation(simulation_id):
    """Get simulation by ID"""
    simulation = Simulation.get_by_id(simulation_id)
    if not simulation:
        return jsonify({'error': 'Simulation not found'}), 404
    return jsonify(simulation)

@simulation_bp.route('/city/<int:city_id>/years', methods=['GET'])
def get_years_by_city(city_id):
    """Get all years available for a city"""
    years = Simulation.get_years_by_city(city_id)
    return jsonify(years)

@simulation_bp.route('/city/<int:city_id>/year/<int:year>/mode/<int:mode_id>', methods=['GET'])
def get_simulation_by_city_year(city_id, year, mode_id):
    """Get simulation by city and year"""
    simulation = Simulation.get_by_city_year(city_id, year, mode_id)
    if not simulation:
        return jsonify({'error': 'Simulation not found'}), 404
    return jsonify(simulation)

