from vkbottle.exception_factory.base_exceptions import VKAPIError

from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK

class CQuit(AHandlerCommand):
    """Класс для обработки команды `/q`"""
    COMMAND = "q"
    PREFIX = PREFIX_DEFAULT
    ARGS = 0

    def __init__(self, bot: "CApiVK"):
        self.bot = bot
        self.punishment = bot.punishment

    async def _user_admin_chat(self, peer_id: int, user_id: int):
        await self.bot.send_message(peer_id, f"⛔ Я не могу кикнуть @id{user_id} (тебя), "
                                             f"потому что ты являешься администратором данной беседы.")

    async def _user_kick(self, peer_id: int, user_id: int):
        await self.bot.send_message(peer_id, f"👀 @id{user_id} (Пользователь) покидает эту вечеринку.")

    async def _realization_command(self, message, args=None) -> None:
        message_dict = message.dict()

        peer_id = message_dict['peer_id']
        chat_id = peer_id - 2000000000
        user_id = message_dict['from_id']

        try:
            await self.punishment.kick(chat_id, user_id)
        except VKAPIError as e:
            if e.code == 15:
                await self._user_admin_chat(peer_id, user_id)
        else:
            await self._user_kick(peer_id, user_id)

    @checked_root_user(started_chat=True)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)