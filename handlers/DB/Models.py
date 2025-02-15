from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

BASE = declarative_base()

class InitedChat(BASE):
    """Модель для хранения чатов, которые были активированы"""
    __tablename__ = "inited_chat"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_chat = Column(Integer, nullable=False)

class LvlAdminRoot(BASE):
    """Модель для хранения пользователей с админ правами"""
    __tablename__ = "lvl_admin_root"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_user = Column(Integer, nullable=False)
    id_chat = Column(Integer, nullable=False)
    lvl_admin_root = Column(Integer, nullable=False)

class NickName(BASE):
    """Модель для хранения пользователей с админ правами"""
    __tablename__ = "nick_name"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_user = Column(Integer, nullable=False)
    id_chat = Column(Integer, nullable=False)
    nick = Column(String(length=60), nullable=False)