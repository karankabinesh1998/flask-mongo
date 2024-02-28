APP_VERISON = '/v1'
APP_API = '/api'
APP_PRODUCT = '/product'
APP_ID = "/<string:product_id>"
APP_AUTH = "/auth"
APP_LOGIN = "/login"


# /api/v1/product
APP_PRODUCT_SIGNATURE = APP_API + APP_VERISON + APP_PRODUCT
# /api/v1/product/:id
APP_PRODUCT_SIGNATURE_BY_ID = APP_API + APP_VERISON + APP_PRODUCT + APP_ID

# /api/v1/auth/login
APP_AUTH_LOGIN = APP_API + APP_VERISON + APP_AUTH + APP_LOGIN