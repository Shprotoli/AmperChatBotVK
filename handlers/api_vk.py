"""api_vk.py - Файл предназначенный для работы с API вконтакнте"""
from json import dumps
from typing import Optional

from vkbottle.exception_factory.base_exceptions import VKAPIError
from vkbottle import Bot

from AmperChatBot.handlers.ABC.ABCAmper import AApiVk
from AmperChatBot.handlers.ERROR.ApiVKRaise import NotArgumentAccess, ManyArgumentAccess

class CPunishmentApiVK:
    def __init__(self, bot: "Bot"):
        self.bot = bot

    async def _kick(self, chat_id: int, user_id: int) -> None:
        await self.bot.api.messages.remove_chat_user(chat_id, user_id)

    async def _mute(self, peer_id: int, user_id: int, min: int) -> None:
        await self.bot.api.request(
            "messages.changeConversationMemberRestrictions",
            {
                "peer_id": peer_id,
                "member_ids": user_id,
                "for": min * 60,
                "action": "ro"
            }
        )

    async def _unmute(self, peer_id: int, user_id: int) -> None:
        await self.bot.api.request(
            "messages.changeConversationMemberRestrictions",
            {
                "peer_id": peer_id,
                "member_ids": user_id,
                "action": "rw",
            }
        )


    async def kick(self, chat_id, user_id) -> None: await self._kick(chat_id, user_id)
    async def mute(self, peer_id, user_id, min) -> None: await self._mute(peer_id, user_id, min)
    async def unmute(self, peer_id, user_id) -> None: await self._unmute(peer_id, user_id)

class CApiVK(AApiVk):
    def __init__(self, bot: Bot):
        self.bot = bot

        self._punishment = CPunishmentApiVK(bot)

    async def _parse_user_id(self, user_info: str) -> Optional[int]:
        """Извлекает ID пользователя из строки [id12345|Имя]"""
        if "|" in user_info:
            return int(user_info.split("|")[0].replace("[id", ""))

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

    async def _send_notif(self, peer_id, event_id, user_id, message):
        await self.bot.api.messages.send_message_event_answer(
            event_id=event_id,
            peer_id=peer_id,
            user_id=user_id,
            event_data=dumps({"type": "show_snackbar", "text": message}),
        )

    async def _send_message_by_list(self, peer_id, user_id, messages_list, status, index, id_request, admin_lvl_set):
        if not any([status, index]):
            raise NotArgumentAccess("Not passed argument access in functional")

        if sum([bool(status), bool(index)]) > 1:
            raise ManyArgumentAccess("Many passed argument access in functional")

        if index:
            return await self._send_message(peer_id, list(messages_list.values())[index].value.format(
                admin_lvl_set=admin_lvl_set,
                id_request=id_request,
                user_id=user_id,
            ))
        await self._send_message(peer_id, messages_list[status].value.format(
            admin_lvl_set=admin_lvl_set,
            id_request=id_request,
            user_id=user_id,

        ))


    async def _send_message(self, peer_id, message_text):
        await self.bot.api.messages.send(
            peer_id=peer_id,
            message=message_text,
            random_id=0
        )

    async def _get_info_chat(self, peer_id):
        return await self.bot.api.messages.get_conversations_by_id(peer_ids=peer_id)

    async def _get_info_user(self, user_id):
        return await self.bot.api.users.get(user_ids=user_id, fields=["first_name", "last_name"])

    async def _get_users_online(self, peer_id):
        conversation_members = await self.bot.api.messages.get_conversation_members(peer_id=peer_id)

        profiles = conversation_members.profiles

        online_user_ids = [
            profile.id
            for profile in profiles
            if profile.online_info.is_online
        ]

        return online_user_ids

    @property
    def punishment(self) -> "CPunishmentApiVK": return self._punishment


    async def get_creater_chat(self, peer_id): return await self._get_creater_chat(peer_id)
    async def get_users_online(self, peer_id): return await self._get_users_online(peer_id)
    async def is_creater_chat(self, id_user, peer_id): return id_user == await self._get_creater_chat(peer_id)
    async def bot_is_admin_in_chat(self, peer_id): return await self._bot_is_admin_in_chat(peer_id)
    async def edit_message_chat(self, peer_id, conversation_message_id, message, keyboard=None):
        await self._edit_message_chat(peer_id, conversation_message_id, message, keyboard)
    async def send_notif(self, peer_id, event_id, user_id, message): await self._send_notif(peer_id, event_id, user_id, message)
    async def send_message(self, peer_id, message_text): await self._send_message(peer_id, message_text)
    async def send_messages_by_list(self, peer_id, user_id, messages_list, status=None, index=None, id_request=None, admin_lvl_set=None):
        await self._send_message_by_list(peer_id, user_id, messages_list, status, index, id_request, admin_lvl_set)
    async def get_info_chat(self, peer_id): return await self._get_info_chat(peer_id)
    async def get_info_user(self, user_id): return await self._get_info_user(user_id)
    async def parse_user_id(self, user_info): return await self._parse_user_id(user_info)