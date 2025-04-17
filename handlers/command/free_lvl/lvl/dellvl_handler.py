"""dellvl_handler.py - Файл для команды с удалением админ-прав"""
from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL
from AmperChatBot.handlers.ENUM.message import EDeleteMessage

class CDeleteLevel(AHandlerCommand):
    """Класс для обработки команды `/dellvl`"""
    COMMAND = "dellvl"
    PREFIX = PREFIX_DEFAULT
    ARGS = 1
    SEP = None

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.db = DAmperMySQL().lvl_admin_root

    async def _send_message(self, peer_id: int, user_id: int = None, status: str = "") -> None:
        messages = {
            'success': EDeleteMessage.SUCCESS,
            'no_rights': EDeleteMessage.NO_RIGHTS,
            'less_rights': EDeleteMessage.LESS_RIGHTS,
            'self_remove': EDeleteMessage.SELF_REMOVE,
            'incorrect_id': EDeleteMessage.INCORRECT_ID,
        }
        await self.api.send_message(peer_id, messages[status].value.format(user_id=user_id))

    async def _has_permission_to_remove(self, id_request: int, user_id: int, id_chat: int) -> bool:
        """
        Функция для проверки того, что уровень админ-прав пользователя,
        который удаляет админ-права больше, чем у того, у кого удаляют

        :param id_request: ID того, кто удаляет
        :param user_id: ID того, у кого удаляют
        :param id_chat: ID чата
        :return: Возвращает `bool` в зависимости от ситуации
                - `True`: Если у пользователя отправителя (id_request) админ-права выше,
                          чем у удаляемого (user_id) или пользователь создатель группы
                - `False`: В остальных случаях
        """
        owner_id = await self.api.get_creater_chat(id_chat + 2_000_000_000)

        user_request_db = await self.db.get_in_chat(id_request, id_chat)
        user_request_admin_lvl = 0 if not user_request_db else user_request_db.lvl_admin_root

        user_target_db = await self.db.get_in_chat(user_id, id_chat)
        user_target_admin_lvl = 0 if not user_target_db else user_target_db.lvl_admin_root

        if user_request_admin_lvl <= user_target_admin_lvl and id_request != owner_id:
            return False
        return True

    async def _is_valid_user(self, user_string: str, peer_id: int, id_request_user: int) -> bool:
        user_id = await self.api.parse_user_id(user_string)

        if not user_id:
            await self._send_message(peer_id, user_id, status="incorrect_id")
            return False

        if id_request_user == user_id:
            await self._send_message(peer_id, user_id, status="self_remove")
            return False
        return user_id

    async def _realization_command(self, message, args=None) -> None:
        user_string = args[0]
        id_chat = message.chat_id
        peer_id = message.peer_id
        id_request_user = message.from_id

        user_id = await self._is_valid_user(user_string, peer_id, id_request_user)
        if not user_id: return

        if await self._has_permission_to_remove(id_request_user, user_id, id_chat):
            result_db_remove = await self.db.remove_in_chat(user_id, id_chat)

            if result_db_remove:
                await self._send_message(peer_id, user_id, status="success")
            else:
                await self._send_message(peer_id, user_id, status="no_rights")
        else:
            await self._send_message(peer_id, user_id, status="less_rights")

    @checked_root_user(started_chat=True, lvl_admin_root=3)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)