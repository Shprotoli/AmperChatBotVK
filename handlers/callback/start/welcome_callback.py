# -*- coding: utf-8 -*-
"""welcome_callback.py - Файл предназначен для обработки команд связанных с вступлением бота в группу"""
from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Callback

from AmperChatBot.handlers.ABC.ABCAmper import ACallbackHandler
from AmperChatBot.handlers.DB.amper_mysql import DInitedChat

class CStartBot(ACallbackHandler):
    """Класс для обработки события нажатия на кнопку `Старт` в первом приветствии от бота"""
    def __init__(self, db: "DInitedChat"):
        self.db = db

    async def _user_not_owner_chat(self) -> None:
        """
        Функция, которая отправляет сообщение пользователю, если у него нет прав для активации бота

        :return: None
        """
        await self.api_vk_class.send_notif(
            peer_id=self.peer_id,
            user_id=self.user_id,
            event_id=self.event_id,
            message="❌ У вас нет прав для активации бота в данной беседе!"
        )

    async def _bot_not_is_admin(self) -> None:
        """
        Функция, которая отправляет сообщение, что у бота нет админки беседы в случае,
        если функция `bot_is_admin_in_chat`, возвращает None, иначе,
        запускает функцию `_user_not_owner_chat`

        :return: None
        """
        if not await self.api_vk_class.bot_is_admin_in_chat(self.peer_id):
            await self.api_vk_class.send_notif(peer_id=self.peer_id, user_id=self.user_id, event_id=self.event_id, message="❌ У бота нет прав администратора в беседе!")
        else: await self._user_not_owner_chat()

    async def _user_owner_chat(self) -> None:
        """
        Функция, которая отправляет сообщение об успешной активации бота.

        :param chat_in_db: Поле отвечает за проверку был ли чат активирован до этого
            - `True`: Если поле chat_in_db является True, то бот уже был активирован до этого
            - `False`: Если False, то бот еще не был активирован до этого
        :return: None
        """
        chat_in_db = await self.db.get_chat(self.peer_id)

        if not chat_in_db:
            await self.api_vk_class.edit_message_chat(self.peer_id, self.conversation_message_id, "✅ Бот успешно активирован! Пропишите '/help', чтобы узнать все команды!")
            await self.db.add_chat(self.peer_id)
        else:
            await self.api_vk_class.edit_message_chat(self.peer_id, self.conversation_message_id, "❌ Бот уже активирован! Пропишите '/help', чтобы узнать все команды!")

    async def _realization_callback(self, information_callback, api_vk_class):
        self.api_vk_class = api_vk_class

        self.user_id = information_callback['user_id']
        self.peer_id = information_callback['peer_id']
        self.event_id = information_callback['event_id']
        self.conversation_message_id = information_callback['conversation_message_id']

        is_owner = await api_vk_class.is_creater_chat(id_user=self.user_id, peer_id=self.peer_id)

        if is_owner: await self._user_owner_chat()
        else: await self._bot_not_is_admin()

    async def realization_callback(self, information_callback, api_vk_class): await self._realization_callback(information_callback, api_vk_class)


class CJoinGroup:
    """Класс для обработки логики подключения бота к беседе"""
    TEXT_JOIN_MESSAGE = (
        "Привет! Amper теперь в вашей беседе 🥳\n\n"
        "Для дальнейшей работы нужно дать боту права администратора, а затем нажать кнопку 'Старт' 🚀"
    )

    KEYBOARD_START = (
        Keyboard(inline=True)
        .add(Callback("Старт", payload={"command": "start_bot_chat"}), color=KeyboardButtonColor.POSITIVE)
    )

    async def join_group(self, message: Message):
        if message.action.member_id == -228701807: await message.answer(self.TEXT_JOIN_MESSAGE, keyboard=self.KEYBOARD_START)