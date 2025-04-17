from vkbottle.exception_factory.base_exceptions import VKAPIError

from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.ENUM.message import EQuit

class CQuit(AHandlerCommand):
    """Класс для обработки команды `/q`"""
    COMMAND = "q"
    PREFIX = PREFIX_DEFAULT
    ARGS = 0
    SEP = None

    MESSAGES_DICT = {
        'success': EQuit.SUCCESS,
        'self_admin': EQuit.SELF_ADMIN,
    }

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.punishment = api.punishment

    async def _realization_command(self, message, args=None) -> None:
        message_dict = message.dict()

        peer_id = message_dict['peer_id']
        chat_id = peer_id - 2000000000
        user_id = message_dict['from_id']

        try:
            await self.punishment.kick(chat_id, user_id)
        except VKAPIError as e:
            if e.code == 15:
                await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="self_admin")
        else:
            await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="success")

    @checked_root_user(started_chat=True)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)