"""api_vk.py - Файл предназначенный для работы с API вконтакнте"""
from json import dumps

from vkbottle import Bot
from vkbottle.exception_factory.base_exceptions import VKAPIError

from AmperChatBot.handlers.ABC.ABCAmper import AApiVk

class CApiVK(AApiVk):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _get_creater_chat(self, peer_id):
        try:
            response = await self.bot.api.messages.get_conversation_members(peer_id=peer_id)

            for member in response.items:
                member_dict = member.dict()
                if member_dict['is_owner']: return member_dict['member_id']

        except VKAPIError as e:
            if e.code == 917:
                return

    async def _bot_is_admin_in_chat(self, peer_id):
        try:
            await self.bot.api.messages.get_conversation_members(peer_id=peer_id)
            return True
        except VKAPIError as e:
            if e.code == 917:
                return False

    async def _edit_message_chat(self, peer_id, conversation_message_id, message, keyboard):
        await self.bot.api.messages.edit(
           peer_id=peer_id,
           conversation_message_id=conversation_message_id,
           message=message,
           keyboard=keyboard,
        )

    import json

    async def _send_notif(self, peer_id, event_id, user_id, message):
        await self.bot.api.messages.send_message_event_answer(
            event_id=event_id,
            peer_id=peer_id,
            user_id=user_id,
            event_data=dumps({"type": "show_snackbar", "text": message}),
        )

    async def get_creater_chat(self, peer_id): return await self._get_creater_chat(peer_id)

    async def is_creater_chat(self, id_user, peer_id): return id_user == await self._get_creater_chat(peer_id)

    async def bot_is_admin_in_chat(self, peer_id): return await self._bot_is_admin_in_chat(peer_id)

    async def edit_message_chat(self, peer_id, conversation_message_id, message, keyboard): await self._edit_message_chat(peer_id, conversation_message_id, message, keyboard)

    async def send_notif(self, peer_id, event_id, user_id, message): await self._send_notif(peer_id, event_id, user_id, message)