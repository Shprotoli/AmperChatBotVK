from typing import Optional

from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import sessionmaker

from AmperChatBot.handlers.ABC.ABCAmperDataBase import ADataModel
from AmperChatBot.handlers.DB.Models import (
    BASE,
    InitedChat,
    LvlAdminRoot,
    NickName,
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
            new_admin = LvlAdminRoot(id_user=id_user, id_chat=id_chat, lvl_admin_root=lvl_admin_root)
            session.add(new_admin)
            session.commit()

    async def _update_lvl_admin(self, id_user: int, id_chat: int, new_lvl_admin_root: int) -> Optional["LvlAdminRoot"]:
        """
        Обновляет уровень администратора для пользователя в заданном чате.

        :param id_user: ID пользователя
        :param id_chat: ID чата
        :param new_lvl_admin_root: Новый уровень администратора
        :return: Обновленная запись или None, если запись не найдена
        """
        with self.session() as session:
            stmt = select(LvlAdminRoot).where(
                (LvlAdminRoot.id_user == id_user) &
                (LvlAdminRoot.id_chat == id_chat)
            )
            result = session.execute(stmt)
            admin_record = result.scalar_one_or_none()

            if admin_record:
                stmt = (
                    update(LvlAdminRoot)
                    .where(
                        (LvlAdminRoot.id_user == id_user) &
                        (LvlAdminRoot.id_chat == id_chat)
                    )
                    .values(lvl_admin_root=new_lvl_admin_root)
                )
                session.execute(stmt)
                session.commit()
                return admin_record

    async def _get_mr(self, id_user: int, id_chat: int, lvl_admin_root: int) -> Optional["LvlAdminRoot"]:
        """
        Получение записи в котором поле `lvl_admin_root` равен заданному или больше

        :param id_user: ID пользователя
        :param id_chat: ID чата
        :param lvl_admin_root: Уровень администратора
        :return:
        """
        with self.session() as session:
            stmt = select(LvlAdminRoot).where(
                (LvlAdminRoot.id_user == id_user) &
                (LvlAdminRoot.id_chat == id_chat) &
                (LvlAdminRoot.lvl_admin_root >= lvl_admin_root)
            )
            result = session.execute(stmt)
            admin_record = result.scalar_one_or_none()

            return admin_record

    async def _get(self, id_user: int, id_chat: int) -> Optional["LvlAdminRoot"]:
        with self.session() as session:
            stmt = select(LvlAdminRoot).where(
                (LvlAdminRoot.id_user == id_user) &
                (LvlAdminRoot.id_chat == id_chat)
            )
            result = session.execute(stmt)
            admin_record = result.scalar_one_or_none()

            return admin_record

    async def add(self, id_user: int, id_chat: int, lvl_admin_root: int) -> None: await self._add(id_user, id_chat, lvl_admin_root)
    async def get_mr(self, id_user: int, id_chat: int, lvl_admin_root: int) -> Optional["LvlAdminRoot"]: return await self._get_mr(id_user, id_chat, lvl_admin_root)
    async def get(self, id_user: int, id_chat: int) -> Optional["LvlAdminRoot"]: return await self._get(id_user, id_chat)
    async def update_lvl_admin(self, id_user: int, id_chat: int, lvl: int) -> Optional["LvlAdminRoot"]: await self._update_lvl_admin(id_user, id_chat, lvl)

class DNickName(ADataModel):
    def __init__(self, session):
        self.session = session

    async def _add(self, id_user: int, id_chat: int, new_nick: str) -> None:
        """
        Добавляет новый ник для пользователя в чате в базу данных `new_nick`

        :param id_chat: ID чата для добавления
        :return: None
        """
        with self.session() as session:
            new_column = NickName(id_user=id_user, id_chat=id_chat, nick=new_nick)
            session.add(new_column)
            session.commit()

    async def _remove(self, id_user: int, id_chat: int) -> bool:
        """
        Функция для удаления ника пользователю

        :param id_user: ID пользователя
        :param id_chat: ID чата
        :return: Возвращает `bool` тип в зависимости от ситуации
                - `True`: Если был найден в таблице и удален
                - `False`: Если не был найден в таблице и не был удален
        """
        with self.session() as session:
            smrt = delete(NickName).where(
                NickName.id_chat == id_chat,
                NickName.id_user == id_user,
            )

            result = session.execute(smrt)
            session.commit()

            return True if result.rowcount else False

    async def _update(self, id_user: int, id_chat: int, new_nick: str) -> Optional["NickName"]:
        """
        Обновляет уровень администратора для пользователя в заданном чате.

        :param id_user: ID пользователя
        :param id_chat: ID чата
        :param new_nick: Новый ник пользователя
        :return: Обновленная запись или None, если запись не найдена
        """
        with self.session() as session:
            stmt = select(NickName).where(
                (NickName.id_user == id_user) &
                (NickName.id_chat == id_chat)
            )
            result = session.execute(stmt)
            admin_record = result.scalar_one_or_none()

            if admin_record:
                stmt = (
                    update(NickName)
                    .where(
                        (NickName.id_user == id_user) &
                        (NickName.id_chat == id_chat)
                    )
                    .values(nick=new_nick)
                )
                session.execute(stmt)
                session.commit()
                return admin_record

    async def _get_more(self, id_chat: int) -> list:
        with self.session() as session:
            stmt = select(NickName).where(
                NickName.id_chat == id_chat
            )
            result = session.execute(stmt)
            return result.scalars().all()

    async def _get(self, id_chat: int, id_user: int) -> "NickName":
        """
        Функция получает пользователя из базы данных `new_nick`

        :param id_chat: ID чата для получения
        :return: None
        """
        with self.session() as session:
            stmt = select(NickName).where(
                                            NickName.id_chat == id_chat,
                                            NickName.id_user == id_user,
                                            )
            result = session.execute(stmt)
            return result.scalars().first()

    async def add(self, id_user, id_chat, new_nick): await self._add(id_user, id_chat, new_nick)
    async def update(self, id_chat, id_user, new_nick): return await self._update(id_chat, id_user, new_nick)
    async def get(self, id_chat, id_user): return await self._get(id_chat, id_user)
    async def remove(self, id_user, id_chat): return await self._remove(id_user, id_chat)
    async def get_more(self, id_chat): return await self._get_more(id_chat)

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

    async def _get(self, id_peer: int) -> "InitedChat":
        """
        Функция получает чат из базы данных `inited_chat`

        :param id_chat: ID чата для получения
        :return: None
        """
        with self.session() as session:
            stmt = select(InitedChat).where(InitedChat.id_chat == id_peer)
            result = session.execute(stmt)
            return result.scalars().first()

    async def add(self, id_chat): await self._add(id_chat)
    async def get(self, id_peer): return await self._get(id_peer)


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
        self._lvl_admin_root_db = DLvlAdminRoot(self.session)
        self._nick_name_db = DNickName(self.session)

    @property
    def inited_chat_db(self): return self._inited_chat_db

    @property
    def lvl_admin_root(self): return self._lvl_admin_root_db

    @property
    def nick_name_db(self): return self._nick_name_db


    def init_database(self) -> None:
        """
        Функция для инициализации баз данных

        :return: None
        """
        with self.engine.begin() as conn:
            self.Base.metadata.create_all(conn)