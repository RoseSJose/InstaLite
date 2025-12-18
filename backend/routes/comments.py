from flask import Blueprint, request, jsonify
from models import db, Comment, User
from utils.auth_utils import decode_token

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/comment', methods=['POST'])
def add_comment():
    token = request.headers.get('Authorization')
    user_id = decode_token(token)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    post_id = data.get('post_id')
    text = data.get('text')
    if not post_id or not text:
        return jsonify({'error': 'Missing data'}), 400
    comment = Comment(user_id=user_id, post_id=post_id, text=text)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added'})

@comment_bp.route('/comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()
    return jsonify([{
        'id': c.id,
        'user_id': c.user_id,
        'username': User.query.get(c.user_id).username,
        'text': c.text,
        'created_at': c.created_at
    } for c in comments])