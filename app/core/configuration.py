import os

APP_TITLE = os.getenv("APP_TITLE", "MY NEW API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_MONGO_URI = os.getenv("APP_MONGO_URI", "mongodb://user:password@localhost/db")
APP_MONGO_DB = os.getenv("APP_MONGO_DB", "db")
APP_GOOGLE_CLIENT_ID = os.getenv("APP_GOOGLE_CLIENT_ID", "")
APP_GOOGLE_CLIENT_SECRET = os.getenv("APP_GOOGLE_CLIENT_SECRET", "")
APP_SECRET_KEY_MIDDLEWARE = os.getenv("APP_SECRET_KEY_MIDDLEWARE", "my_secret_middleware_key")
APP_SECRET_TOKENS = os.getenv("APP_SECRET_TOKENS", "43e36b7672fadda3df4b158f414ce2b41d2dbb24b639727a1352760bf6133e73")
APP_TOKEN_ALGORITHM="HS256"