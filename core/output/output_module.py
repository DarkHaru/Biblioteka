import zope.interface
from .file_object import FileObject

PATH_TO_OUTPUT_FILES = "output_files/"


class IOutputModule(zope.interface.Interface):
    '''
    Interface for working with output files
    '''

    def write_to_file(self, data: FileObject):
        '''
        Write to file data
        '''
        pass

    def transform_data(self, raw_data):
        '''
        Transform raw data in form that easy to write in file
        '''
        pass
