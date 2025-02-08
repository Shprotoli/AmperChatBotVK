# -*- coding: utf-8 -*-
"""__main__.py - Основная реализация и запуск бота"""
from vkbottle.bot import Bot
from vkbottle.dispatch.rules.base import ChatActionRule
from vkbottle_types.events import GroupEventType

from _init.config import token, labeler
# HANDLERS
from handlers.callback import CCallbackHandler
from handlers.start.welcome import CJoinGroup
from handlers.api_vk import CApiVK

class AmperBotInit(Bot):
    def __init__(self, token):
        super().__init__(token, labeler=labeler)

        self.join_group_ekz = CJoinGroup()
        self.api_vk_ekz = CApiVK(self)
        self.callback_handler_ekz = CCallbackHandler(self, self.api_vk_ekz)

        self._register_handlers()

    def _register_handlers(self) -> None:
        """Инициализация обработчиков бота"""
        labeler.chat_message(ChatActionRule("chat_invite_user"))(self.join_group_ekz.join_group)
        labeler.raw_event(GroupEventType.MESSAGE_EVENT)(self.callback_handler_ekz.callback_handler)

if __name__ == "__main__":
    bot = AmperBotInit(token)
    bot.run_forever()