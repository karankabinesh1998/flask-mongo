from flask_jwt_extended import get_jwt_identity, jwt_required
from src.auth.auth_service import get_user_by_token
from flask import Response, abort, request, jsonify, make_response


@jwt_required()
def authenticate():
    user_identity = get_jwt_identity()
    print(user_identity,">>user_identity")
    user = get_user_by_token(user_identity)
    if not user:
        print('No user token exist')
        response = make_response(jsonify(message="Invalid auth token"), 401)
        return abort(response)
    setattr(request, 'user', user)
    setattr(request, 'user_identity', user_identity)
    return

def authenticate_user():
    authenticate()