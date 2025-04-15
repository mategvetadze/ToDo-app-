from sqlalchemy import Column,Integer,Boolean,String
from db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)
