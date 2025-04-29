"""staff.py - Файл для команды со списком пользователей с правами администратора"""
from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL

class CStaffList(AHandlerCommand):
    """Класс для обработки команды `/staff`"""
    DIR = "../../handlers/command/one_lvl/staff_users/staff_handler.py"
    COMMAND = "staff"
    PREFIX = PREFIX_DEFAULT
    ARGS = 0
    SEP = None

    def __init__(self, api: "CApiVK"):
        self.api = api

        self.db = DAmperMySQL()
        self.db_staff = self.db.lvl_admin_root
        self.db_nick = self.db.nick_name_db

    async def _get_users_with_nick(self, id_chat: int) -> list: return await self.db_nick.get_more(id_chat)

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

    async def _get_owner_text(self, peer_id: int) -> list[int, str]:
        """Функция для генерации текста о владельце чата под вставку в функцию '_get_text_users_staff' """
        owner_id_user = await self.api.get_creater_chat(peer_id)
        full_name = await self._get_name_user(owner_id_user)

        return owner_id_user, f"Владелец беседы 👑: @id{owner_id_user} ({full_name})\n\n"

    async def _get_emoji_lvl(self, lvl_admin_root: int) -> str:
        """Возвращает эмодзи, которое подходит по уровню администратора"""
        return {
            1: "✏",
            2: "💣",
            3: "🍺",
        }[lvl_admin_root]

    async def _get_text_users_staff(self, peer_id: int, id_chat: int) -> str:
        """Функция для генерации текста с пользователями онлайн

        :param id_chat: ID чата (чистый id)
        :return: Возвращает `str` с текстом о пользователях онлайн
        """
        list_users_with_nick = {user.id_user: user for user in await self._get_users_with_nick(id_chat)}
        list_users_staff = await self.db_staff.get_more_in_chat(id_chat, 1)

        text_return = "👁️‍🗨️ Список пользователей с админ-правами\n\n"

        owner_id, text_owner = await self._get_owner_text(peer_id)
        text_return += text_owner

        for id, admin_info in enumerate(list_users_staff):
            id_user, lvl_admin_root = admin_info.id_user, admin_info.lvl_admin_root
            emoji_lvl = await self._get_emoji_lvl(lvl_admin_root)

            if id_user == owner_id: continue

            if id_user in list_users_with_nick:
                info_admin_nick = list_users_with_nick[id_user]
                text_return += f"{id+1}. @id{id_user} ({info_admin_nick.nick}) - {lvl_admin_root} уровень {emoji_lvl}\n"
            else:
                full_name = await self._get_name_user(id_user)
                text_return += f"{id+1}. @id{id_user} ({full_name}) - {lvl_admin_root} уровень {emoji_lvl}\n"
        return text_return

    async def _realization_command(self, message, args=None) -> None:
        peer_id = message.peer_id
        id_chat = peer_id - 2000000000

        text_return = await self._get_text_users_staff(peer_id, id_chat)
        await self.api.send_message(peer_id, text_return)

    @checked_root_user(started_chat=True, lvl_admin_root=1)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)