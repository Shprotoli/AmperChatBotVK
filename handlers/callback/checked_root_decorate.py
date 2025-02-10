from AmperChatBot.handlers.DB.amper_mysql import DAmperMySQL

def checked_root_user(started_chat: bool=False):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            peer_id = args[1].dict().get("peer_id")
            if started_chat:
                """
                �������� �� ��, ��� ��� ��� ��������������� � ���� ������ (�.�. ������ `�����` � ����� ��������� ����)
                    response_chat_init:
                        - `True`: ���� ��� ������ � ���� ������ (�.�. ���������������) �� �������� ��������
                        - `False/None`: ���� ��� �� ������ � ���� ������ �� ���������� �����������
                """
                response_chat_init = await DAmperMySQL().inited_chat_db.get_chat(peer_id)
                if not response_chat_init: return
            return await func(*args, **kwargs)
        return wrapper
    return decorator