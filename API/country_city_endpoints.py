from flask import Blueprint, request, jsonify, abort
from Model.city import City
from Model.country import Country
from Model.user import User
from datab import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from Persistence.DataManager import DataManager

country_city_bp = Blueprint('country_bp', __name__,)
data_manager = DataManager()

# POST /countries
@country_city_bp.route('/countries', methods=['GET'])
def get_countries():
    countries = Country.query.all()
    return jsonify([countries.to_dict() for countries in countries]), 200

# POST /countries
@country_city_bp.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    country = Country.query.filter_by(code=country_code).first()
    if not country:
        abort(404, description="Country not found")
    return jsonify(country), 200

# POST /cities by country
@country_city_bp.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    if not Country.query.filter_by(code=country_code).first():
        abort(404, description="Country not found")
    cities = City.query.filter_by(country_code=country_code).all()
    cities_json = [city.to_dict() for city in cities]
    return jsonify(cities_json), 200

# POST /cities
@country_city_bp.route('/cities', methods=['POST'])
@jwt_required
def create_city():
    user = User.query.get(get_jwt_identity())
    if not user.is_admin:
        abort(403, description="Admin rights required")

    if not request.json or 'name' not in request.json or 'country_code' not in request.json:
        abort(400, "Missing required fields")

    name = request.json['name']
    country_code = request.json['country_code']

    if not data_manager.get(country_code, 'Country'):
        abort(400, "Invalid country code")

    existing_cities = City.query.filter_by(
        name=name, country_code=country_code).first()
    if existing_cities:
        abort(409, "City name already exists in this country")

    city = City(name=name, country_code=country_code)
    db.session.add(city)
    db.session.commit()

    return jsonify({"city_id": city.id, "city": city.to_dict()}), 201

# GET /cities
@country_city_bp.route('/cities', methods=['GET'])
def get_cities():
    cities = City.query.all()
    return jsonify(cities), 200

# GET /cities/<city_id>
@country_city_bp.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = City.query.get(city_id)
    if not city:
        abort(404, description="City not found")
    return jsonify(city.to_dict()), 200

# PUT /cities/<city_id>
@country_city_bp.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = City.query.get(city_id)
    if not city:
        abort(404, description="City not found")

    if not request.json:
        abort(400, description="Missing required fields")

    city.name = request.json.get('name', city.name)
    city.country_code = request.json.get('country_code', city.country_code)

    if not data_manager.get(city.country_code, 'Country'):
        abort(400, description="Invalid country code")

    db.session.commit()
    return jsonify(city.to_dict()), 200

# DELETE /cities/<city_id>
@country_city_bp.route('/cities/<city_id>', methods=['DELETE'])
@jwt_required
def delete_city(city_id):
    user = User.query.get(get_jwt_identity())
    if not user.is_admin:
        abort(403, description="Admin rights required")

    city = City.query.get(city_id)
    db.session.delete(city)
    db.session.commit()
    return '', 204
