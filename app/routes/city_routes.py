from flask import Blueprint, jsonify, request, Response
from app.models.city import City
from app.services.city_service import CityService

city_bp = Blueprint('city', __name__)

@city_bp.route('/', methods=['GET'])
def get_cities():
    """Get all cities"""
    cities = City.get_all()
    return jsonify(cities)


@city_bp.route('/<int:city_id>', methods=['GET'])
def get_city(city_id):
    """Get city by ID"""
    city = City.get_by_id(city_id)
    if not city:
        return jsonify({'error': 'City not found'}), 404
    return jsonify(city)
