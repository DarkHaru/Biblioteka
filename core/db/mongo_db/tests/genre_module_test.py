import unittest
from ..modules.genre_module import GenreModule
from pymongo import MongoClient
from ....secret import MONGODB_CONNECTION_LINK
from ....entities.genre_dto import GenreDto
from typing import List


class TestGenreModule(unittest.TestCase):

    def setUp(self):
        client = MongoClient(MONGODB_CONNECTION_LINK)
        self.genre_module = GenreModule(client.db.genres)

    # Should create new user in database
    def test_create_new_genre(self):
        genre = GenreDto(-1, 'test_genre')
        self.genre_module.create_new_genre(genre)

        created_genre = self.genre_module.find_genre_by_name(genre.name)
        self.assertIsNotNone(created_genre)

    # Should change user password in database
    def test_update_genre_data(self):
        genre = self.genre_module.find_genre_by_name("test_genre")
        _id = genre._id
        new_name = 'new_name'
        genre = GenreDto(_id, new_name)
        self.genre_module.update_genre_data(genre)

        updated_genre = self.genre_module.find_genre_by_name(new_name)
        self.assertEqual(updated_genre.name, new_name)

        genre = GenreDto(_id, "test_genre")
        self.genre_module.update_genre_data(genre)

    # Should return user dto if user exist in database
    def test_find_genre_by_name(self):
        genre = self.genre_module.find_genre_by_name("test_genre")
        self.assertIsNotNone(genre)

    # Should return list of user dtos
    def test_find_all_genres(self):
        genres = self.genre_module.find_all_genres()
        self.assertIsNotNone(genres)

    # Should delete user from database
    def test_delete_genre(self):
        genre = self.genre_module.find_genre_by_name("test_genre")
        _id = genre._id
        self.genre_module.delete_genre(_id)

        genre = self.genre_module.find_genre_by_id(_id)
        self.assertIsNone(genre)
