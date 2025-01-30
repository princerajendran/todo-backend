from aiohttp import web
import bcrypt
import jwt
from database import async_session, User
from sqlalchemy.future import select
from settings import SECRET_KEY, JWT_ALGORITHM  # Import from settings
from datetime import datetime, timedelta


# Register User
async def register(request):
    try:
        data = await request.json()
        if "username" not in data or "password" not in data:
            return web.json_response({"error": "Missing required fields"}, status=400)

        username = data["username"]
        password = data["password"]

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        new_user = User(username=username, hashed_password=hashed_password.decode("utf-8"))

        async with async_session() as session:
            session.add(new_user)
            await session.commit()

        return web.json_response({"message": "User created successfully"}, status=201)

    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)


# Login User (JWT Token)
async def login(request):
    try:
        data = await request.json()
        if "username" not in data or "password" not in data:
            return web.json_response({"error": "Missing required fields"}, status=400)

        username = data["username"]
        password = data["password"]

        async with async_session() as session:
            result = await session.execute(select(User).filter_by(username=username))
            user = result.scalars().first()

            if user and bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8")):
                # Convert user ID to string
                # payload = {"sub": str(user.id)}
                payload = {
                    "sub": str(user.id),  # Convert user ID to string
                    "exp": datetime.utcnow() + timedelta(hours=1)  # Optional: Add expiration
                }
                token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
                return web.json_response({"token": token})

        return web.json_response({"error": "Invalid credentials"}, status=401)

    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)
