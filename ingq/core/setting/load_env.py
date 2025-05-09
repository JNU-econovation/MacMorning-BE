import os

from dotenv import load_dotenv

load_dotenv()


# MySQL Setting(ingq/core/db_config.py)
MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME")

# ingq/db/database.py
DATABASE_URL = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB_NAME}"

# ingq/migration/env.py
DATABASE_URL_ALEMBIC = os.getenv("DATABASE_URL_ALEMBIC")

# Redis Setting(ingq/core/redis_config.py)
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_DATABASE = int(os.getenv("REDIS_DATABASE"))

# About Token(ingq/auth)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Crypto(ingq/user/utils/crypto.py)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# AWS S3 Setting
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

# CloudFront Domain
CLOUDFRONT_DOMAIN = os.getenv("CLOUDFRONT_DOMAIN")
