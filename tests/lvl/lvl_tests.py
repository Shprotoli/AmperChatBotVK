import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import unittest

from AmperChatBot.handlers.command.free_lvl.lvl.dellvl_handler import CDeleteLevel
from AmperChatBot.tests.test_tool import TApiVK

api = TApiVK()

class TDeleteLevel(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.class_testing = CDeleteLevel(api)

    """functional: parse_user_id"""
    async def test_parse_user_id_success(self):
        user_id = await self.class_testing._parse_user_id("[id12345|Имя]")

        self.assertEqual(user_id, 12345)

    async def test_parse_user_id_incorrect_tag(self):
        user_id = await self.class_testing._parse_user_id("@testincorrect")

        self.assertEqual(user_id, None)

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
