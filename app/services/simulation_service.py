"""
Simulation service module.
Contains business logic related to the Simulation model.
"""
from app.models import Simulation, City, GeoObject

class SimulationService:
    @staticmethod
    def get_simulation_details(simulation_id):
        """Get detailed information about a simulation"""
        simulation = Simulation.get_by_id(simulation_id)
        if not simulation:
            return None
        
        return simulation
    
    @staticmethod
    def get_timeline_for_city(city_id):
        """Get a timeline of all years for a city with additional metadata"""
        city = City.get_by_id(city_id)
        if not city:
            return None
        
        years = Simulation.get_years_by_city(city_id)
        modes = Simulation.get_modes()
        
        timeline = []
        for year in years:
            for mode in modes:
                simulation = Simulation.get_by_city_year(city_id, year, mode)
                if simulation:
                    timeline_entry = {
                        'year': year,
                        'simulation_id': simulation['id'],
                    }
                    timeline.append(timeline_entry)
                    break
        
        return {
            'city': city,
            'timeline': timeline
        }
