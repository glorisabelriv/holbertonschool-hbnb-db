from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt
from Model.amenity import Amenity
from datab import db
from Model.user import User
from Persistence.DataManager import DataManager

amenity_bp = Blueprint('amenity_bp', __name__)
data_manager = DataManager()

# POST /amenities
@amenity_bp.route('/amenities', methods=['POST'], endpoint='create_amenity')
@jwt_required
def create_amenity():
   user = User.query.get(get_jwt_identity())
   if not user.is_admin:
        abort(403, description="Admin rights required")

   if not request.json or not 'name' in request.json:
        abort(400, description="Missing required fields")

   name = request.json['name']

   existing_amenity = Amenity.query.filter_by(name=name).first()

   if existing_amenity:
        abort(409, description="Amenity name already exists")

   amenity = Amenity(name=name)
   db.session.add(amenity)
   db.session.commit()
   return jsonify(amenity.to_dict()), 201

#GET ALL AMENITIES
@amenity_bp.route('/amenities', methods=['GET'], endpoint='get_amenities')
def get_amenities():
    amenities = Amenity.query.all()
    return jsonify([amenities.to_dict() for amenities in amenities]), 200

#GET AMENITY BY ID
@amenity_bp.route('/amenities/<amenity_id>', methods=['GET'], endpoint='get_amenity')
def get_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")
    return jsonify(amenity.to_dict()), 200

#PUT /amenities/<amenity_id>
@amenity_bp.route('/amenities/<amenity_id>', methods=['PUT'], endpoint='update_amenity')
def update_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")

    if not request.json:
        abort(400, description="Missing required fields")

    new_name = request.json.get('name')
    if new_name and new_name != amenity.name:
        existing_amenity = Amenity.query.filter(
            Amenity.name == new_name, Amenity.id != amenity_id).first()
        if existing_amenity:
            abort(409, description="Amenity name already exists")
        amenity.name = new_name

    db.session.commit()
    return jsonify(amenity.to_dict()), 200

#DELETE /amenities/<amenity_id>
@amenity_bp.route('/amenities/<amenity_id>', methods=['DELETE'], endpoint='delete_amenity')
@jwt_required
def delete_amenity(amenity_id):
    user = User.query.get(get_jwt_identity())
    if not user.is_admin:
        abort(403, description="Admin rights required")
    amenity = Amenity.query.get(amenity_id)
    db.session.delete(amenity)
    db.session.commit()
    return '', 204
