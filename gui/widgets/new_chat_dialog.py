# gui/widgets/new_chat_dialog.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
                               QPushButton, QListWidget, QListWidgetItem, QLabel)
from PySide6.QtCore import Slot, Qt
from app.models import User

class NewChatDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Start New Chat")
        self.setMinimumWidth(300)
        
        self.users = []

        layout = QVBoxLayout(self)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by username...")
        self.search_button = QPushButton("Search")
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        
        # Results list
        self.results_list = QListWidget()
        
        layout.addLayout(search_layout)
        layout.addWidget(QLabel("Search Results:"))
        layout.addWidget(self.results_list)
        
        # Connect signals
        self.search_button.clicked.connect(self.perform_search)
        self.search_input.returnPressed.connect(self.perform_search)
        self.results_list.itemDoubleClicked.connect(self.start_chat)
        
        self.controller.user_search_success.connect(self.populate_results)
        self.controller.user_search_error.connect(self.show_search_error)

    def perform_search(self):
        query = self.search_input.text()
        if query:
            self.search_button.setEnabled(False)
            self.results_list.clear()
            self.results_list.addItem("Searching...")
            self.controller.search_users(query)

    @Slot(list)
    def populate_results(self, users):
        self.search_button.setEnabled(True)
        self.results_list.clear()
        self.users = users
        
        if not users:
            self.results_list.addItem("No users found.")
            return
            
        for user in users:
            item = QListWidgetItem(f"{user.username} (ID: {user.id})")
            item.setData(Qt.UserRole, user)
            self.results_list.addItem(item)

    @Slot(str)
    def show_search_error(self, error_msg):
        self.search_button.setEnabled(True)
        self.results_list.clear()
        self.results_list.addItem(f"Error: {error_msg}")

    def start_chat(self, item):
        user = item.data(Qt.UserRole)
        if isinstance(user, User):
            self.controller.start_new_conversation_with_user(user)
            self.accept() # Close the dialog
