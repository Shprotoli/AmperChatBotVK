from typing import Union

from vkbottle_types.responses.messages import MessagesGetConversationByIdExtended, MessagesGetConversationById

from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK

class CInfo(AHandlerCommand):
    """Класс для обработки команды `/help`"""
    COMMAND = "info"
    PREFIX = PREFIX_DEFAULT
    ARGS = 0
    SEP = None

    def __init__(self, api: "CApiVK"):
        self.api = api

    async def _get_setting_chat(self, response: Union[MessagesGetConversationByIdExtended, MessagesGetConversationById]) -> None:
        """
        Функция для установки в переменную `TEXT` текст с информацией о текущем чате

        :param response: Информация о беседе
        :return: None
        """
        chat_setting = response.items[0].chat_settings

        title = chat_setting.title
        id_chat = response.items[0].peer.id - 2000000000
        user_count = len(chat_setting.active_ids) + 1
        admin_count = len(chat_setting.admin_ids) + 1
        owner_chat = f"https://vk.com/id{chat_setting.owner_id}"

        text = "💭 Информация о данной беседе:\n\n"
        text += f"💬 Название беседы: {title}\n"
        text += f"🆔 ID чата: {id_chat}\n"
        text += f"👥 Пользователей в беседе: {user_count}\n"
        text += f"👤 Администраторов в беседе (со звездой): {admin_count}\n"
        text += f"🔗 Владелец беседы: {owner_chat}"

        return text

    async def _realization_command(self, message, args=None) -> None:
        response = await self.api.get_info_chat(message.peer_id)

        text = await self._get_setting_chat(response)
        await message.answer(text)

    @checked_root_user(started_chat=True)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)