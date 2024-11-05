from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()
templates = Jinja2Templates(directory="templates")

SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer)

Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def book_list(request: Request):
    db = SessionLocal()
    books = db.query(Book).all()
    return templates.TemplateResponse("book_list.html", {"request": request, "books": books})

@app.get("/add", response_class=HTMLResponse)
def add_book_form(request: Request):
    return templates.TemplateResponse("add_book.html", {"request": request})

@app.post("/add")
def add_book(title: str = Form(...), author: str = Form(...), year: int = Form(...)):
    db = SessionLocal()
    new_book = Book(title=title, author=author, year=year)
    db.add(new_book)
    db.commit()
    return RedirectResponse(url="/", status_code=303)