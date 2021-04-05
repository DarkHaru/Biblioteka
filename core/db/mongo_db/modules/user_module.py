from ....entities.user_dto import UserDto
from bson.objectid import ObjectId
from typing import List


class UserModule:
    '''
    User module to operate with 'users' collection in database
    '''

    # Class constructor
    def __init__(self, collection_controller):
        self.collection_controller = collection_controller

    # Insert data in database
    def create_new_user(self, user_dto: UserDto):
        '''
        Create new user in database
        '''

        new_user = {
            "name": user_dto.name,
            "password": user_dto.password,
            "collection": user_dto.collection,
            "_admin": user_dto._admin
        }

        self.collection_controller.insert_one(new_user)

    # Update data in database
    def update_user_data(self, user_dto: UserDto):
        '''
        Update particular user data
        '''
        update_query = {"_id": user_dto._id}
        update_data = {
            "$set": {
                "name": user_dto.name,
                "password": user_dto.password,
                "collection": user_dto.collection,
                "_admin": user_dto._admin
            }
        }

        self.collection_controller.update_one(update_query, update_data)

    # Delete data from database
    def delete_user(self, user_id: str):
        '''
        Delete particular user from database
        '''
        object_id = ObjectId(user_id)
        delete_query = {"_id": object_id}

        self.collection_controller.delete_one(delete_query)

    # Read data from database
    def find_user_by_name(self, name: str) -> UserDto:
        '''
        Fetch particular user from database by name
        '''

        raw_user = self.collection_controller.find_one({"name": name})
        if (not raw_user):
            return None

        user = UserDto(raw_user["_id"], raw_user["name"],
                       raw_user["password"], raw_user["collection"])
        user._admin = raw_user["_admin"]

        return user

    def find_user_by_id(self, user_id: str) -> UserDto:
        '''
        Fetch particular user from database by id
        '''

        object_id = ObjectId(user_id)
        raw_user = self.collection_controller.find_one({"_id": object_id})
        if (not raw_user):
            return None

        user = UserDto(raw_user["_id"], raw_user["name"],
                       raw_user["password"], raw_user["collection"])
        user._admin = raw_user["_admin"]

        return user

    def find_all_users(self) -> List[UserDto]:
        '''
        Fetch all users in database
        '''

        raw_users = self.collection_controller.find()
        users = []

        for user in raw_users:
            user_dto = UserDto(user["_id"], user["name"],
                               user["password"], user["collection"])
            user_dto._admin = user["_admin"]

            users.append(user_dto)

        return users
