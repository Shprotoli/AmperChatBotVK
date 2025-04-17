from AmperChatBot.handlers.ERROR.amper_raise import AmperError

class ApiVkError(AmperError):
    """
    Основной класс исключений для класса `CApiVK`
    """
    pass




class SendMessageByList(ApiVkError):
    """
    Класс-шаблон для функции `_send_message_by_list`
    """
    pass

class ManyArgumentAccess(SendMessageByList):
    """
    Исключение, которое вызывается, когда аргументов доступа к элементу контейнера
    по которым осуществляется доступ к елементу списка больше 1, например: `status` или `index`


    ***(1)***
    Пример, когда будет вызвана ошибка:

    ```
    ._send_message_by_list(self,
        peer_id=1000000000,
        user_id=1,
        messages_list={
            'success': EDeleteMessage.SUCCESS,
            'no_rights': EDeleteMessage.NO_RIGHTS,
            'less_rights': EDeleteMessage.LESS_RIGHTS,
            'self_remove': EDeleteMessage.SELF_REMOVE,
            'incorrect_id': EDeleteMessage.INCORRECT_ID,
        },
        status="access",
        index=2,
    ):
    ```

    В данном примере мы передаем и status, и index,
    из-за чего получим ошибку `ManyArgumentAccess`
    """
    pass

class NotArgumentAccess(SendMessageByList):
    """
    Исключение, которое вызывается при отсутствии аргументов
    по которым осуществляется доступ к елементу списка, например: `status` или `index`


    ***(1)***
    Пример, когда будет вызвана ошибка:

    ```
    ._send_message_by_list(self,
        peer_id=1000000000,
        user_id=1,
        messages_list={
            'success': EDeleteMessage.SUCCESS,
            'no_rights': EDeleteMessage.NO_RIGHTS,
            'less_rights': EDeleteMessage.LESS_RIGHTS,
            'self_remove': EDeleteMessage.SELF_REMOVE,
            'incorrect_id': EDeleteMessage.INCORRECT_ID,
        },
        status=None,
        index=None,
    ):
    ```

    В данном примере мы не передаем ни status, ни index,
    из-за чего не сможем обратится к элементу в списке и получим ошибку `NotArgumentAccess`
    """
    pass