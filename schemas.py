from pydantic import BaseModel

class TodoItemBase(BaseModel):
    title: str
    completed: bool = False

class TodoItemCreate(TodoItemBase):
    pass

class TodoItem(TodoItemBase):
    id: int

    class Config:
        orm_mode = True