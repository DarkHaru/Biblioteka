from core.entities.user_dto import UserDto
import zope.interface


class IAuthModule(zope.interface.Interface):
    '''
    Module for login user and check user existance in database
    '''

    def login(self, name: str, password: str) -> UserDto:
        '''
        Return user dto if names and passwords compare
        '''
        pass

    def check_user_exist(self, name: str) -> bool:
        '''
        Return 'true' if user exist in database, otherwise return 'false'
        '''
        pass
