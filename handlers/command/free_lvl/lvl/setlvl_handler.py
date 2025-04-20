"""setlvl_handler.py - Файл для команды с добавлением админ-прав"""
from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT
from AmperChatBot.handlers.api_vk import CApiVK
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL
from AmperChatBot.handlers.ENUM.message import ESetLvlessage

class CSetLvl(AHandlerCommand):
    """Класс для обработки команды `/setlvl`"""
    COMMAND = "setlvl"
    PREFIX = PREFIX_DEFAULT
    ARGS = 2
    SEP = None
    
    MESSAGES_DICT = {
        'success_set': ESetLvlessage.SUCCESS_SET,
        'success_update': ESetLvlessage.SUCCESS_UPDATE,
        'not_in_chat': ESetLvlessage.NOT_IN_CHAT,
        'eq_or_more': ESetLvlessage.EQ_OR_MORE,
        'self_set': ESetLvlessage.SELF_SET,
        'incorrect_arg': ESetLvlessage.INCORRECT_ARG,
    }

    def __init__(self, api: "CApiVK"):
        self.api = api
        self.db = DAmperMySQL().lvl_admin_root

    async def _check_range_admin_root(self, owner_id: int, user_id: int, request_user_id: int, set_lvl_admin: int, peer_id: int) -> bool:
        """
        Функция проверки то, что уровень, который пытаемся установить
        не больше и не меньше заданных параметров

        :param owner_id: ID владельца чата
        :param request_user_id: ID пользователя, который написал команду
        :param set_lvl_admin: Уровень, который хотим установить
        :param peer_id: ID чата
        :return: Возвращает `bool` в зависимости от ситуации:
                - `False`: Если пользователь, который удаляет (request_user_id) не является владельцем чата (owner_id)
                          и мы устанавливаем 3 уровень админ-прав или устанавливаемый уровень админ-прав (set_lvl_admin)
                          превышает 4 или меньше 1
                - `True`: В остальных случаях
        """
        if owner_id != request_user_id and set_lvl_admin == 3 or set_lvl_admin >= 4 or set_lvl_admin < 1:
            await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="eq_or_more")
            return False
        return True

    async def _is_valid_user(self, args: list, owner_id: int, peer_id: int, id_request_user: int) -> tuple:
        user_id = await self.api.parse_user_id(args[0])
        try:
            set_lvl_admin = int(args[1])
        except ValueError:
            await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="incorrect_arg")
            return [None, None]

        if not await self._check_range_admin_root(owner_id, user_id, id_request_user, set_lvl_admin, peer_id):
            return [None, None]

        if id_request_user == user_id:
            await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="self_set")
            return [None, None]

        return set_lvl_admin, user_id

    async def _realization_command(self, message, args=None) -> None:
        peer_id = message.peer_id
        chat_id = message.peer_id - 2000000000
        owner_id = await self.api.get_creater_chat(peer_id)
        id_request_user = message.from_id

        set_lvl_admin, user_id = await self._is_valid_user(args, owner_id, peer_id, id_request_user)

        if user_id:
            check_user_in_db = await self.db.get_in_chat(user_id, chat_id)

            if check_user_in_db:
                await self.db.update_lvl_admin(user_id, chat_id, set_lvl_admin)
                await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="success_update",
                                                     admin_lvl_set=set_lvl_admin, id_request=id_request_user
                                                     )
            else:
                await self.db.add(user_id, chat_id, set_lvl_admin)
                await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="success_set",
                                                     admin_lvl_set=set_lvl_admin
                                                     )
        else:
            await self.api.send_messages_by_list(peer_id, user_id, self.MESSAGES_DICT, status="not_in_chat")

    @checked_root_user(started_chat=True, lvl_admin_root=3)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)