from aiohttp import web
from database import async_session, Todo
from sqlalchemy.future import select


# Create Todo
async def create_todo(request):
    user_id = request.get('user_id')  # Get user from JWT token

    if not user_id:
        return web.json_response({"error": "Unauthorized"}, status=401)

    try:
        data = await request.json()

        if "title" not in data or "description" not in data:
            return web.json_response({"error": "Missing required fields"}, status=400)

        new_todo = Todo(
            title=data["title"],
            description=data["description"],
            completed=data.get("completed", False),
            user_id=user_id
        )

        async with async_session() as session:
            session.add(new_todo)
            await session.commit()

        return web.json_response({"id": new_todo.id, "title": new_todo.title, "description": new_todo.description,
                                  "completed": new_todo.completed}, status=201)

    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)


# List Todos
async def list_todos(request):
    async with async_session() as session:
        result = await session.execute(select(Todo))
        todos = result.scalars().all()
        return web.json_response(
            [{"id": t.id, "title": t.title, "description": t.description, "completed": t.completed} for t in todos])


# Get a specific Todo by ID
async def get_todo(request):
    todo_id = int(request.match_info['id'])

    async with async_session() as session:
        result = await session.execute(select(Todo).filter_by(id=todo_id))
        todo = result.scalars().first()
        if todo:
            return web.json_response(
                {"id": todo.id, "title": todo.title, "description": todo.description, "completed": todo.completed})
        return web.json_response({"error": "Todo not found"}, status=404)


# Update a Todo
async def update_todo(request):
    todo_id = int(request.match_info['id'])
    user_id = request.get('user_id')  # Get user from JWT token

    if not user_id:
        return web.json_response({"error": "Unauthorized"}, status=401)

    try:
        data = await request.json()

        async with async_session() as session:
            result = await session.execute(select(Todo).filter_by(id=todo_id, user_id=user_id))
            todo = result.scalars().first()
            if not todo:
                return web.json_response({"error": "Todo not found"}, status=404)

            todo.title = data['title']
            todo.description = data.get('description', '')
            todo.completed = data.get('completed', todo.completed)

            await session.commit()
            return web.json_response(
                {"id": todo.id, "title": todo.title, "description": todo.description, "completed": todo.completed})

    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)


# Delete Todo
async def delete_todo(request):
    todo_id = int(request.match_info['id'])
    user_id = request.get('user_id')  # Get user from JWT token

    if not user_id:
        return web.json_response({"error": "Unauthorized"}, status=401)

    async with async_session() as session:
        result = await session.execute(select(Todo).filter_by(id=todo_id, user_id=user_id))
        todo = result.scalars().first()
        if not todo:
            return web.json_response({"error": "Todo not found"}, status=404)
        await session.delete(todo)
        await session.commit()
        return web.json_response({"message": "Todo deleted successfully"})
