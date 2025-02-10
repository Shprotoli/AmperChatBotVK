"""ABCAmper.py - Файл предназначеный для абстрактных классов бота"""
from abc import ABC, abstractmethod
from typing import Union, Optional, Tuple

from vkbottle.bot import Message

class AHandlerCommand(ABC):
    COMMAND = str # Команда для handler, например `help`
    PREFIX = () # Префикс для команды, например `("/", ".")`
    ARGS = int # Количество аргументов, например `2`
    @abstractmethod
    async def _realization_command(self, message: Message, args: Tuple[str]) -> None:
        """
        Функция, которая реализуют ответ на команду

        :param message_event: Информация о команде
        :param api_vk_class: Класс 'CApiVk', с помощью которого можно взаимодействовать с API VK
        :return: None
        """
        pass

    @abstractmethod
    async def realization_command(self, message: Message, args: Tuple[str]) -> None:
        """
        Функция, которая реализуют ответ на команду

        :param message_event: Информация о команде
        :param api_vk_class: Класс 'CApiVk', с помощью которого можно взаимодействовать с API VK
        :return: None
        """
        pass

class ACallbackHandler(ABC):
    @abstractmethod
    async def _realization_callback(self, information_callback: dict, api_vk_class: "AApiVk") -> None:
        """
        Функция для реализация ответа на callback запрос.

        :param event_id: Строка с уникальным `ID` события
        :param information_callback: Словарь, в котором находится информация о callback
        :param api_vk_class: Класс 'CApiVk', с помощью которого можно взаимодействовать с API VK
        :return: None
        """
        pass

    @abstractmethod
    async def realization_callback(self, information_callback: dict, api_vk_class: "AApiVk") -> None:
        """
        Функция для вызова реализации ответа на callback запрос.

        :param event_id: Строка с уникальным `ID` события
        :param information_callback: Словарь, в котором находится информация о callback
        :param api_vk_class: Класс 'CApiVk', с помощью которого можно взаимодействовать с API VK
        :return: None
        """
        pass

class AApiVk(ABC):
    @abstractmethod
    async def get_creater_chat(self, peer_id: Union[str, int]) -> Optional[int]:
        """
        Функция для получения информации о создатели беседы

        :param peer_id: ID группы
        :return:
            - `None`, если у бота нет админ-прав в беседе.
            - `int` (ID создателя группы), если у бота есть админ-права.
        """
        pass

    @abstractmethod
    async def is_creater_chat(self, id_user: Union[str, int], peer_id: Union[str, int]) -> bool:
        """
        Функция для проверки является ли пользователь создателем беседы

        :param id_user: ID пользователя
        :param peer_id: ID беседы
        :return:
            - `bool`, False, если не создатель, True, если создатель
        """
        pass

    @abstractmethod
    async def bot_is_admin_in_chat(self, peer_id: Union[str, int]) -> bool:
        """
        Функция для проверки есть права администратора у бота в беседе

        :param peer_id: ID беседы
        :return:
            - `True`, когда у бота есть права администратора в беседе
            - `False`, когда у бота нет прав администратора в беседе
        """
        pass

    @abstractmethod
    async def edit_message_chat(self, peer_id: Union[str, int], conversation_message_id: Union[str, int], message: str, keyboard: tuple) -> None:
        """
        Функция для редактирования сообщения в беседе

        :param peer_id: ID группы
        :param conversation_message_id: ID сообщения
        :param message: На какое сообщение меняем
        :param keyboard: Клавиатура в сообщении
        :return: None
        """
        pass

    @abstractmethod
    async def send_notif(self, peer_id: Union[str, int], event_id: Union[str, int], user_id: Union[str, int], message: str) -> None:
        """
        Функция для отправки уведомления пользователю

        :param peer_id: ID группы
        :param event_id: ID события
        :param user_id: ID пользователя, которому отправляем уведомление
        :param message: Сообщение которое отправляем
        :return: None
        """
        pass