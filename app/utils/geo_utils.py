"""
Geo utilities.
Contains helper functions for working with geographic data.
"""
import math
from typing import Tuple, List, Dict, Union

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate the Haversine distance between two points in km.
    
    Args:
        point1: (longitude, latitude) of the first point
        point2: (longitude, latitude) of the second point
        
    Returns:
        Distance in kilometers
    """
    # Earth radius in kilometers
    R = 6371.0
    
    lon1, lat1 = point1
    lon2, lat2 = point2
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Difference in coordinates
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance

def convert_coordinates(coords: List[float], from_srid: int, to_srid: int) -> List[float]:
    """
    Convert coordinates from one spatial reference system to another.
    
    NOTE: This is a placeholder function. In a real application, you would
    use a library like pyproj or interact with PostGIS functions for this.
    
    Args:
        coords: [x, y] or [lon, lat] coordinates
        from_srid: Source SRID (e.g., 4326 for WGS84)
        to_srid: Target SRID (e.g., 3857 for Web Mercator)
        
    Returns:
        Converted coordinates
    """
    # Placeholder implementation - in a real app, use proper conversion
    if from_srid == 4326 and to_srid == 3857:
        # Very simplified WGS84 to Web Mercator conversion
        x = coords[0] * 20037508.34 / 180
        y = math.log(math.tan((90 + coords[1]) * math.pi / 360)) / (math.pi / 180)
        y = y * 20037508.34 / 180
        return [x, y]
    elif from_srid == 3857 and to_srid == 4326:
        # Very simplified Web Mercator to WGS84 conversion
        x = coords[0] * 180 / 20037508.34
        y = coords[1] * 180 / 20037508.34
        y = 180 / math.pi * (2 * math.atan(math.exp(y * math.pi / 180)) - math.pi / 2)
        return [x, y]
    else:
        # For other conversions, we'd use a proper library
        # This is a fallback that just returns the original coordinates
        return coords

def validate_bbox(bbox: List[float]) -> bool:
    """
    Validate a bounding box.
    
    Args:
        bbox: [minx, miny, maxx, maxy]
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(bbox, list) or len(bbox) != 4:
        return False
    
    try:
        minx, miny, maxx, maxy = [float(coord) for coord in bbox]
        
        # Basic validation checks
        if minx > maxx or miny > maxy:
            return False
            
        # For longitude/latitude bounds
        if minx < -180 or maxx > 180 or miny < -90 or maxy > 90:
            return False
            
        return True
    except (ValueError, TypeError):
        return False

def format_as_geojson(features: List[Dict]) -> Dict:
    """
    Format a list of features as a GeoJSON FeatureCollection.
    
    Args:
        features: List of GeoJSON Feature objects
        
    Returns:
        GeoJSON FeatureCollection
    """
    return {
        "type": "FeatureCollection",
        "features": features
    }
