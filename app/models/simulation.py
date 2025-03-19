from app import db

class Simulation:
    @staticmethod
    def get_all():
        """Get all simulations"""
        query = """
            SELECT s.id, s.year, c.name as city_name, m.name as mode_name
            FROM Simulation s
            JOIN City c ON s.city_id = c.id
            JOIN Mode m ON s.mode_id = m.id
        """
        return db.execute_query(query)
    
    @staticmethod
    def get_by_id(simulation_id):
        """Get simulation by ID"""
        query = """
            SELECT s.id, s.year, s.city_id, s.mode_id, c.name as city_name, m.name as mode_name
            FROM Simulation s
            JOIN City c ON s.city_id = c.id
            JOIN Mode m ON s.mode_id = m.id
            WHERE s.id = %s
        """
        return db.execute_query(query, (simulation_id,), fetchone=True)
    
    @staticmethod
    def get_by_city_year(city_id, year, mode_id):
        """Get simulation by city and year"""
        query = """
            SELECT s.id, s.year, s.city_id, s.mode_id, c.name as city_name, m.name as mode_name
            FROM Simulation s
            JOIN City c ON s.city_id = c.id
            JOIN Mode m ON s.mode_id = m.id
            WHERE s.city_id = %s AND s.year = %s AND s.mode_id = %s
        """
        return db.execute_query(query, (city_id, year, mode_id), fetchone=True)
    
    @staticmethod
    def get_years_by_city(city_id):
        """Get all available years for a city"""
        query = """
            SELECT DISTINCT year
            FROM Simulation
            WHERE city_id = %s
            ORDER BY year
        """
        result = db.execute_query(query, (city_id,))
        return [record['year'] for record in result]

    @staticmethod
    def get_modes():
        """Get all available modes"""
        query = """
            SELECT id
            FROM Mode
        """
        result = db.execute_query(query, ())
        return [record['id'] for record in result]


