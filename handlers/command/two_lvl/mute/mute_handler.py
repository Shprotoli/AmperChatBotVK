"""mute_handler.py - Файл для реализации выдачи мута"""
from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL

class CMute(AHandlerCommand):
    """Класс для обработки команды `/mute`"""
    COMMAND = "mute"
    PREFIX = PREFIX_DEFAULT
    ARGS = 2
    SEP = None

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.db = DAmperMySQL().mute_db

    async def _not_correct_min_message(self, peer_id: int, request_user_id: int) -> None:
        await self.api.send_message(peer_id, f"⚠ @id{request_user_id} (Вы) неправильно передали аргументы\n"
                                             f"❓ Например: /mute @id1 1")

    async def _mute_message(self, peer_id: int, user_id: int, min: int) -> None:
        if min == 1:
            text_minute = "минуту"
        elif min in [2, 3, 4]:
            text_minute = "минуты"
        else:
            text_minute = "минут"

        await self.api.send_message(peer_id, f"✉ @id{user_id} (Пользователь) получил мут на {min} {text_minute}")

    async def _realization_command(self, message, args=None) -> None:
        request_user_id = message.from_id
        user_id = await self.api.parse_user_id(args[0])
        peer_id = message.peer_id
        try:
            minute_mute = int(args[1])

            await self.api.punishment.mute(peer_id, user_id, minute_mute)
            await self._mute_message(peer_id, user_id, minute_mute)
        except ValueError:
            await self._not_correct_min_message(peer_id, request_user_id)

    @checked_root_user(started_chat=True, lvl_admin_root=2)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)