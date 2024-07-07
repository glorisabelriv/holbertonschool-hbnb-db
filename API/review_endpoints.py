from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required
from Model.review import Review
from datab import db
from Persistence.DataManager import DataManager

review_bp = Blueprint('review_bp', __name__)
data_manager = DataManager()

# POST /places/<place_id>/reviews
@review_bp.route('/places/<place_id>/reviews', methods=['POST'], endpoint='create_review')
@jwt_required()
def create_review(place_id):
    if not request.json or not all(key in request.json for key in ('user_id', 'rating', 'comment')):
        abort(400, description="Missing required fields")

    user_id = request.json['user_id']
    rating = request.json['rating']
    comment = request.json['comment']

    if not (1 <= rating <= 5):
        abort(400, description="Rating must be between 1 and 5")

    review = Review(place_id=place_id, user_id=user_id, rating=rating, comment=comment)
    db.session.add(review)
    db.session.commit()

    return jsonify(review.to_dict()), 201

# GET /users/<user_id>/reviews
@review_bp.route('/users/<user_id>/reviews', methods=['GET'], endpoint='get_user_reviews')
@jwt_required()
def get_user_reviews(user_id):
    reviews = Review.query.filter_by(user_id=user_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200


# GET /places/<place_id>/reviews
@review_bp.route('/places/<place_id>/reviews', methods=['GET'], endpoint='get_place_reviews')
@jwt_required
def get_place_reviews(place_id):
    reviews = Review.query.filter_by(place_id=place_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200


# GET /reviews/<review_id>
@review_bp.route('/reviews/<review_id>', methods=['GET'], endpoint='get_review')
@jwt_required()
def get_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        abort(404, description="Review not found")
    return jsonify(review.to_dict()), 200

# PUT /reviews/<review_id>
@review_bp.route('/reviews/<review_id>', methods=['PUT'], endpoint='update_review')
@jwt_required
def update_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        abort(404, description="Review not found")

    if not request.json:
        abort(400, description="Missing required fields")

    review.rating = request.json.get('rating', review.rating)
    review.comment = request.json.get('comment', review.comment)

    if not (1 <= review.rating <= 5):
        abort(400, description="Rating must be between 1 and 5")

    db.session.commit()
    return jsonify(review.to_dict()), 200

# DELETE /reviews/<review_id>
@review_bp.route('/reviews/<review_id>', methods=['DELETE'], endpoint='delete_review')
@jwt_required()
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        abort(404, description="Review not found")
    db.session.delete(review)
    db.session.commit()
    return '', 204
