from dotenv import load_dotenv
import os

load_dotenv()


class RedisConfig:
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT"))
    REDIS_DATABASE = int(os.getenv("REDIS_DATABASE"))
