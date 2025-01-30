from aiohttp import web
import jwt
from settings import SECRET_KEY, JWT_ALGORITHM  # Import from settings

# Middleware for checking JWT token
@web.middleware
async def jwt_middleware(request, handler):
    # Bypass auth for /register/, /login/, GET /todos/, and GET /todos/{id}/ routes
    if request.path == '/register/' or request.path == '/login/' or (
            request.method == 'GET' and (request.path == '/todos/' or request.path.startswith('/todos/'))):
        return await handler(request)

    # Bypass auth for OPTIONS requests (preflight)
    if request.method == "OPTIONS":
        return await handler(request)

    token = request.headers.get("Authorization")

    if token:
        try:
            token = token.split(" ")[1]  # Extract token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            request['user_id'] = payload['sub']
        except jwt.ExpiredSignatureError:
            return web.json_response({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return web.json_response({"error": "Invalid token"}, status=401)
    else:
        # Token is missing, return error
        return web.json_response({"error": "Authentication token required"}, status=401)

    return await handler(request)