import os
from dotenv import load_dotenv
from typing import Generator, List, Optional
from contextlib import asynccontextmanager
import anyio
from fastapi import FastAPI, HTTPException, Depends, status
from sqlmodel import SQLModel, Field, create_engine, Session, select

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the .env file. Did you create it?")


engine = create_engine(DATABASE_URL, echo=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up... creating database tables.")
    # Run sync SQLModel create_all inside a thread to avoid blocking
    await anyio.to_thread.run_sync(lambda: SQLModel.metadata.create_all(engine))
    print("Database tables created")
    yield 
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


# Dependency that provides a database session for each request
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# Models
class BlogBase(SQLModel):
    title: str
    body: str


class Blog(BlogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class BlogCreate(BlogBase):
    pass


class BlogRead(BlogBase):
    id: int


class BlogUpdate(SQLModel):
    title: Optional[str] = None
    body: Optional[str] = None


# CRUD endpoints
@app.post("/blogs", response_model=BlogRead, status_code=status.HTTP_201_CREATED)
def create_blog(blog_in: BlogCreate, session: Session = Depends(get_session)):
    blog = Blog.from_orm(blog_in)
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog


@app.get("/blogs", response_model=List[BlogRead])
def list_blogs(limit: int = 100, offset: int = 0, session: Session = Depends(get_session)):
    statement = select(Blog).offset(offset).limit(limit)
    blogs = session.exec(statement).all()
    return blogs


@app.get("/blogs/{blog_id}", response_model=BlogRead)
def read_blog(blog_id: int, session: Session = Depends(get_session)):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog id {blog_id} not found")
    return blog


@app.put("/blogs/{blog_id}", response_model=BlogRead)
def update_blog(blog_id: int, blog_in: BlogUpdate, session: Session = Depends(get_session)):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog id {blog_id} not found")
    if blog_in.title is not None:
        blog.title = blog_in.title
    if blog_in.body is not None:
        blog.body = blog_in.body
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog


@app.delete("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
def delete_blog(blog_id: int, session: Session = Depends(get_session)):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog id {blog_id} not found")
    session.delete(blog)
    session.commit()
    return {"status": "success", "message": f"Blog {blog_id} deleted"}

