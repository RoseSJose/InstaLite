from flask import Blueprint, request, jsonify
from models import db, Like
from utils.auth_utils import decode_token

like_bp = Blueprint('like', __name__)

@like_bp.route('/like', methods=['POST'])
def like_post():
    token = request.headers.get('Authorization')
    user_id = decode_token(token)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    post_id = data.get('post_id')
    if not post_id:
        return jsonify({'error': 'No post_id'}), 400
    existing = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'message': 'Unliked'})
    like = Like(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Liked'})

@like_bp.route('/likes/<int:post_id>', methods=['GET'])
def get_likes(post_id):
    count = Like.query.filter_by(post_id=post_id).count()
    return jsonify({'likes': count})