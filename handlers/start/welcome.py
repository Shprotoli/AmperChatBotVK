# -*- coding: utf-8 -*-
"""welcome.py - Файл предназначен для обработки команд связанных с вступлением бота в группу"""
from vkbottle.bot import Message, Bot
from vkbottle import Keyboard, KeyboardButtonColor, Callback

from AmperChatBot.handlers.ABC.ABCAmper import ACallbackHandler

class CStartBot(ACallbackHandler):
    async def realization_callback(self, information_callback, api_vk_class):
        peer_id = information_callback['peer_id']
        conversation_message_id = information_callback['conversation_message_id']

        await api_vk_class.get_creater_group(peer_id)

        #await bot.api.messages.edit(
        #    peer_id=peer_id,
        #    conversation_message_id=conversation_message_id,
        #    message="Это обновлённое сообщение!"
        #)

class CJoinGroup:
    TEXT_JOIN_MESSAGE = (
        "Привет! Amper теперь в вашей беседе 🥳\n\n"
        "Для дальнейшей работы нужно дать боту права администратора, а затем нажать кнопку 'Старт' 🚀"
    )

    KEYBOARD_START = (
        Keyboard(inline=True)
        .add(Callback("Старт", payload={"command": "start_bot_chat"}), color=KeyboardButtonColor.POSITIVE)
    )

    async def join_group(self, message: Message): await message.answer(self.TEXT_JOIN_MESSAGE, keyboard=self.KEYBOARD_START)