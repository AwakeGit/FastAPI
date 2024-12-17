import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql+asyncpg://{os.environ.get('DB_USER_FASTAPI')}:{os.environ.get('DB_PASSWORD_FASTAPI')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME_FASTAPI')}"

