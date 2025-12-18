from flask import Blueprint, request, jsonify
from models import db, Post, Follow, User
from utils.auth_utils import decode_token

feed_bp = Blueprint('feed', __name__)

@feed_bp.route('/feed', methods=['GET'])
def feed():
    token = request.headers.get('Authorization')
    user_id = decode_token(token)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    followed = db.session.query(Follow.followed_id).filter_by(follower_id=user_id)
    followed_ids = [f[0] for f in followed]  # extract IDs from tuples

    # Add the current user's own ID
    followed_ids.append(user_id)
    posts = Post.query.filter(Post.user_id.in_(followed_ids)).order_by(Post.created_at.desc()).all()

    return jsonify([{
        'id': p.id,
        'user_id': p.user_id,
        'username': User.query.get(p.user_id).username,
        'image_url': p.image_url,
        'caption': p.caption,
        'created_at': p.created_at
    } for p in posts])