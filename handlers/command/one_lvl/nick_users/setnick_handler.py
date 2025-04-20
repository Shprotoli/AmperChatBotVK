"""setnick_handler.py - Файл для установки ника пользователю"""
from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL
from AmperChatBot.handlers.ENUM.message import ESetNick

class CSetNick(AHandlerCommand):
    """Класс для обработки команды `/setnick`"""
    COMMAND = "setnick"
    PREFIX = PREFIX_DEFAULT
    ARGS = 2
    SEP = "] "
    
    MESSAGES_DICT = {
        'success_set': ESetNick.SUCCESS_SET,
        'success_update': ESetNick.SUCCESS_UPDATE,
        'max_limit': ESetNick.MAX_LIMIT,
        'min_limit': ESetNick.MIN_LIMIT,
    }

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.db = DAmperMySQL().nick_name_db

    async def _check_len_new_nick(self, new_nick: str, peer_id: int) -> bool:
        """
        Функция проверки ника на то, что он не меньше и не больше заданных параметров

        :param new_nick: Новый ник
        :param peer_id: ID чата
        :return:
        """
        if not new_nick or len(new_nick) < 3:
            await self.api.send_messages_by_list(peer_id, user_id=None, messages_list=self.MESSAGES_DICT, status="min_limit")
            return False

        if len(new_nick) > 60:
            await self.api.send_messages_by_list(peer_id, user_id=None, messages_list=self.MESSAGES_DICT, status="max_limit")
            return False

        return True

    async def _is_valid_user(self, args: list, peer_id: int, id_chat: int) -> tuple:
        user_id = await self.api.parse_user_id(args[0])
        new_nick = args[1]

        if not await self._check_len_new_nick(new_nick, peer_id):
            return

        return user_id, new_nick, await self.db.get(id_chat, user_id)

    async def _realization_command(self, message, args=None) -> None:
        peer_id = message.peer_id
        id_chat = message.peer_id - 2000000000
        id_request_user = message.from_id

        user_id, new_nick, check_user_in_db = await self._is_valid_user(args, peer_id, id_chat)

        if check_user_in_db:
            await self.db.update(user_id, id_chat, new_nick)
            await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="success_update", id_request=id_request_user, new_nick=new_nick)
        else:
            await self.db.add(user_id, id_chat, new_nick)
            await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="success_set", new_nick=new_nick)

    @checked_root_user(started_chat=True, lvl_admin_root=1)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)