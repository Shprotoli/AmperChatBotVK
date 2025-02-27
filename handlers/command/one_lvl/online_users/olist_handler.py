"""nlist_handler.py - Файл для команды со списком пользователей онлайн"""
from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL

class COnlineList(AHandlerCommand):
    """Класс для обработки команды `/olist`"""
    COMMAND = "olist"
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

    async def _get_text_users_online(self, peer_id: int, id_chat: int) -> str:
        """Функция для генерации текста с пользователями онлайн

        :param peer_id: ID чата (в формате 2000000000)
        :param id_chat: ID чата (чистый id)
        :return: Возвращает `str` с текстом о пользователях онлайн
        """
        list_users_with_nick = await self._get_users_with_nick(id_chat)
        list_users_online = await self.api.get_users_online(peer_id)

        text_return = "👥 Список пользователей онлайн\n\n"

        id_counter = 1

        for user in list_users_with_nick:
            if user.id_user in list_users_online:
                user_nick = user.nick
                id_user = user.id_user

                full_name = await self._get_name_user(id_user)

                text_return += f"{id_counter}. {user_nick} - @id{id_user} ({full_name})\n"
                id_counter += 1
                list_users_online.remove(user.id_user)

        for id_user in list_users_online:
            full_name = await self._get_name_user(id_user)
            text_return += f"{id_counter}. @id{id_user} ({full_name})\n"
            id_counter += 1

        return text_return

    async def _realization_command(self, message, args=None) -> None:
        peer_id = message.peer_id
        id_chat = message.peer_id - 2000000000

        text_return = await self._get_text_users_online(peer_id, id_chat)
        await self.api.send_message(peer_id, text_return)

    @checked_root_user(started_chat=True, lvl_admin_root=1)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)