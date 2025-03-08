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
        
        # Add any additional business logic or data enrichment here
        # For example, you might want to add the count of simulations for each city
        
        return cities
    
    @staticmethod
    def get_city_details(city_id):
        """Get detailed information about a city"""
        city = City.get_by_id(city_id)
        if not city:
            return None
        
        # Add any additional business logic or data enrichment here
        # For example, adding statistical information about the city
        
        return city
    
    @staticmethod
    def create_city(name):
        """Create a new city with validation"""
        # Validate city name
        if not name or len(name.strip()) == 0:
            raise ValueError("City name cannot be empty")
        
        # Additional validation can be added here
        
        # Create the city
        return City.create(name.strip())
