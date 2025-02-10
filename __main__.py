# -*- codingc: utf-8 -*-
"""__main__.py - Основная реализация и запуск бота"""
from asyncio import run

from vkbottle.bot import Bot
from vkbottle.dispatch.rules.base import ChatActionRule, CommandRule
from vkbottle_types.events import GroupEventType

from _init.config import token, labeler
# HANDLERS
from AmperChatBot.handlers.callback.callback import CCallbackHandler
from AmperChatBot.handlers.callback.start.welcome_callback import CJoinGroup
from handlers.api_vk import CApiVK
# COMMAND
from AmperChatBot.handlers.command.help.help_handler import CHelp
# DataBase
from handlers.DB.amper_mysql import DAmperMySQL

class AmperBotInit(Bot):
    def __init__(self, token: str):
        super().__init__(token, labeler=labeler)
        run(self._connect_database())

        self.api_vk_ekz = CApiVK(self)

        self._register_handlers()
        self._register_command()

    async def _connect_database(self):
        """
        Функция для установки соединения с базой данных

        :return: None
        """
        self.db = DAmperMySQL()
        self.db.init_database()

    def _register_handlers(self) -> None:
        join_group_ekz = CJoinGroup()
        callback_handler_ekz = CCallbackHandler(self, self.api_vk_ekz, self.db)

        """Инициализация обработчиков бота"""
        labeler.chat_message(ChatActionRule("chat_invite_user"))(join_group_ekz.join_group)
        labeler.raw_event(GroupEventType.MESSAGE_EVENT)(callback_handler_ekz.callback_handler)

    def _register_command(self) -> None:
        help_ekz = CHelp()

        """Инициализация обработчика команд"""
        labeler.chat_message(CommandRule(help_ekz.COMMAND, help_ekz.PREFIX, help_ekz.ARGS))(help_ekz.realization_command)

if __name__ == "__main__":
    bot = AmperBotInit(token)
    bot.run_forever()