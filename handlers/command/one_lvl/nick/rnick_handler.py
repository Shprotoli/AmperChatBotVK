"""rnick_handler.py - Файл для команды с удалением ника у пользователя"""
from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL

class CRemoveNick(AHandlerCommand):
    """Класс для обработки команды `/rnick`"""
    COMMAND = "rnick"
    PREFIX = PREFIX_DEFAULT
    ARGS = 1
    SEP = None

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.db = DAmperMySQL().nick_name_db

    async def _get_id(self, user_info: str) -> int:
        if "|" in user_info: return int(user_info.split("|")[0].replace("[id", ""))

    async def _delete_message(self, peer_id: int, id_user: int):
        await self.api.send_message(peer_id, f"✉ Вы удалили @id{id_user} (пользователю) ник")

    async def _not_delete_message(self, peer_id: int, id_user: int):
        await self.api.send_message(peer_id, f"⚠ У @id{id_user} (пользователя) нет ника")

    async def _realization_command(self, message, args=None) -> None:
        id_user = await self._get_id(args[0])
        id_chat = message.chat_id
        peer_id = message.peer_id

        result_db_remove = await self.db.remove(id_user, id_chat)

        if result_db_remove:
            await self._delete_message(peer_id, id_user)
        else:
            await self._not_delete_message(peer_id, id_user)

    @checked_root_user(started_chat=True, lvl_admin_root=1)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)