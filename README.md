# FastAPI C.R.U.D. API: My Backend Learning Lab

This repository is my "public sketchbook" for mastering modern backend development with Python. It documents my journey from a simple in-memory `list` to a persistent, SQL-backed API.

This project is the foundational "bootcamp" I completed before starting my first major portfolio piece (a full-scale Social Media API).

### Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **PostgreSQL**: Advanced open source relational database.
- **SQLModel**: Library for interacting with SQL databases from Python code, with Python objects.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Uvicorn**: ASGI web server implementation for Python.

-----

## Core Concepts I Mastered

This project was a deep dive into the fundamentals of all backend engineering.

  * **Full C.R.U.D. API:** Built a complete set of endpoints for Create, Read, Update, and Delete operations.
  * **Persistent SQL Database:** Migrated the entire API from a temporary in-memory `list` to a permanent **PostgreSQL** database.
  * **`SQLModel` & `SQLAlchemy`:** Used modern, type-safe Python to define database tables, create the engine, and manage data.
  * **FastAPI `Depends`:** Mastered Dependency Injection to create a clean, reusable `get_session()` function.
  * **Modern Lifespan:** Replaced the deprecated `@on_event` with the modern `lifespan` context manager to create database tables on startup.
  * **Professional Error Handling:** Learned the crucial "Find-First, Check-First" pattern. Instead of `try...except`, I now check if an item is `None` before acting on it, returning a proper `404 Not Found` `HTTPException`.
  * **Path & Body Validation:** Used `Pydantic` models to automatically validate incoming `POST` and `PUT` request bodies.

-----

## My Biggest "Aha!" Moments & Debugging Journey

This project taught me that debugging is the *real* job. I fixed several real-world bugs:

1.  **The Anaconda `sqlite3` Bug:** My initial build with SQLite failed due to a `Symbol not found: _sqlite3_enable_load_extension` error. This is a common bug with Anaconda Python on macOS.

      * **The Fix:** Instead of wasting hours fixing a broken tool, I pivoted. I upgraded the *entire project* to **PostgreSQL**, which is the production-grade database I planned to learn anyway. This was a massive, real-world lesson.

2.  **The "Translator" Bug:** My app then crashed with `ModuleNotFoundError: No module named 'psycopg2'`.

      * **The Fix:** I learned that while `Postgres.app` is the *server*, my Python code needs a *translator* (a driver) to talk to it. `pip install psycopg2-binary` was the fix.

3.  **The "Check-First" Logic Bug:** My `DELETE` and `UPDATE` endpoints were crashing with a `500 Server Error` when I tried to act on an ID that didn't exist.

      * **The Fix:** I learned the difference between list (`IndexError`) and SQL (`None`) error handling. I refactored all my endpoints to use the "Find-First, Check-First" pattern:
        ```python
        blog_to_update = session.exec(select(Blog).where(Blog.id == id)).first()
        if not blog_to_update:
            raise HTTPException(status_code=404, detail="Not found")
        # ... now it's safe to update
        ```

### How to Run This Project

1.  **Clone the repo:**
    ```bash
    git clone https://github.com/Divij-8/FastAPI.git
    cd fastapi
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn sqlmodel psycopg2-binary
    ```
4.  **Run the app (make sure Postgres.app is running!):**
    ```bash
    uvicorn main:app --reload
    ```
5.  **Open the docs** and test the API: `http://127.0.0.1:8000/docs`

### Next Steps

With this C.R.U.D. bootcamp complete, I am now ready to build production-grade projects. My next step is applying these skills to my first major portfolio piece.

* **Portfolio Project 1: The Social Media API**
    * I will use these C.R.U.D. skills as a foundation to build a full-scale API with all the features of a "production-ready" service, including:
    * **JWT Authentication & Security** (for user login/registration).
    * **A Professional Multi-File Structure** (`routers/`, `models/`, `services/`, etc.).
    * **Complex `many-to-many` SQL relationships** (for `followers` and `likes`).
    * **A full `pytest` test suite.**

