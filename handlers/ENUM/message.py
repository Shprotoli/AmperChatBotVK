from enum import Enum

class EDeleteLvlMessage(Enum):
    SUCCESS = "✉ Вы удалили @id{user_id} (пользователю) админ-права"
    NO_RIGHTS = "⚠ У @id{user_id} (пользователя) нет админ-прав"
    LESS_RIGHTS = "⛔ У вас недостаточно админ-прав для удаления админ-прав у данного пользователя"
    SELF_REMOVE = "⚠ Вы пытаетесь снять админ-права сами себе"
    INCORRECT_ID = "⚠ Вы указали неправильного пользователя"

class ESetLvlessage(Enum):
    SUCCESS_SET = "✉ @id{user_id} (Пользователю) успешно были выданы админ-права {admin_lvl_set} уровня"
    SUCCESS_UPDATE = "✉ @id{id_request} (Пользователь) обновил @id{user_id} (пользователю) уровень админ-прав на {admin_lvl_set}"
    NOT_IN_CHAT = "⛔ @id{user_id} (Пользователь) не был найден в чате"
    EQ_OR_MORE = "⚠ Уровень админ-прав не должен быть равен или превышать ваш"
    SELF_SET = "⚠ Вы пытаетесь установить админ-права сами себе"
    INCORRECT_ARG = "⛔ Вы неправильно передали аргументы.\n❓ Пользуйтесь формой: /setlvl user lvl"

class EKickMessage(Enum):
    SUCCESS = "👀 @id{user_id} (Пользователя) выкидывают с этой вечеринки"
    NOT_IN_CHAT = "⛔ @id{user_id} (Пользователя) нет в данном чате"

class EGetNick(Enum):
    SUCCESS = "✉ Ник @id{user_id} (пользователя) - {new_nick}"
    NO_NICK = "✉ У @id{user_id} (пользователя) нет ника"