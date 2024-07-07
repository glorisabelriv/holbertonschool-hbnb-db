from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt
from Model.user import User
from Persistence.DataManager import DataManager


user_bp = Blueprint('user_bp', __name__)
data_manager = DataManager()


@user_bp.route('/users/login', methods=['POST'])
def login():
    if not request.json or 'email' not in request.json or 'password' not in request.json:
        abort(400, description="Missing required fields")

    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    if user is None:
        abort(401, description="User not found")

    if not user.check_password(password):
        abort(401, description="Invalid password")


    return jsonify({"msg": "Login was succeddfuk"}), 200



#POST /users
@user_bp.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'email' in request.json:
        abort(400, description="Missing requirement fields")

    email = request.json['email']
    first_name = request.json.get('first_name', '')
    last_name = request.json.get('last_name', '')
    password = request.json.get('password', '')

    if '@' not in email:
        abort(400, description="Invalid email format")

    existing_users = [user for user in data_manager.storage.get(
		'User', {}).values() if user.email == email]
    if existing_users:
        abort(409, description="Email already exists")


    user = User(email=email, first_name=first_name, last_name=last_name)
    data_manager.save(user)

    return jsonify(user.to_dict()), 201

#POST /users/login
@user_bp.route('/users/<user_id>/promote', methods=['POST'])
@jwt_required()
def promote_user(user_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    user.is_admin = True
    user.save()
    return jsonify(user.to_dict()), 200

#GET /users
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = [user.to_dict()
             for user in data_manager.storage.get('User', {}).values()]
    return jsonify(users), 200

#GET /users/<user_id>
@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = data_manager.get(user_id, 'User')
    if user is None:
        abort(404, description="User not found")
    return jsonify(user.to_dict()), 200

#PUT /users/<user_id>
@user_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    claims = get_jwt()
    if not claims.get('is_admin') and get_jwt_identity != user_id:
        return jsonify({"msg": "Administration rights required"}), 403
    
    user = data_manager.get(user_id, 'User')
    if user is None:
        abort(404, description='User not found')

    if not request.json:
        abort(400, description="Missing required fields")

    user.email = request.json.get('email', user.email)
    user.first_name = request.json.get('first_name', user.first_name)
    user.last_name = request.json.get('last_name', user.last_name)

    data_manager.update(user)
    return jsonify(user.to_dict()), 200

#DELETE /users/<user_id>
@user_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = data_manager.get(user_id, 'User')
    if user is None:
        abort(404, description="User not found")
    data_manager.delete(user_id, 'User')
    return '', 204
