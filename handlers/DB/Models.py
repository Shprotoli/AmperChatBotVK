from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

BASE = declarative_base()

class InitedChat(BASE):
    __tablename__ = "inited_chat"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_chat = Column(Integer, nullable=False)