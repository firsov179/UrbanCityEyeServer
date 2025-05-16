from flask import Blueprint, jsonify, request
from app.models import GeoObject
from app.services import GeoObjectService
from app.utils import validate_bbox, create_error_response, create_success_response
import json

geo_object_bp = Blueprint('geo_object', __name__)


@geo_object_bp.route('/simulation/<int:simulation_id>', methods=['GET'])
def get_geo_objects_by_simulation(simulation_id):
    """Get geographic objects for a specific simulation"""
    bbox = None
    if all(param in request.args for param in ['minx', 'miny', 'maxx', 'maxy']):
        bbox = [
            float(request.args.get('minx')),
            float(request.args.get('miny')),
            float(request.args.get('maxx')),
            float(request.args.get('maxy'))
        ]

        if not validate_bbox(bbox):
            return create_error_response("Invalid bounding box parameters", 400)

    try:
        geojson = GeoObjectService.get_geo_objects_for_simulation(simulation_id, bbox)

        if not geojson:
            return create_error_response("Simulation not found", 404)

        return create_success_response(geojson)
    except Exception as e:
        return create_error_response(f"Error retrieving geographic objects: {str(e)}", 500)


@geo_object_bp.route('/<int:geo_object_id>', methods=['GET'])
def get_geo_object(geo_object_id):
    """Get geographic object by ID"""
    geo_object = GeoObject.get_by_id(geo_object_id)
    if not geo_object:
        return jsonify({'error': 'Geographic object not found'}), 404

    feature = {
        "type": "Feature",
        "geometry": json.loads(geo_object['geometry']),
        "properties": {
            "id": geo_object['id'],
            "name": geo_object['name'],
            "role": geo_object['role'],
            "description": geo_object['description']
        }
    }

    return jsonify(feature)
