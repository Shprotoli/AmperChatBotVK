"""rnick_handler.py - Файл для команды с удалением ника у пользователя"""
from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL
from AmperChatBot.handlers.ENUM.message import ERemoveNick

class CRemoveNick(AHandlerCommand):
    """Класс для обработки команды `/rnick`"""
    DIR = "../../handlers/command/one_lvl/nick_users/rnick_handler.py"
    COMMAND = "rnick"
    PREFIX = PREFIX_DEFAULT
    ARGS = 1
    SEP = None
    
    MESSAGES_DICT = {
        'success': ERemoveNick.SUCCESS,
        'no_nick': ERemoveNick.NO_NICK,
    }

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.db = DAmperMySQL().nick_name_db

    async def _realization_command(self, message, args=None) -> None:
        user_id = await self.api.parse_user_id(args[0])
        id_chat = message.chat_id
        peer_id = message.peer_id

        result_db_remove = await self.db.remove(user_id, id_chat)

        if result_db_remove:
            await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="success")
        else:
            await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="no_nick")

    @checked_root_user(started_chat=True, lvl_admin_root=1)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)