from ....entities.book_dto import BookDto
from bson.objectid import ObjectId
from typing import List


class BookModule:
    '''
    Book module to operate with 'books' collection in database
    '''

    # Class constructor
    def __init__(self, collection_controller):
        self.collection_controller = collection_controller

    # Insert data in database
    def create_new_book(self, book_dto: BookDto):
        '''
        Create new book in database
        '''

        new_book = {
            "title": book_dto.title,
            "description": book_dto.description,
            "genres": book_dto.genres,
            "author": book_dto.author,
        }

        self.collection_controller.insert_one(new_book)

    # Update data in database
    def update_book_data(self, book_dto: BookDto):
        '''
        Update particular book data
        '''
        update_query = {"_id": book_dto._id}
        update_data = {
            "$set": {
                "title": book_dto.title,
                "description": book_dto.description,
                "genres": book_dto.genres,
                "author": book_dto.author
            }
        }

        self.collection_controller.update_one(update_query, update_data)

    # Delete data from database
    def delete_book(self, book_id: str):
        '''
        Delete particular book from database
        '''

        object_id = ObjectId(book_id)
        delete_query = {"_id": object_id}

        self.collection_controller.delete_one(delete_query)

    # Read data from database
    def find_book_by_id(self, book_id: str) -> BookDto:
        '''
        Fetch particular book from database by id
        '''

        object_id = ObjectId(book_id)
        raw_book = self.collection_controller.find_one({"_id": object_id})
        if (not raw_book):
            return None

        book = BookDto(raw_book["_id"], raw_book["title"],
                       raw_book["genres"], raw_book["description"], raw_book["author"])

        return book

    def find_all_books(self) -> List[BookDto]:
        '''
        Fetch all books in database
        '''

        raw_books = self.collection_controller.find()
        books = []

        for book in raw_books:
            books.append(BookDto(book["_id"], book["title"],
                                 book["genres"], book["description"], book["author"]))

        return books

    def find_books_by_genre(self, genre_id: str) -> List[BookDto]:
        '''
        Fetch all books with particular genre
        '''

        find_query = {"genres": genre_id}
        raw_books = self.collection_controller.find(find_query)
        books = []

        for book in raw_books:
            books.append(BookDto(book["_id"], book["title"],
                                 book["genres"], book["description"], book["author"]))

        return books

    def find_books_by_author(self, author: str) -> List[BookDto]:
        '''
        Fetch all books with particular author
        '''

        find_query = {"author": author}
        raw_books = self.collection_controller.find(find_query)
        books = []

        for book in raw_books:
            books.append(BookDto(book["_id"], book["title"],
                                 book["genres"], book["description"], book["author"]))

        return books

    def find_book_by_name(self, book_name: str) -> BookDto:
        '''
        Fetch particular book by name
        '''

        raw_book = self.collection_controller.find_one({"title": book_name})
        if (not raw_book):
            return None

        book = BookDto(raw_book["_id"], raw_book["title"],
                       raw_book["genres"], raw_book["description"], raw_book["author"])

        return book
