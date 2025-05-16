from app.routes.city_routes import city_bp
from app.routes.simulation_routes import simulation_bp
from app.routes.geo_object_routes import geo_object_bp

all_blueprints = [
    (city_bp, '/api/cities'),
    (simulation_bp, '/api/simulations'),
    (geo_object_bp, '/api/geo-objects')
]

def register_blueprints(app):
    """Register all blueprints with the Flask application"""
    for blueprint, url_prefix in all_blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
