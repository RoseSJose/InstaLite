from flask import Blueprint, request, jsonify
from models import db, User
from utils.auth_utils import hash_password, check_password, generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username exists'}), 400
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hash_password(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password(data['password'], user.password_hash):
        used_id = user.id
        token = generate_token(user.id)
        return jsonify({'token': token, 'user_id': used_id})
    return jsonify({'error': 'Invalid credentials'}), 401