from flask import Flask
import os
from src.auth import auth
from src.database import db
from flask_jwt_extended import JWTManager

from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    CORS(app)
    app.debug = True

    my_env = os.getenv("FLASK_ENV")
    if(my_env=="development"):
        uri = "postgresql://postgres:Foluke89@localhost/CaptainUN"
    else:
        uri = os.getenv("DATABASE_URL")
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)

    if test_config is None:
       app.config.from_mapping(
           SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=uri,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
       ) 

    else:
        app.config.from_mapping(test_config)
    
    db.app=app
    db.init_app(app)

    JWTManager(app)
    
    app.register_blueprint(auth)
    
    return app