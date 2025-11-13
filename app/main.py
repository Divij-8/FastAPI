from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, create_engine, Session, select
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up... creating database tables.")
    SQLModel.metadata.create_all(engine)
    print("Database tables created")
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

postgresql_url = "postgresql://divijmazumdar@localhost:5432/postgres"
engine = create_engine(postgresql_url)


def get_session():
    with Session(engine) as session:
        yield session


class Blog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title : str
    body : str


@app.post("/blog")
def create_blog(blog: Blog, session: Session = Depends(get_session)):
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog


@app.get("/blog/list")
def get_all_blogs(session: Session = Depends(get_session)):
    query = select(Blog)
    blogs = session.exec(query).all()
    return blogs


@app.get("/blog/{id}")
def show(id: int, session: Session = Depends(get_session)):
    #Fetch blog with id = id
    query = select(Blog).where(Blog.id == id)
    blog_post = session.exec(query).first()
    if not blog_post:
        raise HTTPException(status_code=404,detail=f"blog id {id} not found")
    return blog_post

@app.delete("/blog/{id}")
def delete_blog(id: int, session: Session = Depends(get_session)):
    query = select(Blog).where(Blog.id == id)
    blog_to_delete = session.exec(query).first()
    if not blog_to_delete:
        raise HTTPException(status_code=404,detail=f"blog id {id} not found")
    session.delete(blog_to_delete)
    session.commit()
    return {"status": "success", "message": f"Blog {id} deleted"}

@app.put("/blog/{id}")
def update_blog(id: int, blog: Blog, session: Session = Depends(get_session)):
    id: int
    blog: Blog
    query = select(Blog).where(Blog.id == id)
    blog_to_update = session.exec(query).first()
    if not blog_to_update:
        raise HTTPException(status_code=404,detail=f"blog id {id} not found")
    blog_to_update.title = blog.title
    blog_to_update.body = blog.body
    session.add(blog_to_update)
    session.commit()
    session.refresh(blog_to_update)
    return blog_to_update


