# Import blueprints for easy access from other parts of the application
from app.routes.city_routes import city_bp
from app.routes.simulation_routes import simulation_bp
from app.routes.geo_object_routes import geo_object_bp

# Define all blueprints that should be registered with the app
all_blueprints = [
    (city_bp, '/api/cities'),
    (simulation_bp, '/api/simulations'),
    (geo_object_bp, '/api/geo-objects')
]

# Function to register all blueprints
def register_blueprints(app):
    """Register all blueprints with the Flask application"""
    for blueprint, url_prefix in all_blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
