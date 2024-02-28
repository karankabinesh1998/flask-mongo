from flask import Flask
from config.constants import SERVER_PORT,SECRET_KEY
from flask_jwt_extended import JWTManager
from datetime import timedelta
from src.middleware.auth_middleware import authenticate_user
app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.config["JWT_SECRET_KEY"] = SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

JWTManager(app)
from src.product import product_controller 
from src.auth import auth_controller

app.register_blueprint(product_controller.product)
app.register_blueprint(auth_controller.auth)

# Middleware
app.before_request_funcs = {
    'product': [authenticate_user]
}

if __name__ == '__main__':
    app.run(debug=True, port=SERVER_PORT)
