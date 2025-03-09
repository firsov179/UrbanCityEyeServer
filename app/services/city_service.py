"""
City service module.
Contains business logic related to the City model.
"""
from app.models import City

class CityService:
    @staticmethod
    def get_all_cities():
        """Get all cities with additional information"""
        cities = City.get_all()
        return cities
    
    @staticmethod
    def get_city_details(city_id):
        """Get detailed information about a city"""
        city = City.get_by_id(city_id)
        if not city:
            return None
        return city
