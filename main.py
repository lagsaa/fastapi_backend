# main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from models import TodoItem, TodoItemResponse
from database import SessionLocal, engine
from pydantic import BaseModel

app = FastAPI()


class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    title: str
    completed: bool

@app.post("/todos/", response_model=TodoItemResponse)
def create_todo(item: TodoCreate):
    db = SessionLocal()
    todo_item = TodoItem(title=item.title)
    db.add(todo_item)
    db.commit()
    db.refresh(todo_item)
    return todo_item

@app.get("/todos/", response_model=list[TodoItemResponse])
def read_todos(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    return db.query(TodoItem).offset(skip).limit(limit).all()

@app.put("/todos/{todo_id}", response_model=TodoItemResponse)
def update_todo(todo_id: int, item: TodoUpdate):
    db = SessionLocal()
    db_item = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_item.title = item.title
    db_item.completed = item.completed
    db.commit()
    return db_item

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    db = SessionLocal()
    db_item = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Todo deleted"}
