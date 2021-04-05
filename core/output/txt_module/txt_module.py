from core.output.output_module import IOutputModule, PATH_TO_OUTPUT_FILES
from ..file_object import FileObject
import zope.interface


@zope.interface.implementer(IOutputModule)
class TxtModule:
    '''
    Class to represent data in txt file.
    Implementation of IOutputModule
    '''

    def write_to_file(self, file_object: FileObject):
        '''
        Write data to txt file
        '''

        path = PATH_TO_OUTPUT_FILES + file_object.name

        with open(path, "w") as file:
            file.write(file_object.data)

    def transform_data(self, raw_data: list) -> str:
        '''
        Transform raw data to string
        '''

        result = ""
        for item in raw_data:
            result += item + "\n"

        return result
