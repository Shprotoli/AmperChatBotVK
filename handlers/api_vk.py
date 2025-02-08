"""api_vk.py - Файл предназначенный для работы с API вконтакнте"""
from vkbottle import Bot
from vkbottle.exception_factory.base_exceptions import VKAPIError

from AmperChatBot.handlers.ABC.ABCAmper import AApiVk

class CApiVK(AApiVk):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def get_creater_group(self, peer_id):
        try:
            await self.bot.api.messages.get_conversation_members(peer_id=peer_id)
        except VKAPIError as e:
            if e.code == 917:
                return