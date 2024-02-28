from flask import Blueprint, request, jsonify
from src.auth.auth_service import authenticate_user,create_user
from src.constants.route_constants import APP_AUTH_LOGIN,APP_USER
from error_handler import throw_error

auth = Blueprint('auth', __name__)

@auth.route(APP_AUTH_LOGIN, methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        user = authenticate_user(email, password)
        if user:
            return jsonify(user), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return throw_error(e)

@auth.route(APP_USER,methods=['POST'])
def create_user_data():
    try:
        if not request.is_json:
            return jsonify({'error': 'JSON data is required in request body'}), 400
        data = request.json
        user_id = create_user(data)
        user_id_str = str(user_id)
        return jsonify({'message': 'User added successfully', 'user_id': user_id_str}),201
    except Exception as e:
        return throw_error(e)