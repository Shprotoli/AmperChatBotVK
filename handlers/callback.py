# -*- coding: utf-8 -*-
"""callback.py - Файл предназначен для обработки callback вызовов"""
from typing import Any

from vkbottle.bot import Bot

from AmperChatBot.handlers.start.welcome import CStartBot

class CCallbackHandler:
    def __init__(self, bot: Bot, api_vk_class):
        self.bot = bot
        self.api_vk_ekz = api_vk_class

        self.start_bot_ekz = CStartBot()

    async def _callback_handler(self, event):
        callback = event['object']
        type_callback = callback['payload']['command']

        match type_callback:
            case "start_bot_chat":
                await self.start_bot_ekz.realization_callback(callback, self.api_vk_ekz)

    async def callback_handler(self, event: dict[str, Any]): await self._callback_handler(event)