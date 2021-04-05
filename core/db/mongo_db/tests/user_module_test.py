import unittest
from ..modules.user_module import UserModule
from pymongo import MongoClient
from ....secret import MONGODB_CONNECTION_LINK
from ....entities.user_dto import UserDto
from typing import List


class TestUserModule(unittest.TestCase):

    def setUp(self):
        client = MongoClient(MONGODB_CONNECTION_LINK)
        self.user_module = UserModule(client.db.users)

    # Should create new user in database
    def test_create_new_user(self):
        user = UserDto(-1, 'test_user', '1234', [])
        self.user_module.create_new_user(user)

        created_user = self.user_module.find_user_by_name(user.name)
        self.assertIsNotNone(created_user)

    # Should change user password in database
    def test_update_user_data(self):
        user = self.user_module.find_user_by_name("test_user")
        _id = user._id
        new_password = '1111'
        user = UserDto(_id, 'test_user', new_password, [])
        self.user_module.update_user_data(user)

        updated_user = self.user_module.find_user_by_name(user.name)
        self.assertEqual(updated_user.password, new_password)

    # Should return user dto if user exist in database
    def test_find_user_by_name(self):
        user = self.user_module.find_user_by_name('test_user')
        self.assertIsNotNone(user)

    # Should return user dto if user in database
    def test_find_user_by_id(self):
        user = self.user_module.find_user_by_name("test_user")
        _id = user._id
        user = self.user_module.find_user_by_id(_id)
        self.assertIsNotNone(user)

    # Should return list of user dtos
    def test_find_all_users(self):
        users = self.user_module.find_all_users()
        self.assertEqual(len(users), 1)

    # Should delete user from database
    def test_delete_user(self):
        user = self.user_module.find_user_by_name("test_user")
        _id = user._id
        self.user_module.delete_user(_id)

        user = self.user_module.find_user_by_id(_id)
        self.assertIsNone(user)
