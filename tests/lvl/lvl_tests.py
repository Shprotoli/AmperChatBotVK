from os import system

import unittest

from AmperChatBot.handlers.command.free_lvl.lvl.dellvl_handler import CDeleteLevel
from AmperChatBot.tests.test_tool import TApiVK
from AmperChatBot.tests.config_test import CONFIG_FILE_POETRY

API = TApiVK()

class TDeleteLevel(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        system(f"mypy {CONFIG_FILE_POETRY}{CDeleteLevel.DIR}")

    async def asyncSetUp(self):
        self.class_testing = CDeleteLevel(API)

    """functional: valid_user"""
    async def test_valid_user_success(self):
        user_id = await self.class_testing._is_valid_user("[id12345|Имя]", 1, 2)

        self.assertEqual(user_id, 12345)

    async def test_valid_user_incorrect_tag(self):
        """
        Функция для проверки, как отреагирует метод, на неправильный формат
        в аргументе `user_string`
        """
        user_id = await self.class_testing._is_valid_user("@testincorrect", 1, 2)

        self.assertEqual(user_id, False)

    async def test_valid_user_self_check(self):
        """
        Функция для проверки, как отреагирует метод,
        на одинаковые id пользователя кто запрашивает, и на кого запрашивают проверку
        """
        user_id = await self.class_testing._is_valid_user("[id12345|Имя]", 1, 12345)

        self.assertEqual(user_id, False)

if __name__ == '__main__':
    unittest.main()