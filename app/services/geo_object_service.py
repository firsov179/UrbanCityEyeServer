import json
from app.models import GeoObject, Simulation
from app.utils import format_as_geojson, calculate_distance, validate_bbox

class GeoObjectService:
    @staticmethod
    def get_geo_objects_for_simulation(simulation_id, bbox=None):
        """
        Get geographic objects for a specific simulation.
        Optionally filtered by a bounding box.
        
        Args:
            simulation_id: ID of the simulation
            bbox: Optional bounding box as [minx, miny, maxx, maxy]
            
        Returns:
            GeoJSON FeatureCollection or None if simulation not found
        """
        simulation = Simulation.get_by_id(simulation_id)
        if not simulation:
            return None
        
        if bbox and not validate_bbox(bbox):
            raise ValueError("Invalid bounding box format")
        
        geo_objects = GeoObject.get_by_simulation(simulation_id, bbox)
        
        features = []
        for obj in geo_objects:
            geometry = json.loads(obj['geometry'])
            
            additional_props = {}
            if 'center_point' in simulation and geometry['type'] == 'Point':
                center = simulation['center_point']
                obj_coords = geometry['coordinates']
                distance = calculate_distance((center[0], center[1]), (obj_coords[0], obj_coords[1]))
                additional_props['distance_from_center'] = round(distance, 2)
            
            feature = {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "id": obj['id'],
                    "name": obj['name'],
                    "role": obj['role'],
                    "description": obj['description'],
                    **additional_props
                }
            }
            features.append(feature)
        
        geojson = format_as_geojson(features)
        
        geojson["metadata"] = {
            "simulation_id": simulation_id,
            "year": simulation['year'],
            "city": simulation['city_name'],
            "mode": simulation['mode_name'],
            "count": len(features),
            "bbox": bbox
        }
        
        return geojson
