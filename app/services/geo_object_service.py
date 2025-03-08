# app/services/geo_object_service.py
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
        # Check if simulation exists
        simulation = Simulation.get_by_id(simulation_id)
        if not simulation:
            return None
        
        # Validate bounding box if provided
        if bbox and not validate_bbox(bbox):
            raise ValueError("Invalid bounding box format")
        
        # Get geo objects
        geo_objects = GeoObject.get_by_simulation(simulation_id, bbox)
        
        # Transform into GeoJSON Feature Collection
        features = []
        for obj in geo_objects:
            # Parse the geometry from JSON string
            geometry = json.loads(obj['geometry'])
            
            # Calculate additional properties if needed
            # For example, if we have a center point of the simulation
            # we could calculate distance from each object to center
            additional_props = {}
            if 'center_point' in simulation and geometry['type'] == 'Point':
                center = simulation['center_point']
                obj_coords = geometry['coordinates']
                distance = calculate_distance((center[0], center[1]), (obj_coords[0], obj_coords[1]))
                additional_props['distance_from_center'] = round(distance, 2)
            
            # Create a GeoJSON Feature
            feature = {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "id": obj['id'],
                    "name": obj['name'],
                    "role": obj['role'],
                    "description": obj['description'],
                    **additional_props  # Add any additional calculated properties
                }
            }
            features.append(feature)
        
        # Format as proper GeoJSON FeatureCollection using our utility
        geojson = format_as_geojson(features)
        
        # Add metadata
        geojson["metadata"] = {
            "simulation_id": simulation_id,
            "year": simulation['year'],
            "city": simulation['city_name'],
            "mode": simulation['mode_name'],
            "count": len(features),
            "bbox": bbox
        }
        
        return geojson
    
    @staticmethod
    def find_nearest_objects(point, simulation_id, max_distance=5.0, limit=10):
        """
        Find the nearest geographic objects to a given point.
        
        Args:
            point: [longitude, latitude] coordinates
            simulation_id: ID of the simulation
            max_distance: Maximum distance in kilometers
            limit: Maximum number of results
            
        Returns:
            List of nearest objects with distance information
        """
        # Implementation would require a specialized query to PostGIS
        # This is a placeholder to show how it would integrate with utilities
        pass
    
    @staticmethod
    def get_object_timeline(geo_object_id):
        """
        Get all simulations that contain a specific geographic object.
        This shows the timeline of when this object existed.
        
        Args:
            geo_object_id: ID of the geographic object
            
        Returns:
            Timeline data for the object
        """
        # Implementation would follow similar pattern to above
        pass
