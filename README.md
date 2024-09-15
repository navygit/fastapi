
# FastAPI Task Manager

This project is a simple Task Manager: 
* It supports CRUD operations on users 
* It supports CRUD operations on tasks.

## How to Run the Project

### With Docker Compose:

1. Make sure Docker and Docker Compose are installed.
2. Clone the repository.
3. Run `docker-compose up --build`.
4. Open your browser and go to `http://localhost:8000/docs` to view the API documentation.

## Endpoints

* `GET /users/{user_id}` - Get user details.
* `POST /users/` - Create a new user.
* `POST /tasks/{user_id}/tasks` - Create a new task for a user.
* `POST /tasks/{user_id}/tasks/{task_id}/complete` - Complete a task for a user.

## Database Migrations

Database migrations are handled using Alembic. To create a new migration:

1. Run `alembic revision --autogenerate -m "migration message"`.
2. Run `alembic upgrade head`.
