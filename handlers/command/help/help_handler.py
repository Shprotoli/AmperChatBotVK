"""help_handler.py - Файл, который содержит всю информацию связанную с командой `help`"""
from vkbottle import Keyboard, KeyboardButtonColor, Callback, Bot

from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import ACallbackHandler
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT

async def get_lvl_setting(lvl: int) -> tuple:
    """Функция возвращает клавиатуру и текст для выбранного уровня"""
    keyboard = (
        Keyboard(inline=True)
        .add(Callback("Без уровня", payload={"command": "zero_lvl"}), color=KeyboardButtonColor.POSITIVE if lvl == 0 else KeyboardButtonColor.SECONDARY)
        .add(Callback("1 уровень", payload={"command": "one_lvl"}), color=KeyboardButtonColor.POSITIVE if lvl == 1 else KeyboardButtonColor.SECONDARY)
        .row()
        .add(Callback("2 уровень", payload={"command": "two_lvl"}), color=KeyboardButtonColor.POSITIVE if lvl == 2 else KeyboardButtonColor.SECONDARY)
        .add(Callback("3 уровень", payload={"command": "free_lvl"}), color=KeyboardButtonColor.POSITIVE if lvl == 3 else KeyboardButtonColor.SECONDARY)
    )

    match lvl:
        case 0:
            text_lvl = (
                "📒 В этом разделе вы можете посмотреть все доступные команды на разных уровнях админ-прав.\n\n"
                "⚡ Команды для пользователя без админ-прав:\n\n"
                "/help - Просмотр списка команд"
            )
        case 1:
            text_lvl = (
                "📒 В этом разделе вы можете посмотреть все доступные команды на разных уровнях админ-прав.\n\n"
                "⚡ Команды для пользователя 1 уровня админ-прав:\n\n"
            )
        case 2:
            text_lvl = (
                "📒 В этом разделе вы можете посмотреть все доступные команды на разных уровнях админ-прав.\n\n"
                "⚡ Команды для пользователя 2 уровня админ-прав:\n\n"
            )
        case 3:
            text_lvl = (
                "📒 В этом разделе вы можете посмотреть все доступные команды на разных уровнях админ-прав.\n\n"
                "⚡ Команды для пользователя 3 уровня админ-прав:\n\n"
            )
        case _:
            text_lvl = (
                "📒 В этом разделе вы можете посмотреть все доступные команды на разных уровнях админ-прав.\n\n"
                "⚡ Команды для пользователя без админ-прав:\n\n"
                "/help - Просмотр списка команд"
            )

    return text_lvl, keyboard

class CLvlInformation(ACallbackHandler):
    """Класс для обработки события нажатия на кнопку в `/help`, для просмотра прав уровней админ-прав"""
    async def _set_author_callback(self) -> None:
        """
        Установка параметров пользователя который подал callback запрос в self-переменные класса

        :return: None
        """
        self.peer_id = self.information_callback['peer_id']
        self.user_id = self.information_callback['user_id']
        self.event_id = self.information_callback['event_id']
        self.conversation_message_id = self.information_callback['conversation_message_id']

    async def _realization_callback_lvl_zero(self):
        """
        Реализация callback ответа на запрос с информацией 0 уровня

        :return: None
        """
        await self._set_author_callback()
        text_lvl, keyboard = await get_lvl_setting(0)

        await self.api_vk_class.edit_message_chat(self.peer_id, self.conversation_message_id, message=text_lvl, keyboard=keyboard)

    async def _realization_callback_lvl_one(self):
        """
        Реализация callback ответа на запрос с информацией 1 уровня

        :return: None
        """
        await self._set_author_callback()
        text_lvl, keyboard = await get_lvl_setting(1)

        await self.api_vk_class.edit_message_chat(self.peer_id, self.conversation_message_id, message=text_lvl, keyboard=keyboard)

    async def _realization_callback_lvl_two(self):
        """
        Реализация callback ответа на запрос с информацией 2 уровня

        :return: None
        """
        await self._set_author_callback()
        text_lvl, keyboard = await get_lvl_setting(2)

        await self.api_vk_class.edit_message_chat(self.peer_id, self.conversation_message_id, message=text_lvl, keyboard=keyboard)

    async def _realization_callback_lvl_free(self):
        """
        Реализация callback ответа на запрос с информацией 3 уровня

        :return: None
        """
        await self._set_author_callback()
        text_lvl, keyboard = await get_lvl_setting(3)

        await self.api_vk_class.edit_message_chat(self.peer_id, self.conversation_message_id, message=text_lvl, keyboard=keyboard)


    async def realization_callback_lvl_zero(self): await self._realization_callback_lvl_zero()
    async def realization_callback_lvl_one(self): await self._realization_callback_lvl_one()
    async def realization_callback_lvl_two(self): await self._realization_callback_lvl_two()
    async def realization_callback_lvl_free(self): await self._realization_callback_lvl_free()

    async def _realization_callback(self, information_callback, api_vk_class):
        """
        В данном классе данная функция отвечает за начальную инициализацию следующих объектов
            - `api_vk_class`: Для управления API VK из класса
            - `information_callback`: Информация о текущем callback
        """
        self.api_vk_class = api_vk_class
        self.information_callback = information_callback

    async def realization_callback(self, information_callback, api_vk_class): await self._realization_callback(information_callback, api_vk_class)

class CHelp(AHandlerCommand):
    """Класс для обработки команды `/help`"""
    COMMAND = "help"
    PREFIX = PREFIX_DEFAULT
    ARGS = 0

    def __init__(self, bot: Bot):
        self.bot = bot

    async def _realization_command(self, message, args=None) -> None:
        text_lvl, keyboard = await get_lvl_setting(0)
        await message.answer(text_lvl, keyboard=keyboard)

    @checked_root_user(started_chat=True)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)