from flask import Blueprint, request, jsonify
from src.auth._jwt import generate_jwt_token, decode_jwt_token
from src.auth.auth_service import authenticate_user,create_user
# from constants.route_constants import APP_AUTH_LOGIN

auth = Blueprint('auth', __name__)

@auth.route('/api/v1/auth/login', methods=['POST'])
def login():
    # create_user()
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = authenticate_user(email, password)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401