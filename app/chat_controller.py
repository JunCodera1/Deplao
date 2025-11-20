# app/chat_controller.py
from PySide6.QtCore import QObject, Signal, Slot
from .socket_manager import SocketManager
from .http_client import HttpClient
from .models import Message, User

class ChatController(QObject):
    # Signals for the UI
    login_success = Signal(dict)
    login_error = Signal(str)
    
    register_success = Signal(dict)
    register_error = Signal(str)

    history_loaded = Signal(int, list) # conversation_id, messages
    history_load_error = Signal(str)

    upload_complete = Signal(dict)
    upload_failed = Signal(str)

    new_message_received = Signal(Message)
    user_status_changed = Signal(int, bool) # user_id, is_online
    typing_indicator_received = Signal(int, int) # conversation_id, user_id

    user_search_success = Signal(list)
    user_search_error = Signal(str)
    new_conversation_started = Signal(Conversation)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.http_client = HttpClient()
        self.socket_manager = SocketManager()
        self.current_user = None

        # Connect network client signals to controller slots
        self.http_client.login_success.connect(self.on_login_success)
        self.http_client.login_error.connect(self.login_error)
        self.http_client.register_success.connect(self.register_success)
        self.http_client.register_error.connect(self.register_error)
        self.http_client.history_success.connect(self.on_history_loaded)
        self.http_client.history_error.connect(self.history_load_error)
        self.http_client.upload_success.connect(self.upload_complete)
        self.http_client.upload_error.connect(self.upload_failed)
        self.http_client.user_search_success.connect(self.on_user_search_success)
        self.http_client.user_search_error.connect(self.user_search_error)

        # Connect socket manager signals
        self.socket_manager.message_received.connect(self.on_message_received)
        self.socket_manager.user_online.connect(lambda data: self.user_status_changed.emit(data.get('userId'), True))
        self.socket_manager.user_offline.connect(lambda data: self.user_status_changed.emit(data.get('userId'), False))
        self.socket_manager.typing_received.connect(lambda data: self.typing_indicator_received.emit(data.get('conversationId', 0), data.get('senderId')))


    def login(self, username, password):
        self.http_client.login(username, password)

    def register(self, username, password):
        self.http_client.register(username, password)

    @Slot(dict)
    def on_login_success(self, user_data):
        token = user_data.get('token')
        user_info = user_data.get('user')
        
        self.current_user = User(id=user_info['id'], username=user_info['username'])
        self.http_client.set_token(token)
        self.socket_manager.connect(token)
        
        self.login_success.emit(user_info)

    def search_users(self, query):
        if query:
            self.http_client.search_users(query)

    @Slot(list)
    def on_user_search_success(self, users_data):
        users = [User(**data) for data in users_data]
        self.user_search_success.emit(users)

    def start_new_conversation_with_user(self, user: User):
        # This is a client-side action to create a new conversation view.
        # The actual conversation is created on the backend when the first message is sent.
        if user.id == self.current_user.id:
            return # Cannot start a conversation with oneself

        # A more robust implementation would check if a conversation already exists.
        
        new_convo = Conversation(id=f"temp_{user.id}", participants=[self.current_user, user])
        self.new_conversation_started.emit(new_convo)

    def load_conversation_history(self, conversation_id):
        # Don't try to load history for temporary client-side conversations
        if isinstance(conversation_id, str) and conversation_id.startswith('temp_'):
            return
        self.http_client.get_message_history(conversation_id)

    @Slot(list)
    def on_history_loaded(self, messages_data):
        # Assuming the API returns messages for one conversation at a time
        if not messages_data:
            return

        conversation_id = messages_data[0]['conversation_id']
        messages = [Message(**msg) for msg in messages_data]
        self.history_loaded.emit(conversation_id, messages)

    def send_message(self, recipient_id, message_text):
        if not message_text.strip():
            return
        self.socket_manager.send_message(recipient_id, message_text)

    def send_file(self, recipient_id, file_path):
        # The upload process is now fully async
        # The UI should listen to upload_complete and upload_failed signals
        self.http_client.upload_file(file_path)

    @Slot(dict)
    def on_upload_complete(self, upload_result):
        # This slot is now a potential point of confusion.
        # The controller doesn't know which conversation the file was for.
        # The UI (e.g., ChatView) will need to hold the context (recipient_id)
        # and call send_file_message after receiving the upload_complete signal.
        self.upload_complete.emit(upload_result)

    def send_file_message(self, recipient_id, upload_result):
        """Called by the UI after a file upload is confirmed."""
        self.socket_manager.send_file_message(
            recipient_id,
            upload_result['fileUrl'],
            upload_result['fileName'],
            upload_result['fileType']
        )

    @Slot(dict)
    def on_message_received(self, message_data):
        message = Message(**message_data)
        self.new_message_received.emit(message)

    def send_typing_notification(self, recipient_id):
        self.socket_manager.send_typing_notification(recipient_id)

    def shutdown(self):
        self.socket_manager.disconnect()
