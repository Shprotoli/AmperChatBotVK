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
from AmperChatBot.handlers.command.zero_lvl.help.help_handler import CHelp
from AmperChatBot.handlers.command.zero_lvl.help.info_handler import CInfo
from AmperChatBot.handlers.command.zero_lvl.other.q_handler import CQuit
from AmperChatBot.handlers.command.free_lvl.setlvl_handler import CSetLvl
from AmperChatBot.handlers.command.two_lvl.setnick_handler import CSetNick
from AmperChatBot.handlers.command.two_lvl.nlist_handler import CNickList
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
        help_ekz = CHelp(self.api_vk_ekz)
        info_ekz = CInfo(self.api_vk_ekz)
        quit_ekz = CQuit(self.api_vk_ekz)
        set_nick_ekz = CSetNick(self.api_vk_ekz)
        set_lvl_ekz = CSetLvl(self.api_vk_ekz)
        nick_list_ekz = CNickList(self.api_vk_ekz)

        """Инициализация обработчика команд"""
        labeler.chat_message(CommandRule(help_ekz.COMMAND, help_ekz.PREFIX, help_ekz.ARGS))(help_ekz.realization_command)
        labeler.chat_message(CommandRule(info_ekz.COMMAND, info_ekz.PREFIX, info_ekz.ARGS))(info_ekz.realization_command)
        labeler.chat_message(CommandRule(quit_ekz.COMMAND, quit_ekz.PREFIX, quit_ekz.ARGS))(quit_ekz.realization_command)
        labeler.chat_message(CommandRule(set_lvl_ekz.COMMAND, set_lvl_ekz.PREFIX, set_lvl_ekz.ARGS))(set_lvl_ekz.realization_command)
        labeler.chat_message(CommandRule(set_nick_ekz.COMMAND, set_nick_ekz.PREFIX, set_nick_ekz.ARGS, sep="] "))(set_nick_ekz.realization_command)
        labeler.chat_message(CommandRule(nick_list_ekz.COMMAND, nick_list_ekz.PREFIX, nick_list_ekz.ARGS))(nick_list_ekz.realization_command)

if __name__ == "__main__":
    bot = AmperBotInit(token)
    bot.run_forever()