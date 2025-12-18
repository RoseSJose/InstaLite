from flask import Blueprint, request, jsonify
from models import db, User, Post, Follow
from utils.auth_utils import decode_token

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization')
    user_id = decode_token(token)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    followers = Follow.query.filter_by(followed_id=user_id).count()
    following = Follow.query.filter_by(follower_id=user_id).count()
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'profile_pic': user.profile_pic,
        'posts': [{
            'id': p.id,
            'image_url': p.image_url,
            'caption': p.caption,
            'created_at': p.created_at
        } for p in posts],
        'followers': followers,
        'following': following
    })