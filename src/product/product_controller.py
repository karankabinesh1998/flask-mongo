from bson import ObjectId
from flask import Blueprint, jsonify , request
from src.product.product_service import find_products,insert_product,find_product_by_id,delete_product_by_id,update_product
from error_handler import throw_error
from src.constants.route_constants import APP_PRODUCT_SIGNATURE , APP_PRODUCT_SIGNATURE_BY_ID
import flask
product = Blueprint('product', __name__)

@product.route(APP_PRODUCT_SIGNATURE,methods=['GET'])
def fetch_all_product():
    try:
        # Read query parameters from the request
        query_params = request.args.to_dict()
        limit = query_params.get("limit",10)
        offset = query_params.get("offset",0)
        product = find_products({},int(limit),int(offset))
        return flask.jsonify(product)
    except Exception as e:
        return throw_error(e)

@product.route(APP_PRODUCT_SIGNATURE, methods=['POST'])
def add_product():
    try:
        if not request.is_json:
            return jsonify({'error': 'JSON data is required in request body'}), 400
        # Get product data from request body
        product_data = request.json
        # Check if required fields are present
        if 'name' not in product_data or 'description' not in product_data:
            return jsonify({'error': 'Name and Description are required fields'}), 400
        # Insert product into database
        product_id = insert_product(product_data)
        # Convert ObjectId to string before returning
        product_id_str = str(product_id)
        return jsonify({'message': 'Product added successfully', 'product_id': product_id_str}), 201
    except Exception as e:
        return throw_error(e)

@product.route(APP_PRODUCT_SIGNATURE_BY_ID, methods=['GET'])
def fetch_product_by_id(product_id):
    try:
        if product_id is None:
            return jsonify({'error': 'Product ID is required'}), 400
        product = find_product_by_id(product_id)
        if product is None:
            return jsonify({'error': 'Product not found'}), 400
        return flask.jsonify(product)
    except Exception as e:
        return throw_error(e)

@product.route(APP_PRODUCT_SIGNATURE_BY_ID, methods=['PUT'])
def update_product_by_id(product_id):
    try:
        # Check if product_id is provided
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400
        # Check if request contains JSON data
        if not request.is_json:
            return jsonify({'error': 'JSON data is required in request body'}), 400
        # Read updated product data from request body
        updated_data = request.json
        
        # Update the product
        result = update_product({'_id': ObjectId(product_id)}, updated_data)
        
        # Check if the product was updated successfully
        if result > 0:
            return jsonify({'message': 'Product updated successfully'}), 200
        else:
            return jsonify({'error': 'Product not found or no changes were made'}), 404
    except Exception as e:
        return throw_error(e)

@product.route(APP_PRODUCT_SIGNATURE_BY_ID, methods=['DELETE'])
def delete_product(product_id):
    try:
        if product_id is None:
            return jsonify({'error': 'Product ID is required'}), 400
        # Call the delete function from the product service
        deleted_count = delete_product_by_id(product_id)
        if deleted_count:
            return jsonify({'message': 'Product deleted successfully'}), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return throw_error(e)