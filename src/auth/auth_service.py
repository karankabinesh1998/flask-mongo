from database.db import connect_to_mongodb, close_mongodb_connection
import uuid
from flask_jwt_extended import create_access_token
from datetime import datetime,date
from bson.objectid import ObjectId
from pymongo.results import UpdateResult
from config.constants import MAX_TOKENS
# # Function to encrypt password
# def encrypt_password(password):
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed_password

def get_days_between_dates(date_one, date_two):
    """
    Returns day difference between two given dates
    """
    day_difference = 0
    if isinstance(date_one, date) and isinstance(date_two, date):
        day_difference = abs((date_one - date_two).days)
    return day_difference

# # Function to verify password
def verify_password(plain_password, hashed_password):
      return plain_password == hashed_password
#     return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)



# Authenticate user by email and password
def authenticate_user(email, password):
    client = connect_to_mongodb()
    try:
        max_tokens_count = int(MAX_TOKENS)
        user_from_db = client.portal_db.users.find_one({'email': email})
        if user_from_db and verify_password(password, user_from_db['password']):
            identity = str(uuid.uuid4())
            access_token = create_access_token(identity=identity)
            existing_tokens = user_from_db.get('tokens', [])
            valid_existing_tokens = list(filter(lambda token_details: get_days_between_dates(
                token_details.get('updated_at'), datetime.utcnow()) <= 1, existing_tokens))
            if len(valid_existing_tokens) >= max_tokens_count:
                valid_existing_tokens.sort(
                    reverse=True, key=lambda token: token['updated_at'])
                valid_existing_tokens = valid_existing_tokens[:max_tokens_count - 1]
            valid_existing_tokens.append({'token': identity, 'updated_at': datetime.utcnow()})
            user_from_db['_id'] = str(user_from_db['_id'])  # Convert ObjectId to string
            update_user_token(user_from_db['_id'], valid_existing_tokens)
            return {"user":user_from_db,"access_token":access_token}
        else:
            return None
    finally:
        close_mongodb_connection(client)

def get_user_by_token(token):
    """
    Given a token, return a user with that session.
    """
    try:
        client = connect_to_mongodb()
        response = client.portal_db.users.find_one({'tokens.token': token})
        return response
    except Exception as e:
        return None

def update_user_token(user_id, tokens):
    """
    Updated user's tokens in database to handle sessions
    """
    try:
        client = connect_to_mongodb()
        user_object_id = user_id
        if isinstance(user_object_id, str):
            user_object_id = ObjectId(user_object_id)
        response = client.portal_db.users.update_one({'_id': user_object_id}, {
            '$set': {'tokens': tokens}})
        # print(user_id, tokens, 'update')
        if type(response) is UpdateResult:
            return True
        else:
            return response
    except Exception as e:
        return e

# Create new user
def create_user():
    client = connect_to_mongodb()
    try:
        # # Check if user already exists
        # if client.portal_db.users.find_one({'email': email}):
        #     return None  # User already exists

        # Create user document
        user_data = {
            'firstName': 'karan',
            'lastName': 'kumar',
            'email': 'karankabinesh@gmail.com',
            'mobile': '9080050803',
            'alternateMobile': '',
            'gender': 'male',
            'password': '12345',  # Note: You should hash the password before storing it
            'roles': 'super-admin',
            'status': 'active'
            # Additional fields if needed
        }
         # Hash the password
        # user_data['password'] = encrypt_password(user_data['password'])


        # Insert user document into the database
        result = client.portal_db.users.insert_one(user_data)
        return result.inserted_id
    finally:
        close_mongodb_connection(client)

# Logout user (dummy function, as JWT tokens are stateless)
def logout_user(user_id):
    pass  # No action required for JWT-based authentication
