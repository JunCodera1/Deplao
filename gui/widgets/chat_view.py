# gui/widgets/chat_view.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QScrollArea, QFrame, QFileDialog)
from PySide6.QtCore import Qt, Slot
from .message_bubbles import TextMessageBubble, ImageMessageBubble, FileMessageBubble, SystemMessageBubble
from app.models import Message

class ChatView(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.current_conversation_id = None
        self.current_recipient_id = None

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setProperty("class", "header")
        header_layout = QHBoxLayout(header)
        self.contact_name_label = QLabel("Select a conversation")
        self.contact_name_label.setStyleSheet("font-weight: bold;")
        self.typing_indicator_label = QLabel("")
        self.typing_indicator_label.setStyleSheet("color: gray; font-style: italic;")
        header_layout.addWidget(self.contact_name_label)
        header_layout.addStretch()
        header_layout.addWidget(self.typing_indicator_label)
        header.setStyleSheet(".header { background-color: #f0f0f0; padding: 10px; border-bottom: 1px solid #ddd; }")

        # Message Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.message_container = QWidget()
        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.addStretch()
        self.scroll_area.setWidget(self.message_container)

        # Input Bar
        input_bar = QFrame()
        input_bar.setProperty("class", "input-bar")
        input_layout = QHBoxLayout(input_bar)
        self.attach_button = QPushButton("📎")
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.send_button = QPushButton("Send")
        input_layout.addWidget(self.attach_button)
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        input_bar.setStyleSheet(".input-bar { background-color: #f0f0f0; padding: 5px; border-top: 1px solid #ddd; }")

        layout.addWidget(header)
        layout.addWidget(self.scroll_area)
        layout.addWidget(input_bar)

    def connect_signals(self):
        self.send_button.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)
        self.attach_button.clicked.connect(self.attach_file)
        
        # Connect controller signals for async operations
        self.controller.history_loaded.connect(self.display_history)
        self.controller.new_message_received.connect(self.add_message)
        self.controller.upload_complete.connect(self.on_upload_complete)
        self.controller.upload_failed.connect(lambda error_msg: self.add_system_message(f"Upload Failed: {error_msg}"))

    def set_conversation(self, conversation):
        self.clear_messages()
        self.current_conversation_id = conversation.id
        # Simple logic for 1-on-1 chat to find the other user
        self.current_recipient_id = next((p.id for p in conversation.participants if p.id != self.controller.current_user.id), None)
        
        self.contact_name_label.setText(conversation.name)
        self.add_system_message(f"Chat with {conversation.name} started.")
        self.controller.load_conversation_history(self.current_conversation_id)

    @Slot(int, list)
    def display_history(self, conversation_id, messages):
        if conversation_id != self.current_conversation_id:
            return
        for msg in messages:
            self.add_message(msg, scroll_to_bottom=False)
        self.scroll_to_bottom()

    @Slot(Message)
    def add_message(self, message, scroll_to_bottom=True):
        if message.conversation_id != self.current_conversation_id:
            return

        is_own = message.sender_id == self.controller.current_user.id
        
        if message.content_type == 'text':
            bubble = TextMessageBubble(message, is_own)
        elif message.content_type == 'image':
            bubble = ImageMessageBubble(message, is_own)
        elif message.content_type == 'file':
            bubble = FileMessageBubble(message, is_own)
        else: # system
            self.add_system_message(message.content)
            return

        # Layout to align bubble left/right
        row_layout = QHBoxLayout()
        if is_own:
            row_layout.addStretch()
            row_layout.addWidget(bubble)
        else:
            row_layout.addWidget(bubble)
            row_layout.addStretch()
        
        # Insert bubble before the final stretch
        self.message_layout.insertLayout(self.message_layout.count() - 1, row_layout)

        if scroll_to_bottom:
            self.scroll_to_bottom()

    def add_system_message(self, text):
        bubble = SystemMessageBubble(text)
        row_layout = QHBoxLayout()
        row_layout.setAlignment(Qt.AlignCenter)
        row_layout.addWidget(bubble)
        self.message_layout.insertLayout(self.message_layout.count() - 1, row_layout)

    def clear_messages(self):
        while self.message_layout.count() > 1: # Keep the stretch
            item = self.message_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # Clear nested layouts
                while item.layout().count() > 0:
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                item.layout().deleteLater()

    def send_message(self):
        text = self.message_input.text()
        if text and self.current_recipient_id:
            self.controller.send_message(self.current_recipient_id, text)
            self.message_input.clear()

    def attach_file(self):
        if not self.current_recipient_id:
            self.add_system_message("Please select a conversation first.")
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.add_system_message(f"Uploading {file_path.split('/')[-1]}...")
            self.controller.send_file(self.current_recipient_id, file_path)

    @Slot(dict)
    def on_upload_complete(self, upload_result):
        # Now that upload is done, send the actual file message
        if self.current_recipient_id:
            self.controller.send_file_message(self.current_recipient_id, upload_result)

    def scroll_to_bottom(self):
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
