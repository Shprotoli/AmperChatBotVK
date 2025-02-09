from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

class DAmperMySQL:
    def __init__(self):
        self.engine = create_async_engine("mysql+asyncmy://shprot:shprot@localhost:3307/amper", echo=True)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        self.Base = declarative_base()
        self.session = None

    async def _init_database(self) -> None:
        """
        Функция для инициализации баз данных

        :return: None
        """
        class InitedChat(self.Base):
            __tablename__ = "inited_chat"

            id = Column(Integer, primary_key=True, autoincrement=True)
            id_chat = Column(Integer, primary_key=True)

        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)