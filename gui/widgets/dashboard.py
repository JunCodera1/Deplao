# gui/widgets/dashboard.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QSplitter, QPushButton
from PySide6.QtCore import Slot, QSize, Qt
from .conversation_list_item import ConversationListItem
from .chat_view import ChatView
from .new_chat_dialog import NewChatDialog
from app.models import Conversation, User, Message # Dummy data for now

class Dashboard(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.conversations = {} # Store Conversation objects by ID

        self.setup_ui()
        self.connect_signals()
        self.load_dummy_data() # Replace with real data loading

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        splitter = QSplitter(self)
        
        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        left_layout.setSpacing(5)

        self.new_chat_button = QPushButton("+ New Chat")
        self.new_chat_button.setStyleSheet("padding: 8px; font-weight: bold;")

        self.convo_list_widget = QListWidget()
        self.convo_list_widget.setSpacing(2)
        self.convo_list_widget.setStyleSheet("QListWidget { border: none; background-color: #f5f5f5; }")
        
        left_layout.addWidget(self.new_chat_button)
        left_layout.addWidget(self.convo_list_widget)
        
        # Right panel: Chat View
        self.chat_view = ChatView(self.controller)
        
        splitter.addWidget(left_panel)
        splitter.addWidget(self.chat_view)
        splitter.setSizes([250, 550]) # Initial sizes
        
        layout.addWidget(splitter)

    def connect_signals(self):
        self.new_chat_button.clicked.connect(self.open_new_chat_dialog)
        self.convo_list_widget.itemClicked.connect(self.on_conversation_selected)
        self.controller.new_message_received.connect(self.update_conversation_preview)
        self.controller.new_conversation_started.connect(self.on_new_conversation)

    def open_new_chat_dialog(self):
        dialog = NewChatDialog(self.controller, self)
        dialog.exec()

    @Slot(Conversation)
    def on_new_conversation(self, conversation):
        # Check if conversation already exists in the list
        if conversation.id not in self.conversations:
            self.add_conversation(conversation)
        
        # Find and select the item
        for i in range(self.convo_list_widget.count()):
            item = self.convo_list_widget.item(i)
            if item.data(Qt.UserRole) == conversation.id:
                self.convo_list_widget.setCurrentItem(item)
                self.on_conversation_selected(item)
                break

    def load_dummy_data(self):
        # In a real app, you'd fetch this from an API endpoint
        # For now, we create dummy conversations to demonstrate the UI
        user1 = User(id=1, username="Alice")
        user2 = User(id=2, username="Bob")
        
        # Assume current user is ID 100
        if self.controller.current_user:
            me = self.controller.current_user
        else: # Fallback for testing without login
            me = User(id=100, username="Me")

        convo1 = Conversation(id=1, participants=[me, user1], last_message=Message(id=1, conversation_id=1, sender_id=1, content_type='text', content='Hey, how are you?', created_at='2023-10-27T10:00:00Z', sender_username='Alice'))
        convo2 = Conversation(id=2, participants=[me, user2], last_message=Message(id=2, conversation_id=2, sender_id=100, content_type='file', content='{"url":"/uploads/file.zip", "name":"file.zip"}', created_at='2023-10-27T09:30:00Z', sender_username='Me'))

        self.add_conversation(convo1)
        self.add_conversation(convo2)

    def add_conversation(self, conversation):
        # Prevent adding duplicates
        if conversation.id in self.conversations:
            return
            
        self.conversations[conversation.id] = conversation
        
        item_widget = ConversationListItem(conversation, self.convo_list_widget)
        list_item = QListWidgetItem(self.convo_list_widget)
        list_item.setSizeHint(item_widget.sizeHint())
        # Store conversation ID in the item for later retrieval
        list_item.setData(Qt.UserRole, conversation.id)
        
        self.convo_list_widget.addItem(list_item)
        self.convo_list_widget.setItemWidget(list_item, item_widget)

    @Slot(QListWidgetItem)
    def on_conversation_selected(self, item):
        conversation_id = item.data(Qt.UserRole)
        if conversation_id in self.conversations:
            selected_convo = self.conversations[conversation_id]
            self.chat_view.set_conversation(selected_convo)

    @Slot(Message)
    def update_conversation_preview(self, message):
        convo_id = message.conversation_id
        if convo_id in self.conversations:
            self.conversations[convo_id].last_message = message
            
            # Find the QListWidgetItem and update its widget
            for i in range(self.convo_list_widget.count()):
                item = self.convo_list_widget.item(i)
                if item.data(Qt.UserRole) == convo_id:
                    item_widget = self.convo_list_widget.itemWidget(item)
                    # This is a simple update, a better way is to have an update method
                    # in ConversationListItem
                    if message.content_type == 'text':
                        item_widget.last_message_label.setText(message.content)
                    else:
                        item_widget.last_message_label.setText(f"Sent a {message.content_type}")
                    item_widget.time_label.setText(message.display_time)
                    break
