from pymongo import MongoClient
from typing import List
import zope.interface
from ..db_module import IDBModule
from ...secret import MONGODB_CONNECTION_LINK
from .modules.user_module import UserModule
from .modules.book_module import BookModule
from .modules.genre_module import GenreModule
from ...entities.user_dto import UserDto
from ...entities.book_dto import BookDto
from ...entities.genre_dto import GenreDto


@zope.interface.implementer(IDBModule)
class MongoDBFacade:
    def __init__(self):
        client = MongoClient(MONGODB_CONNECTION_LINK)
        self.user_module = UserModule(client.db.users)
        self.book_module = BookModule(client.db.books)
        self.genre_module = GenreModule(client.db.genres)

    # User functions
    def create_new_user(self, user_data: UserDto):
        self.user_module.create_new_user(user_data)

    def update_user_data(self, user_data: UserDto):
        self.user_module.update_user_data(user_data)

    def delete_user(self, user_id: str):
        self.user_module.delete_user(user_id)

    def find_user_by_name(self, name: str) -> UserDto:
        user = self.user_module.find_user_by_name(name)
        return user

    def find_user_by_id(self, user_id: str) -> UserDto:
        user = self.user_module.find_user_by_id(user_id)
        return user

    def find_all_users(self) -> List[UserDto]:
        users = self.user_module.find_all_users()
        return users

    # Book functions
    def create_new_book(self, book_data: BookDto):
        self.book_module.create_new_book(book_data)

    def update_book_data(self, book_data: BookDto):
        self.book_module.update_book_data(book_data)

    def delete_book(self, book_id: str):
        self.book_module.delete_book(book_id)

    def find_all_books(self) -> List[BookDto]:
        books = self.book_module.find_all_books()
        return books

    def find_book_by_id(self, book_id: str) -> BookDto:
        book = self.book_module.find_book_by_id(book_id)
        return book

    def find_book_by_title(self, title: str) -> BookDto:
        book = self.book_module.find_book_by_name(title)
        return book

    def find_books_by_genre(self, genre: str) -> List[BookDto]:
        books = self.book_module.find_books_by_genre(genre)
        return books

    def find_books_by_author(self, author: str) -> List[BookDto]:
        books = self.book_module.find_books_by_author(author)
        return books

    # Genre functions
    def create_new_genre(self, genre_data: GenreDto):
        self.genre_module.create_new_genre(genre_data)

    def update_genre_data(self, genre_data: GenreDto):
        self.genre_module.update_genre_data(genre_data)

    def delete_genre(self, genre_id: str):
        self.genre_module.delete_genre(genre_id)

    def find_all_genres(self) -> List[GenreDto]:
        genres = self.genre_module.find_all_genres()
        return genres

    def find_genre_by_name(self, name: str) -> GenreDto:
        genre = self.genre_module.find_genre_by_name(name)
        return genre

    def find_genre_by_id(self, genre_id: str) -> GenreDto:
        genre = self.genre_module.find_genre_by_id(genre_id)
        return genre
