from enum import Enum

class EDeleteMessage(Enum):
    SUCCESS = "✉ Вы удалили @id{user_id} (пользователю) админ-права"
    NO_RIGHTS = "⚠ У @id{user_id} (пользователя) нет админ-прав"
    LESS_RIGHTS = "⛔ У вас недостаточно админ-прав для удаления админ-прав у данного пользователя"
    SELF_REMOVE = "⚠ Вы пытаетесь снять админ-права сами себе"
    INCORRECT_ID = "⚠ Вы указали неправильного пользователя"