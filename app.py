from aiohttp import web
from database import init_db
from middleware import jwt_middleware
from routes import setup_routes
import aiohttp_cors
from settings import CORS_ALLOWED_ORIGINS, APP_PORT, DEBUG  # Import from settings

# Create the aiohttp app
app = web.Application()

# CORS setup
cors = aiohttp_cors.setup(app, defaults={
    CORS_ALLOWED_ORIGINS: aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    ),
})

# Add middleware
app.middlewares.append(jwt_middleware)

# Setup routes
setup_routes(app, cors)  # Pass `cors` to the setup_routes function

# Startup procedure to initialize the database
async def startup(app):
    await init_db()

# Register startup event
app.on_startup.append(startup)

if __name__ == "__main__":
    web.run_app(app, port=APP_PORT)