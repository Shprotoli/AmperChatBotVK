from dotenv import load_dotenv
from os import getenv

load_dotenv()
token = getenv("TOKEN")

from vkbottle.bot import BotLabeler
labeler = BotLabeler()