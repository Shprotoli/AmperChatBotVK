from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL

class CSetNick(AHandlerCommand):
    """Класс для обработки команды `/help`"""
    COMMAND = "setnick"
    PREFIX = PREFIX_DEFAULT
    ARGS = 2

    TEXT = "💭 Информация о данной беседе:\n\n"

    def __init__(self, bot: "CApiVK"):
        self.bot = bot
        self.db = DAmperMySQL().nick_name_db

    async def _get_id(self, user_info: str) -> int:
        if "|" in user_info: return int(user_info.split("|")[0].replace("id", ""))

    async def _check_len_new_nick(self, new_nick: str, peer_id: int) -> bool:
        """
        Функция проверки ника на то, что он не меньше и не больше заданных параметров

        :param new_nick: Новый ник
        :param peer_id: ID чата
        :return:
        """
        if not new_nick or len(new_nick) < 3:
            await self._small_len_nick_message(peer_id)
            return False

        if len(new_nick) > 60:
            await self._big_len_nick_message(peer_id)
            return False

        return True

    async def _small_len_nick_message(self, peer_id: int) -> None:
        await self.bot.send_message(peer_id, f"✉ Минимальная длинна ника - 3 символа")

    async def _big_len_nick_message(self, peer_id: int) -> None:
        await self.bot.send_message(peer_id, f"✉ Максимальная длинна ника - 60 символов")

    async def _add_nick_message(self, peer_id: int, id_user: int, id_request: int, nick_name: str) -> None:
        await self.bot.send_message(peer_id, f"✉ @id{id_request} (Пользователь) установили @id{id_user} (пользователю) ник - '{nick_name}'")

    async def _set_nick_message(self, peer_id: int, id_user: int, id_request: int, nick_name: str) -> None:
        await self.bot.send_message(peer_id, f"✉ @id{id_request} (Пользователь) обновил @id{id_user} (пользователю) ник на - '{nick_name}'")

    async def _realization_command(self, message, args=None) -> None:
        peer_id = message.peer_id
        id_chat = message.peer_id - 2000000000
        id_request_user = message.from_id

        id_user = await self._get_id(args[0])
        new_nick = args[1]

        if not await self._check_len_new_nick(new_nick, peer_id):
            return

        check_user_in_db = await self.db.get(id_chat, id_user)
        if check_user_in_db:
            await self.db.update(id_user, id_chat, new_nick)
            await self._set_nick_message(peer_id, id_user, id_request_user,  new_nick)
        else:
            await self.db.add(id_user, id_chat, new_nick)
            await self._add_nick_message(peer_id, id_user, id_request_user, new_nick)


    @checked_root_user(started_chat=True, lvl_admin_root=2)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)