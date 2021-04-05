from ..entities.user_dto import UserDto
from ..entities.book_dto import BookDto
from ..entities.genre_dto import GenreDto
from typing import List
import zope.interface


class IDBModule(zope.interface.Interface):
    ''' Interface for all database modules '''

    # User functions
    def create_new_user(self, user_data: UserDto):
        ''' Add new user to the database '''
        pass

    def update_user_data(self, user_data: UserDto):
        ''' Update user data in database '''
        pass

    def delete_user(self, id: str):
        ''' Delete user from database '''
        pass

    def find_user_by_name(self, name: str) -> UserDto:
        ''' 
        Find user in database by name. 
        Return user dto 
        '''
        pass

    def find_user_by_id(self, id: str) -> UserDto:
        ''' 
        Find user in database by id. 
        Return user dto 
        '''
        pass

    def find_all_users(self) -> List[UserDto]:
        '''
        Find all users in database
        Return list of user dtos
        '''
        pass

    # Book functions
    def create_new_book(self, book_data: BookDto):
        ''' Add new book to the database '''
        pass

    def update_book_data(self, book_data: BookDto):
        ''' Update book data in database '''
        pass

    def delete_book(self, id: str):
        ''' Delete book from database '''
        pass

    def find_all_books(self) -> List[BookDto]:
        ''' 
        Find all books in database. 
        Return list of book dtos 
        '''
        pass

    def find_book_by_id(self, id: str) -> BookDto:
        ''' 
        Find book in database by id. 
        Return book dto 
        '''
        pass

    def find_book_by_title(self, title: str) -> BookDto:
        ''' 
        Find book in database by title. 
        Return book dto 
        '''
        pass

    def find_books_by_genre(self, genre: str) -> List[BookDto]:
        ''' 
        Find books with particular genre. 
        Return list of book dtos 
        '''
        pass

    def find_books_by_author(self, author: str) -> List[BookDto]:
        '''
        Find books with particular author.
        Return list of book dtos
        '''
        pass

    # Genre functions
    def create_new_genre(self, genre_data: GenreDto):
        ''' Add new genre to the database '''
        pass

    def update_genre_data(self, genre_data: GenreDto):
        ''' Update genre data in database '''
        pass

    def delete_genre(self, id: str):
        ''' Delete genre from database '''
        pass

    def find_all_genres(self) -> List[GenreDto]:
        ''' 
        Find all genres in database. 
        Return list of genre dtos 
        '''
        pass

    def find_genre_by_name(self, name: str) -> GenreDto:
        '''
        Find particular genre by name.
        Return genre dto
        '''
        pass

    def find_genre_by_id(self, id: str) -> GenreDto:
        '''
        Find particular genre by id.
        Return genre dto
        '''
        pass
