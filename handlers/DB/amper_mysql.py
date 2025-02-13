from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from AmperChatBot.handlers.ABC.ABCAmperDataBase import ADataModel
from AmperChatBot.handlers.DB.Models import (
    BASE,
    InitedChat,
    LvlAdminRoot,
)

class DLvlAdminRoot(ADataModel):
    def __init__(self, session):
        self.session = session

    async def _add(self, id_user: int, id_chat: int, lvl_admin_root: int) -> None:
        """
        Добавляет права администратора пользователю в заданном чате, добавляя в базу данных `lvl_admin_root`

        :param id_user: ID пользователя
        :param id_chat: ID чата для добавления
        :param lvl_admin_root: Уровень администратора
        :return: None
        """
        with self.session() as session:
            new_admin = LvlAdminRoot(id_user, id_chat, lvl_admin_root)
            session.add(new_admin)
            session.commit()

    async def add(self, id_user: int, id_chat: int, lvl_admin_root: int) -> None: await self._add(id_user, id_chat, lvl_admin_root)

class DInitedChat(ADataModel):
    def __init__(self, session):
        self.session = session

    async def _add(self, id_chat: int) -> None:
        """
        Добавляет новый чат в базу данных `inited_chat`

        :param id_chat: ID чата для добавления
        :return: None
        """
        with self.session() as session:
            new_chat = InitedChat(id_chat=id_chat)
            session.add(new_chat)
            session.commit()

    async def _get(self, id_chat: int) -> "InitedChat":
        """
        Функция получает чат из базы данных `inited_chat`

        :param id_chat: ID чата для получения
        :return: None
        """
        with self.session() as session:
            stmt = select(InitedChat).where(InitedChat.id_chat == id_chat)
            result = session.execute(stmt)
            return result.scalars().first()

    async def add(self, id_chat): await self._add(id_chat)
    async def get(self, id_chat) -> str: return await self._get(id_chat)


class DAmperMySQL:
    DB = None
    def __new__(cls, *args, **kwargs):
        if not cls.DB:
            cls.DB = super(DAmperMySQL, cls).__new__(cls)
        return cls.DB

    def __init__(self):
        self.engine = create_engine("mysql+pymysql://shprot:shprot@localhost:3307/amper", echo=True, pool_size=20)
        self.session = sessionmaker(
            self.engine,
            expire_on_commit=False,
        )

        self.Base = BASE

        self._inited_chat_db = DInitedChat(self.session)
        self._lvl_admin_root = DLvlAdminRoot(self.session)

    @property
    def inited_chat_db(self): return self._inited_chat_db

    @property
    def lvl_admin_root(self): return self._lvl_admin_root


    def init_database(self) -> None:
        """
        Функция для инициализации баз данных

        :return: None
        """
        with self.engine.begin() as conn:
            self.Base.metadata.create_all(conn)