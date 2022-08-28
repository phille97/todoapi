from pydantic import BaseModel


class Item(BaseModel):
    id: int
    description: str
    is_done: bool = False

    class Config:
        orm_mode = True


class ItemCreate(BaseModel):
    description: str
    is_done: bool = False


class ItemUpdate(BaseModel):
    description: str | None = None
    is_done: bool | None = None
