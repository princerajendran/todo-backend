import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todos.db")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "kROyqhkESBvw9sOAupyUEOuoCP3dPl0s7CFLW3fLKkOpPWzabHd9mH6hVPkPcRLH")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# CORS Configuration
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "*")

# Application Configuration
APP_PORT = int(os.getenv("APP_PORT", 8088))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
