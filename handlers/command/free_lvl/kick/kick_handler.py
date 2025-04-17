"""rnick_handler.py - Файл для команды с удалением ника у пользователя"""
from vkbottle.exception_factory.base_exceptions import VKAPIError

from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL

class CKick(AHandlerCommand):
    """Класс для обработки команды `/kick`"""
    COMMAND = "kick"
    PREFIX = PREFIX_DEFAULT
    ARGS = 1
    SEP = None

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.punishment = api.punishment

        self.db = DAmperMySQL().nick_name_db

    async def _user_kick_message(self, peer_id: int, id_user: int):
        await self.api.send_message(peer_id, f"👀 @id{id_user} (Пользователя) выкидывают с этой вечеринки.")

    async def _user_error_kick_message(self, peer_id: int, id_user: int):
        await self.api.send_message(peer_id, f"⛔ @id{id_user} (Пользователя) нет в данном чате.")

    async def _realization_command(self, message, args=None) -> None:
        id_user = await self.api.parse_user_id(args[0])
        id_chat = message.chat_id
        peer_id = message.peer_id

        try:
            await self.punishment.kick(id_chat, id_user)
        except VKAPIError as e:
            if e.code == 100:
                await self._user_error_kick_message(peer_id, id_user)
        else:
            await self._user_kick_message(peer_id, id_user)

    @checked_root_user(started_chat=True, lvl_admin_root=3)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)