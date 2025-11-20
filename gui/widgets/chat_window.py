# gui/widgets/chat_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QTextEdit, QPushButton, QLineEdit,
    QSplitter, QFileDialog
)
# Make sure to import your controller
# from app.chat_controller import ChatController

class ChatWindow(QMainWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.current_recipient_id = None # Example recipient

        self.setWindowTitle("Deplao Chat")
        self.setGeometry(100, 100, 800, 600)

        # --- Main Layout ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        splitter = QSplitter()
        main_layout.addWidget(splitter)

        # --- Left Panel (Contacts) ---
        self.contact_list = QListWidget()
        # In a real app, you would populate this from a user list
        self.contact_list.addItem("User 1 (ID: 1)")
        self.contact_list.addItem("User 2 (ID: 2)")
        self.contact_list.itemClicked.connect(self.on_contact_selected)
        splitter.addWidget(self.contact_list)

        # --- Right Panel (Chat Area) ---
        chat_panel = QWidget()
        chat_layout = QVBoxLayout(chat_panel)
        
        self.message_view = QTextEdit()
        self.message_view.setReadOnly(True)
        
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.send_button = QPushButton("Send")
        self.attach_button = QPushButton("Attach")

        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.attach_button)

        chat_layout.addWidget(self.message_view)
        chat_layout.addLayout(input_layout)
        splitter.addWidget(chat_panel)

        splitter.setSizes([200, 600])

        # --- Connect Signals ---
        self.send_button.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)
        self.attach_button.clicked.connect(self.attach_file)
        
        # Connect controller signals to UI slots
        self.controller.socket_manager.message_received.connect(self.display_message)

    def on_contact_selected(self, item):
        # A simple way to get the recipient ID from the contact list text
        try:
            # Assumes format "Username (ID: 123)"
            self.current_recipient_id = int(item.text().split('(ID: ')[1][:-1])
            self.message_view.clear()
            self.message_view.append(f"--- Chat with {item.text()} ---")
        except (IndexError, ValueError):
            print("Could not parse recipient ID from contact item.")
            self.current_recipient_id = None

    def send_message(self):
        if self.current_recipient_id is None:
            self.message_view.append("<i>Please select a contact to chat with.</i>")
            return
            
        text = self.message_input.text()
        if text:
            self.controller.send_message(self.current_recipient_id, text)
            self.message_input.clear()

    def attach_file(self):
        if self.current_recipient_id is None:
            self.message_view.append("<i>Please select a contact to chat with before sending a file.</i>")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Send")
        if file_path:
            self.controller.send_file(self.current_recipient_id, file_path)

    def display_message(self, message):
        # This is a very basic display. A real app would use a more complex view.
        sender = "You" if message['sender_id'] != self.current_recipient_id else f"User {message['sender_id']}"
        
        content = message['content']
        if message['content_type'] != 'text':
            import json
            try:
                file_info = json.loads(content)
                content = f"File: {file_info.get('name', 'N/A')} ({file_info.get('url', '')})"
            except json.JSONDecodeError:
                content = "Received a file (could not parse details)."

        self.message_view.append(f"<b>{sender}:</b> {content}")

# Example of how to run this (you would integrate this into your main app)
# if __name__ == '__main__':
#     import sys
#     from PySide6.QtWidgets import QApplication
# 
#     app = QApplication(sys.argv)
#     
#     # 1. Perform login
#     # In a real app, you'd have a login window first
#     controller = ChatController()
#     user = controller.login("testuser", "password123") # Use a valid user
# 
#     if user:
#         # 2. If login is successful, show the main chat window
#         window = ChatWindow(controller)
#         window.show()
#         sys.exit(app.exec())
#     else:
#         print("Login failed. Exiting.")
#         sys.exit(-1)

