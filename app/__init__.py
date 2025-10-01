from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv('.env')
# Inicializa as extensões (sem anexar à app ainda)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Cria e configura a instância do Flask."""
    
    app = Flask(__name__)
    
    # Configurações da Aplicação
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db) 
    
    with app.app_context():
        from app import models
    
    # 3. Registra Blueprints (rotas)
    from app.views import app as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
