from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL

class CNickList(AHandlerCommand):
    """Класс для обработки команды `/nlist`"""
    COMMAND = "nlist"
    PREFIX = PREFIX_DEFAULT
    ARGS = 0
    SEP = None

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.db = DAmperMySQL().nick_name_db

    async def _get_users_with_nick(self, id_chat: int) -> list: return await self.db.get_more(id_chat)

    async def _get_name_user(self, id_user: int) -> str:
        """
        Функция, которая возвращает полное имя пользователя (`first_name` + `last_name`)

        :param id_user: ID пользователя
        :return:
        """
        info_about_user = await self.api.get_info_user(id_user)
        info_about_user_dict = info_about_user[0].dict()

        first_name = info_about_user_dict.get("first_name")
        last_name = info_about_user_dict.get("last_name")

        return first_name + " " + last_name

    async def _realization_command(self, message, args=None) -> None:
        peer_id = message.peer_id
        id_chat = message.peer_id - 2000000000
        list_user_with_nick = await self._get_users_with_nick(id_chat)

        text_return = "👥 Список пользователей с ником\n\n"

        for id, user in enumerate(list_user_with_nick):
            user_nick = user.nick
            id_user = user.id_user

            full_name = await self._get_name_user(id_user)

            text_return += f"{id + 1}. {user_nick} - @id{id_user} ({full_name})\n"

        await self.api.send_message(peer_id, text_return)

    @checked_root_user(started_chat=True, lvl_admin_root=2)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)