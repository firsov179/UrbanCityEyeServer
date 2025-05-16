"""
Database manager module.
Provides functionality for connecting to and querying the PostgreSQL database.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app, g
import logging

class DBManager:
    def __init__(self):
        self.conn = None
        self.logger = logging.getLogger(__name__)
    
    def init_app(self, app):
        """Initialize with Flask app configuration"""
        app.teardown_appcontext(self.close_connection)
        
        @app.route('/api/healthcheck/db', methods=['GET'])
        def db_healthcheck():
            try:
                self.get_connection()
                return {'status': 'Database connection successful'}, 200
            except Exception as e:
                self.logger.error(f"Database connection failed: {str(e)}")
                return {'status': 'Database connection failed', 'error': str(e)}, 500
    
    def get_connection(self):
        """Get database connection"""
        if 'db' not in g:
            try:
                g.db = psycopg2.connect(
                    host=current_app.config['DB_HOST'],
                    port=current_app.config['DB_PORT'],
                    dbname=current_app.config['DB_NAME'],
                    user=current_app.config['DB_USER'],
                    password=current_app.config['DB_PASSWORD'],
                    cursor_factory=RealDictCursor
                )
                self.logger.debug("Database connection established")
            except Exception as e:
                self.logger.error(f"Error connecting to database: {str(e)}")
                raise
        return g.db
    
    def close_connection(self, e=None):
        """Close database connection"""
        db = g.pop('db', None)
        if db is not None:
            db.close()
            self.logger.debug("Database connection closed")
    
    def execute_query(self, query, params=None, fetchone=False):
        """Execute a database query and return results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            self.logger.debug(f"Executing query: {query} with params: {params}")
            cursor.execute(query, params or ())
            conn.commit()
            
            if cursor.description:
                if fetchone:
                    return cursor.fetchone()
                return cursor.fetchall()
            return None
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Query execution error: {str(e)}")
            raise
        finally:
            cursor.close()
    
    def execute_many(self, query, params_list):
        """Execute a query with multiple parameter sets"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            self.logger.debug(f"Executing many query: {query}")
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Query executemany error: {str(e)}")
            raise
        finally:
            cursor.close()
    
    def call_procedure(self, procedure_name, params=None):
        """Call a stored procedure in the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            param_placeholders = ', '.join(['%s'] * len(params)) if params else ''
            query = f"CALL {procedure_name}({param_placeholders})"
            
            self.logger.debug(f"Calling procedure: {query} with params: {params}")
            cursor.execute(query, params or ())
            conn.commit()
            
            if cursor.description:
                return cursor.fetchall()
            return None
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Procedure call error: {str(e)}")
            raise
        finally:
            cursor.close()
