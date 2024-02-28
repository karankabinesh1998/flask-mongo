from database.db import connect_to_mongodb, close_mongodb_connection
from pymongo import DESCENDING
from bson import ObjectId  # Import ObjectId from bson library
from datetime import datetime,timezone

# Insert document into 'product' collection
def insert_product(product):
    client = connect_to_mongodb()
    product_to_save = {
        "name" : product["name"],
        "description" : product["description"],
        "is_active" : product.get("updated_by", True),
        "created_by": product.get("created_by", None),
        "updated_by": product.get("updated_by", None),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    try:
        client.portal_db.product.create_index([('name', 1)], unique=True)
        result = client.portal_db.product.insert_one(product_to_save)
        return result.inserted_id
    finally:
        close_mongodb_connection(client)

# Find documents in 'product' collection
def find_products(query, limit=10, offset=0):
    client = connect_to_mongodb()
    try:
        # Perform a separate query to get the total count of documents
        total_count = client.portal_db.product.count_documents(query)

        # Query to find products and paginate the results
        products_cursor = client.portal_db.product.find(query).sort("createdAt", DESCENDING).skip(offset).limit(limit)
        products_list = list(products_cursor)  # Convert cursor to list of documents
        
        # Convert ObjectId fields to strings in each document
        for product in products_list:
            product['_id'] = str(product['_id'])  # Convert _id field to string
            product['created_at'] = int(product['created_at'].timestamp())
            product['updated_at'] = int(product['updated_at'].timestamp())
        # Serialize the products list to JSON
        return {"total_count": total_count, "products": products_list}
    finally:
        close_mongodb_connection(client)



# Update document in 'product' collection
def update_product(query, update_data):
    client = connect_to_mongodb()
    try:
        result = client.portal_db.product.update_one(query, {"$set": update_data})
        return result.modified_count
    finally:
        close_mongodb_connection(client)


# Find document in 'product' collection by id
def find_product_by_id(product_id):
    client = connect_to_mongodb()
    try:
        # Convert product_id to ObjectId
        product_id = ObjectId(product_id)
        # Query to find the product by its _id
        query = {'_id': product_id}
        # Find the product document
        product = client.portal_db.product.find_one(query)
        
        # Convert ObjectId to string for JSON serialization
        if product:
            product['_id'] = str(product['_id'])
            product['created_at'] = int(product['created_at'].timestamp())
            product['updated_at'] = int(product['updated_at'].timestamp())
        return product if product else None
    finally:
        close_mongodb_connection(client)

# Delete document from 'product' collection by id
def delete_product_by_id(product_id):
    client = connect_to_mongodb()
    try:
        # Convert product_id to ObjectId
        product_id = ObjectId(product_id)
        # Query to find and delete the product by its _id
        query = {'_id': product_id}
        # Delete the product document
        result = client.portal_db.product.delete_one(query)
        return result.deleted_count
    finally:
        close_mongodb_connection(client)
