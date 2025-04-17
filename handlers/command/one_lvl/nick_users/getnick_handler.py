"""getnick_handler.py - Файл для команды с получением ника у пользователя"""
from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL
from AmperChatBot.handlers.ENUM.message import EGetNick

class CGetNick(AHandlerCommand):
    """Класс для обработки команды `/getnick`"""
    COMMAND = "getnick"
    PREFIX = PREFIX_DEFAULT
    ARGS = 1
    SEP = None
    
    MESSAGES_DICT = {
        'success': EGetNick.SUCCESS,
        'no_nick': EGetNick.NO_NICK,
    }

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.db = DAmperMySQL().nick_name_db

    async def _not_name_message(self, peer_id: int, user_id: int):
        await self.api.send_message(peer_id, f"✉ У @id{user_id} (пользователя) нет ника")

    async def _name_message(self, peer_id: int, user_id: int, name_user: str):
        await self.api.send_message(peer_id, f"✉ Ник @id{user_id} (пользователя) - {name_user}")

    async def _realization_command(self, message, args=None) -> None:
        user_id = await self.api.parse_user_id(args[0])
        id_chat = message.chat_id
        peer_id = message.peer_id

        user_db = await self.db.get(id_chat, user_id)

        if not user_db: await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="no_nick")
        else: await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="success", new_nick=user_db.nick)

    @checked_root_user(started_chat=True, lvl_admin_root=1)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)