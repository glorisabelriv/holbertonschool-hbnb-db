from flask import Flask
from flask_jwt_extended import JWTManager
from datab import db
import os
from API.user_endpoints import user_bp
from API.place_endpoints import place_bp
from API.review_endpoints import review_bp
from API.amenity_endpoints import amenity_bp
from API.country_city_endpoints import country_city_bp
import Model

app = Flask(__name__)


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'GloriHBNB' 


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


environment_config = DevelopmentConfig if os.environ.get(
    'ENV') == 'development' else ProductionConfig

app.config.from_object(environment_config)

db.init_app(app)
jwt = JWTManager(app)



@app.route('/')
def home():
    return 'Welcome to the holbertonbnb api'


app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(place_bp, url_prefix='/api')
app.register_blueprint(review_bp, url_prefix='/api')
app.register_blueprint(amenity_bp, url_prefix='/api')
app.register_blueprint(country_city_bp, url_prefix='/api')

with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
