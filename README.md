# FastAPI C.R.U.D. API: My Backend Learning Lab

This repository documents my journey in mastering professional, production-grade API development. It's the foundational "bootcamp" project I built from scratch to learn the core principles of backend engineering before starting my first major portfolio piece.

The project "Blog API" evolved from a simple in-memory list to a persistent, secure, and robust SQL-backed API built on modern engineering principles.

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **SQLModel**: Library for interacting with SQL databases from Python code, combining SQLAlchemy and Pydantic for type-safe database operations.
- **PostgreSQL**: Advanced open source relational database used for persistent data storage.
- **python-dotenv**: Library for loading environment variables from a .env file.
- **AnyIO**: Asynchronous networking and concurrency library for Python, used for running synchronous database operations in an async context.
- **Uvicorn**: ASGI web server implementation for Python.

---

## Core Concepts Mastered

This project was a deep dive into building APIs the *right way*, focusing on security, scalability, and clean code.

### 1. Schema Separation (Pydantic Models)

This was the most critical concept. I learned *why* you never use your database model (`Blog`) as your API schema. I implemented separate models for each operation to build a secure and clear data contract:

- **`BlogCreate`**: For `POST` requests. This schema has no `id` field, guaranteeing a user cannot force an `id` on creation.
- **`BlogRead`**: For `GET` requests. This schema *guarantees* an `id` is always returned to the client.
- **`BlogUpdate`**: For `PUT`/`PATCH` requests. All fields are `Optional`, allowing for true partial updates.

### 2. True Partial Updates (PATCH Logic)

I implemented a `PUT` endpoint that functions as a `PATCH`. It only updates fields that are *explicitly* provided by the user (e.g., `if blog_in.title is not None:`), rather than forcing the user to resend the entire object. This is a critical feature for a good user experience.

### 3. Dependency Injection (`Depends`)

I mastered FastAPI's core design pattern by creating a reusable `get_session()` dependency. This keeps all endpoints clean, DRY (Don't Repeat Yourself), and easy to test, as the session management logic is centralized in one place.

### 4. Settings & Environment Management

I secured all database credentials by moving them out of the code and into a `.env` file. This is a non-negotiable professional standard. I used `pydantic-settings` to load and validate these environment variables safely at startup.

### 5. Modern App Lifecycle (`lifespan`)

I upgraded from the deprecated `@on_event("startup")` to the modern `asynccontextmanager` (`lifespan`). This function now correctly runs the synchronous `SQLModel.metadata.create_all(engine)` in a separate thread using `anyio.to_thread.run_sync()`, preventing the async event loop from being blocked.

### 6. Professional Error Handling

I learned the difference between `list` and `SQL` error handling. I refactored all endpoints to use the "Find-First, Check-First" pattern, which is more robust and readable than `try...except`.

```python
# The "Find-First, Check-First" Pattern
blog = session.get(Blog, blog_id)
if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, ...)
# ... now it's safe to use 'blog'
```

## How to Run This Project

### Clone the repo:

```bash
git clone https://github.com/Divij-8/FastAPI.git
cd FastAPI
```

### Create a .env file in the root directory. (This file should be in your .gitignore).

```
DATABASE_URL="postgresql://your_mac_username@localhost:5432/postgres"
```

### Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install all dependencies:

```bash
pip install "fastapi[all]" sqlmodel psycopg2-binary pydantic-settings python-dotenv anyio
```

### Run the app (Make sure your Postgres.app server is running!):

```bash
uvicorn app.main:app --reload
```

Open the docs and test the live API: http://127.0.0.1:8000/docs

## Next Steps

With this C.R.U.D. bootcamp complete, I am now building my first major portfolio project: a full-scale Social Media API that will use this exact professional structure as its foundation.
