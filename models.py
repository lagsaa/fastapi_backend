# models.py
from sqlalchemy import Column, Integer, String, Boolean
from database import Base
from pydantic import BaseModel

class TodoItem(Base):
    __tablename__ = 'todo_items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)

# Pydantic model for response
class TodoItemResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        orm_mode = True  # This allows Pydantic to read data from SQLAlchemy models