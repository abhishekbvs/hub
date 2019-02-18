from flask import Flask, Blueprint
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restplus import Api

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app, 
    version='0.0.1', 
    title="Switch API", 
    description="Switch services API listing.", 
    default='General')

from app import routes, farer, events, models, reg