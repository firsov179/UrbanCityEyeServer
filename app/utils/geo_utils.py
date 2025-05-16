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
    R = 6371.0
    
    lon1, lat1 = point1
    lon2, lat2 = point2
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance

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
