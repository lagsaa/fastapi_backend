from sqlalchemy.orm import Session
from . import models, schemas

def get_todo_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.TodoItem).offset(skip).limit(limit).all()

def create_todo_item(db: Session, todo_item: schemas.TodoItemCreate):
    db_item = models.TodoItem(**todo_item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_todo_item(db: Session, item_id: int, todo_item: schemas.TodoItemCreate):
    db_item = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    if db_item:
        db_item.title = todo_item.title
        db_item.completed = todo_item.completed
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_todo_item(db: Session, item_id: int):
    db_item = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item