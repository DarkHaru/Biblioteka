import unittest
from ..modules.book_module import BookModule
from pymongo import MongoClient
from core.secret import MONGODB_CONNECTION_LINK
from core.entities.book_dto import BookDto


class TestBookModule(unittest.TestCase):

    def setUp(self):
        client = MongoClient(MONGODB_CONNECTION_LINK)
        self.book_module = BookModule(client.db.books)

    # Should create new book in database
    def test_create_new_book(self):
        book = BookDto(-1, 'test_book', ['1'], 'test_descr', 'ego')
        self.book_module.create_new_book(book)

        created_book = self.book_module.find_book_by_name(book.title)
        self.assertIsNotNone(created_book)

    # Should change book description in database
    def test_update_book_data(self):
        book = self.book_module.find_book_by_name("test_book")
        new_descr = 'new_descr'
        update_data = BookDto(book._id, 'test_book', ['1'], new_descr, 'ego')
        self.book_module.update_book_data(update_data)

        updated_book = self.book_module.find_book_by_id(book._id)
        self.assertEqual(updated_book.description, new_descr)

    # Should return book dto if it exists in database
    def test_find_book_by_id(self):
        book = self.book_module.find_book_by_name("test_book")
        book = self.book_module.find_book_by_id(book._id)
        self.assertIsNotNone(book)

    # Should return book dto if it exists in database
    def test_find_book_by_name(self):
        book = self.book_module.find_book_by_name("test_book")
        self.assertIsNotNone(book)

    # Should return list of book dtos
    def test_find_all_books(self):
        books = self.book_module.find_all_books()
        self.assertEqual(len(books), 1)

    # Should return all books with particular genre
    def test_find_books_by_genre(self):
        books_with_genre_1 = self.book_module.find_books_by_genre('1')
        books_with_genre_a = self.book_module.find_books_by_genre('a')

        self.assertEqual(len(books_with_genre_1), 1)
        self.assertEqual(len(books_with_genre_a), 0)

    def test_find_books_by_author(self):
        books_with_author_ego = self.book_module.find_books_by_author('ego')
        books_with_author_zero = self.book_module.find_books_by_author('zero')

        self.assertEqual(len(books_with_author_ego), 1)
        self.assertEqual(len(books_with_author_zero), 0)

    # Should delete book from database
    def test_delete_book(self):
        book = self.book_module.find_book_by_name("test_book")
        self.book_module.delete_book(book._id)

        book = self.book_module.find_book_by_id(book._id)
        self.assertIsNone(book)
