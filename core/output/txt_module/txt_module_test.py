import unittest
from .txt_module import TxtModule
from ..output_module import PATH_TO_OUTPUT_FILES
from core.output.file_object import FileObject


class TestTxtModule(unittest.TestCase):

    def setUp(self):
        self.txt_module = TxtModule()

    def test_write_to_file(self):
        file_object = FileObject("test_file.txt", "test_data")
        self.txt_module.write_to_file(file_object)

        with open(PATH_TO_OUTPUT_FILES + file_object.name, "r") as file:
            data = file.read()
            self.assertEqual(file_object.data, data)

    def test_transform_data(self):
        raw_data = ["test", "case", "data"]
        test_str = "test\ncase\ndata\n"
        data = self.txt_module.transform_data(raw_data)

        self.assertEqual(data, test_str)
