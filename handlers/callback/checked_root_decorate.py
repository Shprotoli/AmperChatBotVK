from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL

def checked_root_user(started_chat: bool=False):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            peer_id = args[1].dict().get("peer_id")
            if started_chat:
                """
                Проверка на то, что бот уже инициализирован в базе данных (т.е. нажали `старт` в перво сообщении бота)
                    response_chat_init:
                        - `True`: Если бот найден в базе данных (т.е. инициализирован) то проверка пройдена
                        - `False/None`: Если бот не найден в базе данных то возвращаем уведомление
                """
                response_chat_init = await DAmperMySQL().inited_chat_db.get_chat(peer_id)
                if not response_chat_init: return
            return await func(*args, **kwargs)
        return wrapper
    return decorator