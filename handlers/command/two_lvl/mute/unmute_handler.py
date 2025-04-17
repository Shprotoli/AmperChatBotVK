"""unmute_handler.py - Файл для реализации снятия мута"""
from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL
from AmperChatBot.handlers.ENUM.message import EUnMute

class CUnMute(AHandlerCommand):
    """Класс для обработки команды `/unmute`"""
    COMMAND = "unmute"
    PREFIX = PREFIX_DEFAULT
    ARGS = 1
    SEP = None

    MESSAGES_DICT = {
        'success': EUnMute.SUCCESS,
    }

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.db = DAmperMySQL().mute_db

    async def _unmute_message(self, peer_id: int, user_id:int, id_user_request: int) -> None:
        await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="self_remove", id_request=id_user_request)

    async def _realization_command(self, message, args=None) -> None:
        request_user_id = message.from_id
        user_id = await self.api.parse_user_id(args[0])
        peer_id = message.peer_id

        await self.api.punishment.unmute(peer_id, user_id)
        await self._unmute_message(peer_id, user_id, request_user_id)

    @checked_root_user(started_chat=True, lvl_admin_root=2)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)