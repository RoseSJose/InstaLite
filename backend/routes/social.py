from flask import Blueprint, request, jsonify
from models import db, User, Follow
from utils.auth_utils import decode_token

social_bp = Blueprint('social', __name__)

@social_bp.route('/follow', methods=['POST'])
def follow():
    token = request.headers.get('Authorization')
    user_id = decode_token(token)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    target_id = data.get('user_id')
    if not target_id or target_id == user_id:
        return jsonify({'error': 'Invalid user to follow'}), 400

    # Check if already following
    existing = Follow.query.filter_by(follower_id=user_id, followed_id=target_id).first()
    if existing:
        return jsonify({'message': 'Already following'}), 200

    follow = Follow(follower_id=user_id, followed_id=target_id)
    db.session.add(follow)
    db.session.commit()
    return jsonify({'message': 'Now following'}), 201

@social_bp.route('/unfollow', methods=['POST'])
def unfollow():
    token = request.headers.get('Authorization')
    user_id = decode_token(token)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    target_id = data.get('user_id')
    if not target_id or target_id == user_id:
        return jsonify({'error': 'Invalid user to unfollow'}), 400

    follow = Follow.query.filter_by(follower_id=user_id, followed_id=target_id).first()
    if not follow:
        return jsonify({'message': 'Not following'}), 200

    db.session.delete(follow)
    db.session.commit()
    return jsonify({'message': 'Unfollowed'}), 200

@social_bp.route('/followers/<int:user_id>', methods=['GET'])
def followers(user_id):
    followers = Follow.query.filter_by(followed_id=user_id).all()
    follower_ids = [f.follower_id for f in followers]
    return jsonify({'followers': follower_ids})

@social_bp.route('/following/<int:user_id>', methods=['GET'])
def following(user_id):
    following = Follow.query.filter_by(follower_id=user_id).all()
    followed_ids = [f.followed_id for f in following]
    return jsonify({'following': followed_ids})

@social_bp.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify({'users': [{'id': u.id, 'username': u.username} for u in users]})