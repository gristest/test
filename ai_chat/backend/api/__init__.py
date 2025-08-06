


from flask import Flask
from flask_cors import CORS
from models import db
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configure database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "../../data.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from .routes import conversation_routes
    app.register_blueprint(conversation_routes)
    
    return app


