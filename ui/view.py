from PyQt5 import QtWidgets
from .forms.main_form import Ui_MainWindow
from .forms.auth_form import Ui_AuthForm
from .forms.book_form import Ui_BookManager
import sys
from enum import Enum


class MainWindowPages(Enum):
    USER = 0
    ADMIN = 1
    BOOK_INFO = 2


class UserPages(Enum):
    MY_BOOKS = 0
    CATALOG = 1


class AdminPages(Enum):
    ALL_BOOKS = 0
    ALL_USERS = 1


class InsertModes(Enum):
    INSERT = 0
    UPDATE = 1


class DesktopView:
    def __init__(self):
        '''
        Initialize desktop application and all forms
        '''
        self._desktop_app = QtWidgets.QApplication(sys.argv)
        self._main_form = QtWidgets.QMainWindow()
        self._auth_form = QtWidgets.QDialog()
        self._book_form = QtWidgets.QDialog()

        self._main_form_ui = Ui_MainWindow()
        self._auth_form_ui = Ui_AuthForm()
        self._book_form_ui = Ui_BookManager()

        self._main_form_ui.setupUi(self._main_form)
        self._auth_form_ui.setupUi(self._auth_form)
        self._book_form_ui.setupUi(self._book_form)

        self._message_box = QtWidgets.QMessageBox()

    def get_app(self):
        '''
        Return app instance
        '''
        return self._desktop_app

    def get_main_window(self):
        '''
        Return main window
        '''
        return self._main_form

    def get_auth_dialog(self):
        '''
        Return auth dialog window
        '''
        return self._auth_form

    def get_book_dialog(self):
        '''
        Return book manager dialog window
        '''
        return self._book_form

    def get_uis(self):
        '''
        Return all uis to work with components
        '''
        return [self._main_form_ui, self._auth_form_ui, self._book_form_ui]

    def _show_message_box(self, title: str, message: str, icon: QtWidgets.QMessageBox.Icon):
        '''
        Show message box
        '''
        self._message_box.setIcon(icon)
        self._message_box.setWindowTitle(title)
        self._message_box.setText(message)
        self._message_box.show()

    def show_error_message(self, message: str):
        '''
        Show error message
        '''
        self._show_message_box(
            'Error message',
            message,
            QtWidgets.QMessageBox.Critical
        )

    def show_warning_message(self, message: str):
        '''
        Show warning message
        '''
        self._show_message_box(
            'Warning message',
            message,
            QtWidgets.QMessageBox.Warning
        )

    def show_message(self, message: str):
        '''
        Show message
        '''
        self._show_message_box(
            'Message',
            message,
            QtWidgets.QMessageBox.Information
        )
