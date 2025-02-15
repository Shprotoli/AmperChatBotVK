from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL

class CSetLvl(AHandlerCommand):
    """Класс для обработки команды `/setlvl`"""
    COMMAND = "setlvl"
    PREFIX = PREFIX_DEFAULT
    ARGS = 2

    def __init__(self, bot: "CApiVK"):
        self.bot = bot
        self.db = DAmperMySQL().lvl_admin_root

    async def _get_id(self, user_info: str) -> int:
        if "|" in user_info: return int(user_info.split("|")[0].replace("[id", ""))

    async def _add_admin_message(self, peer_id: int, user_id: int, admin_lvl_set: int) -> None:
        await self.bot.send_message(peer_id, f"✉ @id{user_id} (Пользователю) успешно были выданы админ-права {admin_lvl_set} уровня")

    async def _error_add_admin_message(self, peer_id: int, user_id: int) -> None:
        await self.bot.send_message(peer_id, f"✉ @id{user_id} (Пользователь) не был найден")

    async def _lvl_admin_root_not_correct_message(self, peer_id: int) -> None:
        await self.bot.send_message(peer_id, f"✉ Уровень админ-прав не должен быть равен или превышать ваш")

    async def _set_admin_root_message(self, peer_id: int, user_id: int, admin_lvl_set: int) -> None:
        await self.bot.send_message(peer_id, f"✉ Вы обновили @id{user_id} (пользователю) уровень админ-прав на {admin_lvl_set}")

    async def _not_correct_arg_message(self, peer_id: int) -> None:
        await self.bot.send_message(peer_id, f"✉ Вы передали аргументы неправильно.\n❓ Пользуйтесь формой: /setlvl user lvl")

    async def _realization_command(self, message, args=None) -> None:
        peer_id = message.peer_id
        chat_id = message.peer_id - 2000000000
        user_id = await self._get_id(args[0])

        try:
            set_lvl_admin = int(args[1])
        except ValueError:
            await self._not_correct_arg_message(peer_id)
            return

        if set_lvl_admin >= 3 or set_lvl_admin < 1:
            await self._lvl_admin_root_not_correct_message(peer_id)
            return

        if user_id:
            check_user_in_db = await self.db.get(user_id, chat_id)

            if check_user_in_db:
                await self.db.update_lvl_admin(user_id, chat_id, set_lvl_admin)
                await self._set_admin_root_message(peer_id, user_id, set_lvl_admin)
            else:
                await self.db.add(user_id, chat_id, set_lvl_admin)
                await self._add_admin_message(peer_id, user_id, set_lvl_admin)
        else:
            await self._error_add_admin_message(peer_id, user_id)

    @checked_root_user(started_chat=True, lvl_admin_root=3)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)