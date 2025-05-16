from app import db

class City:
    @staticmethod
    def get_all():
        """Get all cities"""
        query = "SELECT id, name, name_ru FROM City"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_id(city_id):
        """Get city by ID"""
        query = "SELECT * FROM City WHERE id = %s"
        return db.execute_query(query, (city_id,), fetchone=True)
    
    @staticmethod
    def create(name):
        """Create a new city"""
        query = "INSERT INTO City (name) VALUES (%s) RETURNING id, name"
        return db.execute_query(query, (name,), fetchone=True)

