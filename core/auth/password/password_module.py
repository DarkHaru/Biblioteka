import zope.interface
from core.auth.auth_module import IAuthModule
from core.db.db_module import IDBModule


@zope.interface.implementer(IAuthModule)
class PasswordModule:
    def __init__(self, db_controller: IDBModule):
        self.db_controller = db_controller

    def login(self, name: str, password: str):
        user = self.db_controller.find_user_by_name(name)

        if (not user):
            return None

        if (user.name == name and user.password == password):
            return user
        else:
            return None

    def check_user_exist(self, name: str):
        user = self.db_controller.find_user_by_name(name)

        if (user):
            return True
        else:
            return False
