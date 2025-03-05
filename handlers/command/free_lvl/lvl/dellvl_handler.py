"""dellvl_handler.py - Файл для команды с удалением админ-прав"""
from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL

class CDeleteLevel(AHandlerCommand):
    """Класс для обработки команды `/dellvl`"""
    COMMAND = "dellvl"
    PREFIX = PREFIX_DEFAULT
    ARGS = 1
    SEP = None

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.db = DAmperMySQL().lvl_admin_root

    async def _get_id(self, user_info: str) -> int:
        if "|" in user_info: return int(user_info.split("|")[0].replace("[id", ""))

    async def _delete_message(self, peer_id: int, id_user: int) -> None:
        await self.api.send_message(peer_id, f"✉ Вы удалили @id{id_user} (пользователю) админ-права")

    async def _not_delete_message(self, peer_id: int, id_user: int) -> None:
        await self.api.send_message(peer_id, f"⚠ У @id{id_user} (пользователя) нет админ-прав")

    async def _not_access_for_del_message(self, peer_id: int) -> None:
        await self.api.send_message(peer_id, f"⛔ У вас недостаточно админ-прав для удаления админ-прав у данного пользователя")

    async def _delete_root_yourself(self, peer_id: int) -> None:
        await self.api.send_message(peer_id, f"⚠ Вы пытаетесь снять админ-права сами себе")

    async def _check_lvl(self, id_request: int, id_user: int, id_chat: int) -> bool:
        """
        Функция для проверки того, что уровень админ-прав пользователя,
        который удаляет админ-права больше, чем у того, у кого удаляют

        :param id_request: ID того, кто удаляет
        :param id_user: ID того, у кого удаляют
        :param id_chat: ID чата
        :return: Возвращает `bool` в зависимости от ситуации
                - `True`: Если у пользователя отправителя (id_request) админ-права выше,
                          чем у удаляемого (id_user) или пользователь создатель группы
                - `False`: В остальных случаях
        """
        owner_id = await self.api.get_creater_chat(id_chat + 2000000000)

        user_request_db = await self.db.get(id_request, id_chat)
        user_request_db = 0 if not user_request_db else user_request_db.lvl_admin_root

        user_db = await self.db.get(id_user, id_chat)
        user_db = 0 if not user_db else user_db.lvl_admin_root

        if user_request_db <= user_db and id_request != owner_id:
            return False
        else:
            return True

    async def _realization_command(self, message, args=None) -> None:
        id_user = await self._get_id(args[0])
        id_chat = message.chat_id
        peer_id = message.peer_id
        id_request_user = message.from_id

        if id_request_user == id_user:
            await self._delete_root_yourself(peer_id)
            return

        if await self._check_lvl(id_request_user, id_user, id_chat):
            result_db_remove = await self.db.remove(id_user, id_chat)

            if result_db_remove:
                await self._delete_message(peer_id, id_user)
            else:
                await self._not_delete_message(peer_id, id_user)
        else:
            await self._not_access_for_del_message(peer_id)

    @checked_root_user(started_chat=True, lvl_admin_root=3)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)