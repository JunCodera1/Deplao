# app/socket_manager.py
import socketio
from PySide6.QtCore import QObject, Signal

class SocketManager(QObject):
    # Signals to be emitted when an event is received
    connected = Signal()
    disconnected = Signal()
    message_received = Signal(dict)
    user_online = Signal(dict)
    user_offline = Signal(dict)
    typing_received = Signal(dict)
    connect_error = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sio = socketio.Client()
        self.register_handlers()

    def register_handlers(self):
        @self.sio.event
        def connect():
            self.connected.emit()

        @self.sio.event
        def disconnect():
            self.disconnected.emit()

        @self.sio.on('message:receive')
        def on_message(data):
            self.message_received.emit(data)
        
        @self.sio.on('status:user-online')
        def on_user_online(data):
            self.user_online.emit(data)

        @self.sio.on('status:user-offline')
        def on_user_offline(data):
            self.user_offline.emit(data)

        @self.sio.on('typing')
        def on_typing(data):
            self.typing_received.emit(data)

        @self.sio.event
        def connect_error(data):
            self.connect_error.emit(data)

    def connect(self, token, host='http://localhost:3000'):
        try:
            self.sio.connect(host, auth={'token': token})
        except socketio.exceptions.ConnectionError as e:
            self.connect_error.emit(e)

    def disconnect(self):
        self.sio.disconnect()

    def send_message(self, recipient_id, content):
        self.sio.emit('message:send', {'recipientId': recipient_id, 'content': content})

    def send_file_message(self, recipient_id, file_url, file_name, file_type):
        self.sio.emit('file:send', {
            'recipientId': recipient_id,
            'fileUrl': file_url,
            'fileName': file_name,
            'fileType': file_type,
        })
    
    def send_typing_notification(self, recipient_id):
        self.sio.emit('typing', {'recipientId': recipient_id})
