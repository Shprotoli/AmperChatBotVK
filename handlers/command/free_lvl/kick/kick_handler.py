"""rnick_handler.py - Файл для команды с удалением ника у пользователя"""
from vkbottle.exception_factory.base_exceptions import VKAPIError

from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL
from AmperChatBot.handlers.ENUM.message import EKickMessage

class CKick(AHandlerCommand):
    """Класс для обработки команды `/kick`"""
    DIR = "../../handlers/command/free_lvl/kick/kick_handler.py"
    COMMAND = "kick"
    PREFIX = PREFIX_DEFAULT
    ARGS = 1
    SEP = None

    MESSAGES_DICT = {
        'success': EKickMessage.SUCCESS,
        'no_in_chat': EKickMessage.NOT_IN_CHAT,
    }

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.punishment = api.punishment

        self.db = DAmperMySQL().nick_name_db

    async def _realization_command(self, message, args=None) -> None:
        user_id = await self.api.parse_user_id(args[0])
        id_chat = message.chat_id
        peer_id = message.peer_id

        try:
            await self.punishment.kick(id_chat, user_id)
        except VKAPIError as e:
            if e.code == 100:
                await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="no_in_chat")
        else:
            await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="success")

    @checked_root_user(started_chat=True, lvl_admin_root=3)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)