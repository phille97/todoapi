from sqlalchemy import Boolean, Column, Integer, String

from .db import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    is_done = Column(Boolean)
