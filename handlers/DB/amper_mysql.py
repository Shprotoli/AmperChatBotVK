from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from AmperChatBot.handlers.ABC.ABCAmperDataBase import ADataModel
from AmperChatBot.handlers.DB.Models import (
    BASE,
    InitedChat
)

class DInitedChat(ADataModel):
    def __init__(self, session):
        self.session = session

    async def _add_chat(self, id_chat: int):
        """
        Добавляет новый чат в базу данных

        :param id_chat: ID чата для добавления
        """
        with self.session() as session:
            new_chat = InitedChat(id_chat=id_chat)
            session.add(new_chat)
            session.commit()

    async def add_chat(self, id_chat) -> None: await self._add_chat(id_chat)


class DAmperMySQL:
    def __init__(self):
        self.engine = create_engine("mysql+pymysql://shprot:shprot@localhost:3307/amper", echo=True, pool_size=20)
        self.session = sessionmaker(
            self.engine,
            expire_on_commit=False,
        )

        self.Base = BASE

        self._inited_chat_db = DInitedChat(self.session)

    @property
    def inited_chat_db(self): return self._inited_chat_db

    def _init_database(self) -> None:
        """
        Функция для инициализации баз данных

        :return: None
        """

        with self.engine.begin() as conn:
            self.Base.metadata.create_all(conn)