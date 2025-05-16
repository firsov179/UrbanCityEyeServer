"""
Response utilities.
Contains functions for creating standardized API responses.
"""
from typing import Dict, Any, Optional, List, Union
from flask import jsonify

def create_error_response(message: str, status_code: int = 400, errors: Optional[List[Dict]] = None) -> Dict:
    """
    Create a standardized error response.
    
    Args:
        message: Main error message
        status_code: HTTP status code
        errors: List of detailed error information
        
    Returns:
        Error response dictionary
    """
    response = {
        "success": False,
        "message": message,
        "status_code": status_code
    }
    
    if errors:
        response["errors"] = errors
    
    return jsonify(response), status_code

def create_success_response(data: Any = None, message: str = "Success", meta: Optional[Dict] = None) -> Dict:
    """
    Create a standardized success response.
    
    Args:
        data: Response data
        message: Success message
        meta: Additional metadata
        
    Returns:
        Success response dictionary
    """
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    
    if meta:
        response["meta"] = meta
    
    return jsonify(response)

def paginate_results(results: List, page: int = 1, page_size: int = 20) -> Dict:
    """
    Create a paginated response.
    
    Args:
        results: List of items to paginate
        page: Current page number (1-based)
        page_size: Number of items per page
        
    Returns:
        Dictionary with paginated results and pagination metadata
    """
    total_items = len(results)
    total_pages = (total_items + page_size - 1) // page_size
    
    page = max(1, min(page, total_pages if total_pages > 0 else 1))
    
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_items)
    
    items = results[start_idx:end_idx]
    
    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }
