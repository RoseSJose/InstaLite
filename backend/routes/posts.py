from flask import Blueprint, request, jsonify, current_app
from models import db, Post
from utils.auth_utils import decode_token
from utils.image_utils import save_image

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/upload_post', methods=['POST'])
def upload_post():
    token = request.headers.get('Authorization')
    user_id = decode_token(token)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    image = request.files['image']
    caption = request.form.get('caption')
    image_url = save_image(image, current_app.config['UPLOAD_FOLDER'])
    post = Post(user_id=user_id, image_url=image_url, caption=caption)
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post uploaded!'})

@posts_bp.route('/delete_post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    token = request.headers.get('Authorization')
    user_id = decode_token(token)
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    post = Post.query.get(post_id)
    if not post or post.user_id != user_id:
        return jsonify({'error': 'Post not found or unauthorized'}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'})