from AmperChatBot.handlers.callback.checked_root_decorate import checked_root_user
from AmperChatBot.handlers.ABC.ABCAmper import AHandlerCommand
from AmperChatBot.handlers.command.config_command import PREFIX_DEFAULT

class CInfo(AHandlerCommand):
    """Класс для обработки команды `/help`"""
    COMMAND = "info"
    PREFIX = PREFIX_DEFAULT
    ARGS = 0

    TEXT = (
        "💭 Информация о данной беседе:"
    )

    def __init__(self, bot):
        self.bot = bot

    async def _realization_command(self, message, args=None) -> None:
        await message.answer(self.TEXT)

    @checked_root_user(started_chat=True)
    async def realization_command(self, message, args=None) -> None: await self._realization_command(message, args)