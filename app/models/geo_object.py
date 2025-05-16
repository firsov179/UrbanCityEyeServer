from app import db

class GeoObject:
    @staticmethod
    def get_by_simulation(simulation_id, bbox=None):
        """Get geographic objects for a specific simulation with optional bounding box"""
        params = [simulation_id]
        
        query = """
            SELECT g.id, g.name, g.role, g.description, 
                   ST_AsGeoJSON(g.location) as geometry
            FROM GeoObject g
            JOIN GeoObjectSimulation gs ON g.id = gs.geo_object_id
            WHERE gs.simulation_id = %s
        """
        
        if bbox:
            minx, miny, maxx, maxy = bbox
            query += " AND ST_Intersects(g.location, ST_MakeEnvelope(%s, %s, %s, %s, 4326))"
            params.extend([minx, miny, maxx, maxy])
        
        return db.execute_query(query, params)
    
    @staticmethod
    def get_by_id(geo_object_id):
        """Get geographic object by ID"""
        query = """
            SELECT g.id, g.name, g.role, g.description, 
                   ST_AsGeoJSON(g.location) as geometry
            FROM GeoObject g
            WHERE g.id = %s
        """
        return db.execute_query(query, (geo_object_id,), fetchone=True)

