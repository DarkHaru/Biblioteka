class UserDto:
    def __init__(self, _id: str, name: str, password: str, collection: []):
        self._id = _id
        self._admin = 0
        self.name = name
        self.password = password
        self.collection = collection
