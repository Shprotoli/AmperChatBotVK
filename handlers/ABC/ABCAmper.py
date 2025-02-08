"""ABCAmper.py - Файл предназначеный для абстрактных классов бота"""
from abc import ABC, abstractmethod
from typing import Union, Optional

class ACallbackHandler(ABC):
    @abstractmethod
    async def realization_callback(self, information_callback: dict, api_vk_class: "AApiVk") -> None:
        """
        Функция для реализация ответа на callback запрос.

        :param information_callback: Словарь, в котором находится информация о callback
        :param api_vk_class: Класс 'CApiVk', с помощью которого можно взаимодействовать с API VK
        :return: None
        """
        pass

class AApiVk(ABC):
    @abstractmethod
    async def get_creater_group(self, peer_id: Union[str, int]) -> Optional[int]:
        """
        Функция для получения информации о создатели беседы.

        :param peer_id: ID группы
        :return:
            - `None`, если у бота нет админ-прав в беседе.
            - `int` (ID создателя группы), если у бота есть админ-права.
        """
        pass