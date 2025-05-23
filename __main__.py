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
from AmperChatBot.handlers.command.zero_lvl.other.random_handler import CRandom
from AmperChatBot.handlers.command.zero_lvl.other.q_handler import CQuit
from AmperChatBot.handlers.command.one_lvl.nick_users.setnick_handler import CSetNick
from AmperChatBot.handlers.command.one_lvl.nick_users.nlist_handler import CNickList
from AmperChatBot.handlers.command.one_lvl.nick_users.rnick_handler import CRemoveNick
from AmperChatBot.handlers.command.one_lvl.online_users.olist_handler import COnlineList
from AmperChatBot.handlers.command.one_lvl.staff_users.staff_handler import CStaffList
from AmperChatBot.handlers.command.one_lvl.nick_users.getnick_handler import CGetNick
from AmperChatBot.handlers.command.two_lvl.mute.mute_handler import CMute
from AmperChatBot.handlers.command.two_lvl.mute.unmute_handler import CUnMute
from AmperChatBot.handlers.command.free_lvl.lvl.setlvl_handler import CSetLvl
from AmperChatBot.handlers.command.free_lvl.lvl.dellvl_handler import CDeleteLevel
from AmperChatBot.handlers.command.free_lvl.kick.kick_handler import CKick
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
        join_group_ekz = CJoinGroup(self.db.inited_chat_db)
        callback_handler_ekz = CCallbackHandler(self, self.api_vk_ekz, self.db)

        """Инициализация обработчиков бота"""
        labeler.chat_message(ChatActionRule("chat_invite_user"))(join_group_ekz.join_group)
        labeler.raw_event(GroupEventType.MESSAGE_EVENT)(callback_handler_ekz.callback_handler)

    def _register_command(self) -> None:
        commands = (
            CHelp(self.api_vk_ekz),
            CInfo(self.api_vk_ekz),
            CQuit(self.api_vk_ekz),
            CSetNick(self.api_vk_ekz),
            CSetLvl(self.api_vk_ekz),
            CNickList(self.api_vk_ekz),
            CRemoveNick(self.api_vk_ekz),
            CDeleteLevel(self.api_vk_ekz),
            CRandom(self.api_vk_ekz),
            CMute(self.api_vk_ekz),
            CUnMute(self.api_vk_ekz),
            COnlineList(self.api_vk_ekz),
            CStaffList(self.api_vk_ekz),
            CGetNick(self.api_vk_ekz),
            CKick(self.api_vk_ekz),
        )

        for command in commands:
            if not command.SEP: SEP = " "
            else: SEP = command.SEP

            labeler.chat_message(CommandRule(command.COMMAND, command.PREFIX, command.ARGS, SEP))(command.realization_command)

if __name__ == "__main__":
    bot = AmperBotInit(token)
    bot.run_forever()