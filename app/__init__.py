from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.database.db_manager import DBManager

db = DBManager()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(config_class)

    CORS(app)

    db.init_app(app)

    from app.routes.city_routes import city_bp
    from app.routes.simulation_routes import simulation_bp
    from app.routes.geo_object_routes import geo_object_bp
    
    app.register_blueprint(city_bp, url_prefix='/api/cities')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulations')
    app.register_blueprint(geo_object_bp, url_prefix='/api/geo-objects')
    
    return app
