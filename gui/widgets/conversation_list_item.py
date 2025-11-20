# gui/widgets/conversation_list_item.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QPainter, QColor, QBrush
from PySide6.QtCore import QSize, Qt

class ConversationListItem(QWidget):
    def __init__(self, conversation, parent=None):
        super().__init__(parent)
        self.conversation = conversation

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        # Avatar (placeholder)
        self.avatar = QLabel()
        self.avatar.setFixedSize(40, 40)
        self.avatar.setPixmap(self.create_avatar(conversation.name[0].upper()))
        
        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(0)
        
        self.name_label = QLabel(conversation.name)
        self.name_label.setStyleSheet("font-weight: bold;")
        
        last_message_text = ""
        if conversation.last_message:
            if conversation.last_message.content_type == 'text':
                last_message_text = conversation.last_message.content
            else:
                last_message_text = f"Sent a {conversation.last_message.content_type}"
        
        self.last_message_label = QLabel(last_message_text)
        self.last_message_label.setStyleSheet("color: gray;")
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.last_message_label)
        
        # Timestamp and unread count
        side_layout = QVBoxLayout()
        side_layout.setAlignment(Qt.AlignTop)
        
        timestamp = conversation.last_message.display_time if conversation.last_message else ""
        self.time_label = QLabel(timestamp)
        self.time_label.setStyleSheet("color: gray; font-size: 10px;")
        
        # Unread count (placeholder)
        self.unread_label = QLabel("3")
        self.unread_label.setAlignment(Qt.AlignCenter)
        self.unread_label.setStyleSheet("""
            background-color: #34b7f1;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 1px 5px;
            font-size: 10px;
        """)
        self.unread_label.setMinimumWidth(16)
        self.unread_label.hide() # Hidden by default

        side_layout.addWidget(self.time_label)
        side_layout.addWidget(self.unread_label, 0, Qt.AlignRight)

        layout.addWidget(self.avatar)
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addLayout(side_layout)

    def create_avatar(self, letter):
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor("#34b7f1")))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 40, 40)
        painter.setPen(QColor("white"))
        font = painter.font()
        font.setPixelSize(20)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, letter)
        painter.end()
        return pixmap
