"""checked_root_decorate.py - Файл с декоратором для проверки соответствует пользователь, который прописал команду всем критериям"""
from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL

def checked_root_user(started_chat: bool = True, lvl_admin_root: int = False):
    def decorator(func):
        async def wrapper(self, message, args=None, *arg, **kwargs):
            api = self.api
            message_dict = message.dict()

            peer_id = message_dict.get("peer_id")
            chat_id = peer_id - 2000000000
            user_id = message_dict.get("from_id")

            if started_chat:
                """
                Проверка на то, что бот уже инициализирован в базе данных (т.е. нажали `старт` в перво сообщении бота)
                    response_chat_init:
                        - `True`: Если бот найден в базе данных (т.е. инициализирован) то проверка пройдена
                        - `False/None`: Если бот не найден в базе данных то возвращаем уведомление
                """
                response_chat_init = await DAmperMySQL().inited_chat_db.get(peer_id)
                if not response_chat_init:
                    return await api.send_message(peer_id, "❌ Активируйте бота для дальнейшей работы")

            if lvl_admin_root:
                """
                Проверка на то, что у бота есть админ права
                    response_lvl_admin:
                        - `True`: Если у пользователя есть заданный уровень
                        - `None`: Если у пользователя нет заданного уровня
                """
                owner_id = await api._get_creater_chat(peer_id)
                response_lvl_admin = await DAmperMySQL().lvl_admin_root.get_mr(user_id, chat_id, lvl_admin_root)

                if owner_id != user_id and not response_lvl_admin:
                    return await api.send_message(peer_id, "❌ У вас недостаточно прав для использования данной команды")

            return await func(self, message, args, *arg, **kwargs)
        return wrapper
    return decorator