from PyQt5 import QtWidgets
from core.db.mongo_db.mongo_db_facade import MongoDBFacade
from core.output.txt_module.txt_module import TxtModule
from core.auth.password.password_module import PasswordModule
from ui.view import DesktopView, MainWindowPages, UserPages, AdminPages, InsertModes
from core.entities import UserDto, BookDto, GenreDto
import sys

ID_FOR_NEW_ITEM = -1
NEW_USER_COLLECTION = []


class AppController:
    _insert_mode = None

    def __init__(self):
        # Setup all modules
        self.db_module = MongoDBFacade()
        self.auth_module = PasswordModule(self.db_module)
        self.file_output_module = TxtModule()

        # Setup view
        self.view = DesktopView()
        self.app = self.view.get_app()
        self.main_window = self.view.get_main_window()
        self.auth_dialog = self.view.get_auth_dialog()
        self.book_dialog = self.view.get_book_dialog()
        self._main_window_ui, self._auth_dialog_ui, self._book_dialog_ui = self.view.get_uis()

        self._setup_auth_form_behavior()
        self._setup_main_window_behavior()

    def start(self):
        self.auth_dialog.show()
        sys.exit(self.app.exec_())

    # UI stuff
    def _setup_auth_form_behavior(self):
        '''
        Set up all listeners for auth form
        '''

        # Creating variables for edits
        name_edit = self._auth_dialog_ui.loginEdit
        password_edit = self._auth_dialog_ui.passwordEdit

        # Adding listeners to 'signUpBtn' and 'signInBtn'
        self._auth_dialog_ui.signUpBtn.clicked.connect(
            lambda: self._sign_up_user(
                name_edit.text(),
                password_edit.text()
            )
        )

        self._auth_dialog_ui.signInBtn.clicked.connect(
            lambda: self._sign_in_user(
                name_edit.text(),
                password_edit.text()
            )
        )

    def _setup_main_window_behavior(self):
        '''
        Set up all listeners for main window
        '''

        # Menu listeners
        user_menu = self._main_window_ui.userMenu
        admin_menu = self._main_window_ui.adminMenu

        user_menu.itemClicked.connect(
            lambda: self._set_user_stack_index(
                user_menu.selectedIndexes()[0].row())
        )

        admin_menu.itemClicked.connect(
            lambda: self._set_admin_stack_index(
                admin_menu.selectedIndexes()[0].row())
        )

        # Book list listeners
        user_my_books = self._main_window_ui.myBooksList
        user_catalog_books = self._main_window_ui.catalogBooksList
        admin_books = self._main_window_ui.allBooksList
        admin_users = self._main_window_ui.usersList

        # Unlock admin buttons
        admin_books.itemClicked.connect(
            self._unlock_admin_book_btns
        )

        admin_users.itemClicked.connect(
            self._unlock_admin_users_btns
        )

        # Unlock users buttons
        user_my_books.itemClicked.connect(
            self._unlock_user_my_books_btns
        )

        user_catalog_books.itemClicked.connect(
            self._unlock_user_catalog_btns
        )

        # Bind listeners for search on user page and admin page
        # - User page
        user_search_edit = self._main_window_ui.userSearchEdit
        self._main_window_ui.userSearchBtn.clicked.connect(
            lambda: self._search_and_fill_books(
                user_search_edit.text(), user_catalog_books)
        )
        self._main_window_ui.userResetBtn.clicked.connect(
            self._reset_search_result
        )

        # - Admin page
        admin_search_edit = self._main_window_ui.adminSearchEdit
        self._main_window_ui.adminSearchBtn.clicked.connect(
            lambda: self._search_and_fill_books(
                admin_search_edit.text(), admin_books)
        )
        self._main_window_ui.adminResetBtn.clicked.connect(
            self._reset_search_result
        )

        # Preview buttons listeners
        self._main_window_ui.previewBookBtn.clicked.connect(
            self._show_book_info
        )

        self._main_window_ui.viewBookBtn.clicked.connect(
            self._show_book_info
        )

        self._main_window_ui.viewMyBookBtn.clicked.connect(
            self._show_book_info
        )

        # Back button listener at book info page
        self._main_window_ui.backBtn.clicked.connect(
            self._go_back_from_book_info
        )

        # Listeners for all admin add/edit/remove buttons
        self._main_window_ui.addNewBookBtn.clicked.connect(
            self._open_book_manager_to_insert
        )

        self._main_window_ui.editBookBtn.clicked.connect(
            self._open_book_manager_to_update
        )

        self._main_window_ui.deleteBookBtn.clicked.connect(
            self._delete_book
        )

        self._main_window_ui.deleteUserBtn.clicked.connect(
            self._remove_user
        )

        # Listeners for book manager dialog
        self._book_dialog_ui.addBtn.clicked.connect(
            self._insert_update_new_book
        )

        self._book_dialog_ui.cancelBtn.clicked.connect(
            self.book_dialog.close
        )

        # Listeners for user buttons to operate with collection
        self._main_window_ui.addToCollectionBtn.clicked.connect(
            self._add_book_to_collection
        )

        self._main_window_ui.removeFromCollection.clicked.connect(
            self._remove_book_from_collection
        )

    # Set index for stack widgets
    def _set_main_window_stack_index(self, index: int):
        '''
        Set stack widget index at main window
        '''
        self._main_window_ui.formContent.setCurrentIndex(index)

    def _set_user_stack_index(self, index: int):
        '''
        Set stack widget index at user page
        '''
        if (index >= len(UserPages)):
            self.current_user = None
            self.auth_dialog.show()
            self.main_window.close()

        self._main_window_ui.userContent.setCurrentIndex(index)

    def _set_admin_stack_index(self, index: int):
        '''
        Set stack widget index at admin page
        '''

        if (index >= len(UserPages)):
            self.current_user = None
            self.auth_dialog.show()
            self.main_window.close()

        self._main_window_ui.adminContent.setCurrentIndex(index)

    def _go_back_from_book_info(self):
        '''
        Return back from book info page
        '''
        back_address = MainWindowPages.USER.value

        if (self.current_user._admin == 1):
            back_address = MainWindowPages.ADMIN.value

        self._set_main_window_stack_index(back_address)

    # Clear fields
    def _clear_auth_dialog(self):
        '''
        Clear all edits in auth form
        '''
        self._auth_dialog_ui.loginEdit.setText('')
        self._auth_dialog_ui.passwordEdit.setText('')

    # Fill tables and list widgets
    def _fill_books(self, books, table_widget: QtWidgets.QTableWidget):
        '''
        Fill book list in user page
        '''
        table_widget.setRowCount(0)
        current_row = 0
        for book in books:

            # Set title
            book_title = QtWidgets.QTableWidgetItem()
            book_title.setText(book.title)

            # Set genres
            genres = ','.join(book.genres)
            book_genres = QtWidgets.QTableWidgetItem()
            book_genres.setText(genres)

            # Set author
            book_author = QtWidgets.QTableWidgetItem()
            book_author.setText(book.author)

            # Inserting row and columns
            table_widget.insertRow(current_row)
            table_widget.setItem(current_row, 0, book_title)
            table_widget.setItem(current_row, 1, book_genres)
            table_widget.setItem(current_row, 2, book_author)

            current_row += 1

    def _fill_users(self):
        '''
        Fill users list for admin
        '''

        users_list = self._main_window_ui.usersList
        users = self.db_module.find_all_users()
        users_list.clear()

        for user in users:
            if (user.name != self.current_user.name):
                users_list.addItem(user.name)

    def _update_after_collection_changed(self):
        '''
        Update user books widget after collection changed
        '''

        books = self.db_module.find_all_books()
        user_books = list(
            filter(lambda book: book._id in self.current_user.collection, books))
        my_books_table = self._main_window_ui.myBooksList
        self._fill_books(user_books, my_books_table)

    def _reset_search_result(self):
        '''
        Reset search result
        '''
        books = self.db_module.find_all_books()
        table = None

        if self.current_user._admin == 1:
            table = self._main_window_ui.allBooksList
        else:
            table = self._main_window_ui.catalogBooksList

        self._fill_books(books, table)

    # Unlock buttons and set selected book and selected user
    def _unlock_admin_book_btns(self):
        '''
        Unlock admin buttons on books table page
        '''
        self._main_window_ui.addNewBookBtn.setEnabled(True)
        self._main_window_ui.deleteBookBtn.setEnabled(True)
        self._main_window_ui.editBookBtn.setEnabled(True)
        self._main_window_ui.previewBookBtn.setEnabled(True)

        # Change selected book
        selected_item = self._main_window_ui.allBooksList.selectedItems()[
            0]
        selected_row = selected_item.row()
        selected_title = self._main_window_ui.allBooksList.item(
            selected_row, 0).text()

        self._selected_book = self.db_module.find_book_by_title(selected_title)

    def _unlock_admin_users_btns(self):
        '''
        Unlock admin buttons on users list page
        '''
        self._main_window_ui.deleteUserBtn.setEnabled(True)

        # Change selected user
        selected_name = self._main_window_ui.usersList.selectedItems()[
            0].text()
        self._selected_user = self.db_module.find_user_by_name(selected_name)

    def _unlock_user_my_books_btns(self):
        '''
        Unlock users buttons on my books list page
        '''
        self._main_window_ui.removeFromCollection.setEnabled(True)
        self._main_window_ui.viewMyBookBtn.setEnabled(True)

        # Change selected book
        selected_item = self._main_window_ui.myBooksList.selectedItems()[0]
        selected_row = selected_item.row()
        selected_title = self._main_window_ui.myBooksList.item(
            selected_row, 0).text()
        self._selected_book = self.db_module.find_book_by_title(selected_title)

    def _unlock_user_catalog_btns(self):
        '''
        Unlock users buttons on catalog table page
        '''
        self._main_window_ui.viewBookBtn.setEnabled(True)
        self._main_window_ui.addToCollectionBtn.setEnabled(True)

        # Change selected book
        selected_item = self._main_window_ui.catalogBooksList.selectedItems()[
            0]
        selected_row = selected_item.row()
        selected_title = self._main_window_ui.catalogBooksList.item(
            selected_row, 0).text()
        self._selected_book = self.db_module.find_book_by_title(selected_title)

    # Insert and update book
    def _open_book_manager_to_insert(self):
        '''
        Open book manager dialog to insert new book
        '''
        self._insert_mode = InsertModes.INSERT
        self.book_dialog.show()

    def _open_book_manager_to_update(self):
        '''
        Open book manager to update book data
        '''
        self._insert_mode = InsertModes.UPDATE

        self._book_dialog_ui.bookTitle.setText(self._selected_book.title)
        self._book_dialog_ui.bookGenres.setText(
            ','.join(self._selected_book.genres))
        self._book_dialog_ui.bookAuthor.setText(self._selected_book.author)
        self._book_dialog_ui.bookDescription.setText(
            self._selected_book.description)
        self.book_dialog.show()

    # Functions and methods
    def _sign_up_user(self, name: str, password: str):
        '''
        Sign up new user
        '''

        # Check auth form edits are filled
        if (name == '' or password == ''):
            self.view.show_error_message(
                'Имя пользователя и пароль не заполнены!'
            )
            return None

        # Check if user exist
        is_user_exist = self.auth_module.check_user_exist(name)

        if (is_user_exist):
            self.view.show_error_message('Пользователь уже существует!')
            return None

        # Creating new user
        new_user = UserDto(
            ID_FOR_NEW_ITEM,
            name,
            password,
            NEW_USER_COLLECTION
        )
        self.db_module.create_new_user(new_user)
        self.view.show_message('Пользователь создан!')

    def _sign_in_user(self, name: str, password: str):
        '''
        Sign in user
        '''

        # Check auth form edits are filled
        if (name == '' or password == ''):
            self.view.show_error_message(
                'Имя пользователя и пароль не заполнены!'
            )
            return None

        # Check if user exist
        is_user_exist = self.auth_module.check_user_exist(name)

        if (not is_user_exist):
            self.view.show_error_message('Пользователь не существует!')
            return None

        # Setting current user and open main window
        self.current_user = self.auth_module.login(name, password)

        if (self.current_user):
            self.main_window.show()
            self.auth_dialog.close()
            self._clear_auth_dialog()

            # Preload all books in database
            all_books = self.db_module.find_all_books()

            if (self.current_user._admin):
                self._set_main_window_stack_index(MainWindowPages.ADMIN.value)

                # Fill users list
                self._fill_users()

                # Fill books table view
                table_widget = self._main_window_ui.allBooksList
                self._fill_books(all_books, table_widget)
            else:
                self._set_main_window_stack_index(MainWindowPages.USER.value)

                # Fill books for catalog
                catalog_table = self._main_window_ui.catalogBooksList
                self._fill_books(all_books, catalog_table)

                # Fill user personal books
                my_books_table = self._main_window_ui.myBooksList
                my_books_list = list(filter(
                    lambda book: book._id in self.current_user.collection, all_books))
                self._fill_books(my_books_list, my_books_table)
        else:
            self.view.show_error_message('Неправильный пароль!')

    def _search_books(self, search_data):
        '''
        Find all books that compare to conditions
        '''

        by_author = None
        by_genre = None
        by_title = None

        if self.current_user._admin == 0:
            by_author = self._main_window_ui.userAuthorRadio.isChecked()
            by_genre = self._main_window_ui.userGenreRadio.isChecked()
            by_title = self._main_window_ui.userTitleRadio.isChecked()
        elif self.current_user._admin == 1:
            by_author = self._main_window_ui.adminAuthorRadio.isChecked()
            by_genre = self._main_window_ui.adminGenreRadio.isChecked()
            by_title = self._main_window_ui.adminTitleRadio.isChecked()

        if (by_title):
            return [self.db_module.find_book_by_title(search_data)]
        elif (by_genre):
            return self.db_module.find_books_by_genre(search_data)
        elif (by_author):
            return self.db_module.find_books_by_author(search_data)
        else:
            self.view.show_error_message('Поле поиска пусто!')
            return None

    def _search_and_fill_books(self, search_data, table_widget):
        '''
        Search books in database and fill table widget
        '''
        books = self._search_books(search_data)
        if (books):
            if books[0] == None:
                books = []
            self._fill_books(books, table_widget)

    def _show_book_info(self):
        '''
        Show selected book info on page
        '''

        if (self._selected_book == None):
            self.view.show_error_message('Не выбрана ниодна книга!')
            return None

        self._main_window_ui.bookTitleLabel.setText(self._selected_book.title)
        self._main_window_ui.bookGenresLabel.setText(
            ','.join(self._selected_book.genres))
        self._main_window_ui.bookDescriptionLabel.setText(
            self._selected_book.description)

        self._set_main_window_stack_index(MainWindowPages.BOOK_INFO.value)

    def _delete_book(self):
        '''
        Delete selected book
        '''

        if (self._selected_book == None):
            self.view.show_error_message('Не выбрана ниодна книга!')
            return None

        self.db_module.delete_book(self._selected_book._id)

        new_books = self.db_module.find_all_books()
        all_books_table = self._main_window_ui.allBooksList
        self._fill_books(new_books, all_books_table)

        self.view.show_message('Книга удалена! Поздравляю!')

    def _insert_update_new_book(self):
        '''
        Insert new book
        '''

        title = self._book_dialog_ui.bookTitle.text()
        genres = self._book_dialog_ui.bookGenres.text().split(',')
        author = self._book_dialog_ui.bookAuthor.text()
        description = self._book_dialog_ui.bookDescription.toPlainText()

        book = BookDto(ID_FOR_NEW_ITEM, title, genres, description, author)

        if self._insert_mode == InsertModes.UPDATE:
            book._id = self._selected_book._id
            self.db_module.update_book_data(book)
            self.view.show_message('Книга изменена!')
        elif self._insert_mode == InsertModes.INSERT:
            self.db_module.create_new_book(book)
            self.view.show_message('Книга добавлена!')
        else:
            self.view.show_error_message('Ошибка добавления/изменения!')
            return None

        books = self.db_module.find_all_books()
        all_books_table = self._main_window_ui.allBooksList
        self._fill_books(books, all_books_table)

        self.book_dialog.close()

    def _remove_user(self):
        '''
        Remove user
        '''

        if (self._selected_user == None):
            self.view.show_error_message('Пользователь не выбран!')
            return None

        self.db_module.delete_user(self._selected_user._id)
        self.view.show_message('Пользователь удален!')
        self._fill_users()

    def _add_book_to_collection(self):
        '''
        Add selected book id to user collection
        '''

        if (self._selected_book._id in self.current_user.collection):
            self.view.show_error_message('Книга уже в коллекции!')
            return None

        # Add book to the collection
        self.current_user.collection.append(self._selected_book._id)
        self.db_module.update_user_data(self.current_user)
        self.view.show_message('Книга добавлена в коллекцию!')

        # Update table view
        self._update_after_collection_changed()

    def _remove_book_from_collection(self):
        '''
        Remove selected book id from user collection
        '''

        if (not self._selected_book._id in self.current_user.collection):
            self.view.show_error_message('Книга не в коллекции!')
            return None

        # Remove book from the collection
        self.current_user.collection.remove(self._selected_book._id)
        self.db_module.update_user_data(self.current_user)
        self.view.show_message('Книга удалена из коллекции!')

        # Update table view
        self._update_after_collection_changed()
