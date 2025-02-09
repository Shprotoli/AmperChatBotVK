# -*- coding: utf-8 -*-
"""__main__.py - Основная реализация и запуск бота"""
from asyncio import run

from vkbottle.bot import Bot
from vkbottle.dispatch.rules.base import ChatActionRule
from vkbottle_types.events import GroupEventType

from _init.config import token, labeler
# HANDLERS
from handlers.callback import CCallbackHandler
from handlers.start.welcome import CJoinGroup
from handlers.api_vk import CApiVK
# DataBase
from handlers.DB.amper_mysql import DAmperMySQL

class AmperBotInit(Bot):
    def __init__(self, token: str):
        super().__init__(token, labeler=labeler)
        run(self._connect_database())

        self.join_group_ekz = CJoinGroup()
        self.api_vk_ekz = CApiVK(self)
        self.callback_handler_ekz = CCallbackHandler(self, self.api_vk_ekz)

        self._register_handlers()

    async def _connect_database(self):
        """
        Функция для установки соединения с базой данных

        :return: None
        """
        self.db = DAmperMySQL()
        await self.db._init_database()

    def _register_handlers(self) -> None:
        """Инициализация обработчиков бота"""
        labeler.chat_message(ChatActionRule("chat_invite_user"))(self.join_group_ekz.join_group)
        labeler.raw_event(GroupEventType.MESSAGE_EVENT)(self.callback_handler_ekz.callback_handler)

if __name__ == "__main__":
    bot = AmperBotInit(token)
    bot.run_forever()