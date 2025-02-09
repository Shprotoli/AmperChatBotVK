from abc import ABC, abstractmethod

class ADataModel(ABC):
    @abstractmethod
    def __init__(self, session) -> None:
        """
        `__init__` - Принимает объект `session`,
                    для дальнейшей работы с базой данных

        :param session: Сессия подключения к базе данных
        """
        pass