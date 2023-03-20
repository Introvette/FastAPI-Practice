from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Todos(Base):
    __tablename__ = "todos"
    # Where we define the actual table name
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
