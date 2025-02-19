from random import randint
from typing import Optional

from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK

class CRandom(AHandlerCommand):
    """Класс для обработки команды `/q`"""
    COMMAND = "random"
    PREFIX = PREFIX_DEFAULT
    ARGS = 2
    SEP = None

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.punishment = api.punishment

    async def _send_generate_value_message(self, message, user_id: int, value: int):
        await message.answer(f"🤖 @id{user_id} (Пользователю) выпало число: {value}")

    async def _error_generate_value_message(self, message, user_id: int) -> None:
        await message.answer(f"⚠ @id{user_id} (Вы) должны передать два числовых параметра в порядке возрастания\n"
                             f"❓ Например: /random 0 10")

    async def _generate_value(self, args) -> Optional[int]:
        """
        Генерация числа в диапазоне, который передается в `args` пользователем

        :param args: Аргументы, который передал пользователь в сообщении
        :return: Возвращает значения в зависимости от ситуации
                - `int`: Если параметры переданы правильно, то возвращает сгенерированное число
                - `None`: Если параметры переданы неправильно
                         (например не числа, а буквы или не в порядке возрастания)
        """
        try:
            one_param, two_param = int(args[0]), int(args[1])
            return randint(one_param, two_param)
        except ValueError:
            return

    async def _realization_command(self, message, args=None) -> None:
        used_id = message.from_id
        generate_value = await self._generate_value(args)

        if generate_value:
            await self._send_generate_value_message(message, used_id, generate_value)
        else:
            await self._error_generate_value_message(message, used_id)

    @checked_root_user(started_chat=True)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)