"""
Validation utilities.
Contains functions for validating input data.
"""
from typing import Dict, List, Any, Optional, Union
import re

def validate_geojson(geojson: Dict) -> bool:
    """
    Validate a GeoJSON object structure.
    
    Args:
        geojson: GeoJSON object to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(geojson, dict):
        return False
    
    if 'type' not in geojson:
        return False
    
    if geojson['type'] == 'FeatureCollection':
        if 'features' not in geojson or not isinstance(geojson['features'], list):
            return False
        
        for feature in geojson['features']:
            if not validate_geojson_feature(feature):
                return False
                
        return True
    
    elif geojson['type'] == 'Feature':
        return validate_geojson_feature(geojson)
    
    elif geojson['type'] in ['Point', 'LineString', 'Polygon', 'MultiPoint', 
                            'MultiLineString', 'MultiPolygon', 'GeometryCollection']:
        return 'coordinates' in geojson or 'geometries' in geojson
    
    return False

def validate_geojson_feature(feature: Dict) -> bool:
    """
    Validate a GeoJSON Feature.
    
    Args:
        feature: GeoJSON Feature to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(feature, dict):
        return False
    
    if 'type' not in feature or feature['type'] != 'Feature':
        return False
    
    if 'geometry' not in feature or not isinstance(feature['geometry'], dict):
        return False
    
    if 'properties' not in feature or not isinstance(feature['properties'], dict):
        return False
    
    return True

def validate_year(year: Union[str, int]) -> bool:
    """
    Validate a year value.
    
    Args:
        year: Year to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        year_int = int(year)
        return 1000 <= year_int <= 3000
    except (ValueError, TypeError):
        return False

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

        if minx > maxx or miny > maxy:
            return False

        if minx < -180 or maxx > 180 or miny < -90 or maxy > 90:
            return False

        return True
    except (ValueError, TypeError):
        return False

def sanitize_string(input_str: Optional[str], max_length: int = 255) -> str:
    """
    Sanitize a string input by removing potentially dangerous characters.
    
    Args:
        input_str: String to sanitize
        max_length: Maximum length allowed
        
    Returns:
        Sanitized string
    """
    if input_str is None:
        return ""
    
    sanitized = re.sub(r'[<>\'";]', '', input_str)
    
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized
