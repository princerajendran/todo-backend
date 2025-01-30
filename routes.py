from aiohttp import web
from handlers.auth_handlers import register, login
from handlers.todo_handlers import create_todo, list_todos, get_todo, update_todo, delete_todo

def setup_routes(app, cors):
    # Auth routes
    cors.add(app.router.add_post("/register/", register))
    cors.add(app.router.add_post("/login/", login))

    # Todo routes
    cors.add(app.router.add_post("/todos/", create_todo))
    cors.add(app.router.add_get("/todos/", list_todos))
    cors.add(app.router.add_get("/todos/{id}/", get_todo))
    cors.add(app.router.add_put("/todos/{id}/", update_todo))
    cors.add(app.router.add_delete("/todos/{id}/", delete_todo))

