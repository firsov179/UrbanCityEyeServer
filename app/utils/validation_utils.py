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
    # Check if it's a dictionary
    if not isinstance(geojson, dict):
        return False
    
    # Check if it has a 'type' property
    if 'type' not in geojson:
        return False
    
    # Check type for FeatureCollection
    if geojson['type'] == 'FeatureCollection':
        if 'features' not in geojson or not isinstance(geojson['features'], list):
            return False
        
        # Check each feature
        for feature in geojson['features']:
            if not validate_geojson_feature(feature):
                return False
                
        return True
    
    # Check if it's a single feature
    elif geojson['type'] == 'Feature':
        return validate_geojson_feature(geojson)
    
    # Check if it's a geometry
    elif geojson['type'] in ['Point', 'LineString', 'Polygon', 'MultiPoint', 
                            'MultiLineString', 'MultiPolygon', 'GeometryCollection']:
        # Simple validation for geometries
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
    # Check if it's a dictionary
    if not isinstance(feature, dict):
        return False
    
    # Check if it has required properties
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
        return 1000 <= year_int <= 3000  # Adjust range as needed
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
    
    # Replace potentially dangerous characters
    sanitized = re.sub(r'[<>\'";]', '', input_str)
    
    # Trim to max length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized
