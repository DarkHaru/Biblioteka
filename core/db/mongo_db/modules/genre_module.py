from ....entities.genre_dto import GenreDto
from bson.objectid import ObjectId
from typing import List


class GenreModule:
    '''
    Genre module to operate with 'genres' collection in database
    '''

    # Class constructor
    def __init__(self, collection_controller):
        self.collection_controller = collection_controller

    # Insert data in database
    def create_new_genre(self, genre_data: GenreDto):
        '''
        Create new genre in database
        '''

        new_genre = {
            "name": genre_data.name,
        }

        self.collection_controller.insert_one(new_genre)

    # Update data in database
    def update_genre_data(self, genre_data: GenreDto):
        '''
        Update particular genre data
        '''

        update_query = {"_id": genre_data._id}
        update_data = {
            "$set": {
                "name": genre_data.name,
            }
        }

        self.collection_controller.update_one(update_query, update_data)

    # Delete data from database
    def delete_genre(self, genre_id: str):
        '''
        Delete particular genre from database
        '''

        object_id = ObjectId(genre_id)
        delete_query = {"_id": object_id}

        self.collection_controller.delete_one(delete_query)

    # Read data from database
    def find_genre_by_name(self, genre_name: str) -> GenreDto:
        '''
        Fetch particular genre by name
        '''

        raw_genre = self.collection_controller.find_one({"name": genre_name})
        if (not raw_genre):
            return None

        genre = GenreDto(raw_genre["_id"], raw_genre["name"])

        return genre

    def find_genre_by_id(self, genre_id: str) -> GenreDto:
        '''
        Fetch particular genre by id
        '''

        raw_genre = self.collection_controller.find_one({"_id": genre_id})
        if (not raw_genre):
            return None

        genre = GenreDto(raw_genre["_id"], raw_genre["name"])

        return genre

    def find_all_genres(self) -> List[GenreDto]:
        '''
        Fetch all genres in database
        '''

        raw_genres = self.collection_controller.find()
        genres = []

        for genre in raw_genres:
            genres.append(GenreDto(genre["_id"], genre["name"]))

        return genres
