import unittest
from core.db.mongo_db.mongo_db_facade import MongoDBFacade
from .password_module import PasswordModule
from core.entities.user_dto import UserDto


class TestPasswordModule(unittest.TestCase):
    def setUp(self):
        user_controller = MongoDBFacade()
        self.auth_module = PasswordModule(user_controller)

    # Should return user dto if names and password compares
    def test_login_true(self):
        test_user = self.auth_module.login("test_user", "1111")
        self.assertIsNotNone(test_user)

    # Should return None if names and password not compares
    def test_login_false(self):
        test_user = self.auth_module.login("test_user", "1234")
        self.assertIsNone(test_user)

    # Should return true if user exist
    def test_check_user_exist_true(self):
        is_exist = self.auth_module.check_user_exist("test_user")
        self.assertTrue(is_exist)

    # Should return false if user don't exist
    def test_check_user_exist_false(self):
        is_exist = self.auth_module.check_user_exist("smart_user")
        self.assertFalse(is_exist)
