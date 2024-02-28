from flask_jwt_extended import get_jwt_identity, jwt_required
from src.auth.auth_service import get_user_by_token
from flask import  abort, request, jsonify, make_response
from src.middleware.auth_constants import auth_constants

@jwt_required()
def authenticate():
    user_identity = get_jwt_identity()
    user = get_user_by_token(user_identity)
    if not user:
        response = make_response(jsonify(message="Invalid auth token"), 401)
        return abort(response)
    setattr(request, 'user', user)
    setattr(request, 'user_identity', user_identity)
    return

def authenticate_user():
    if skip_urls(request.url_rule.rule):
        return
    authenticate()

def skip_urls(path):
    return path in auth_constants.skip_urls