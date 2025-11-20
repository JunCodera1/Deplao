# gui/widgets/message_bubbles.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtGui import QPixmap, QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt, QSize

class BaseBubble(QFrame):
    """A base class for message bubbles with a rounded rectangle background."""
    def __init__(self, is_own_message, parent=None):
        super().__init__(parent)
        self.is_own_message = is_own_message
        self.setContentsMargins(10, 8, 10, 8)
        
        # Set style properties for custom painting
        self.setProperty("is_own", is_own_message)
        self.setStyleSheet("""
            QFrame[is_own="true"] {
                background-color: #dcf8c6;
                border-radius: 10px;
            }
            QFrame[is_own="false"] {
                background-color: white;
                border-radius: 10px;
            }
        """)

class TextMessageBubble(BaseBubble):
    def __init__(self, message, is_own_message, parent=None):
        super().__init__(is_own_message, parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.text_label = QLabel(message.content)
        self.text_label.setWordWrap(True)
        
        self.time_label = QLabel(message.display_time)
        self.time_label.setStyleSheet("color: gray; font-size: 9px;")
        
        layout.addWidget(self.text_label)
        layout.addWidget(self.time_label, 0, Qt.AlignRight)
        
        self.setMaximumWidth(400)

class ImageMessageBubble(BaseBubble):
    def __init__(self, message, is_own_message, parent=None):
        super().__init__(is_own_message, parent)
        # In a real app, you'd use http_client to download the image async
        # For now, we assume it's local or we can construct the URL
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_label = QLabel("<em>Loading image...</em>")
        self.image_label.setFixedSize(200, 150) # Placeholder size
        
        # TODO: Implement async image loading
        # For now, we'll just show the name
        if message.file_info:
            self.image_label.setText(f"Image: {message.file_info.name}")

        self.time_label = QLabel(message.display_time)
        self.time_label.setStyleSheet("color: gray; font-size: 9px;")

        layout.addWidget(self.image_label)
        layout.addWidget(self.time_label, 0, Qt.AlignRight)

class FileMessageBubble(BaseBubble):
    def __init__(self, message, is_own_message, parent=None):
        super().__init__(is_own_message, parent)
        
        layout = QHBoxLayout(self)
        
        # Simple file icon placeholder
        icon_label = QLabel("📄")
        icon_label.setStyleSheet("font-size: 24px;")
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        file_name = message.file_info.name if message.file_info else "Unknown File"
        self.name_label = QLabel(file_name)
        self.name_label.setStyleSheet("font-weight: bold;")
        
        self.time_label = QLabel(message.display_time)
        self.time_label.setStyleSheet("color: gray; font-size: 9px;")
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.time_label)
        
        layout.addWidget(icon_label)
        layout.addLayout(info_layout)
        
        # TODO: Add a download button and connect it

class SystemMessageBubble(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        self.label = QLabel(text)
        self.label.setStyleSheet("""
            background-color: #e1f5fe;
            color: #555;
            padding: 4px 8px;
            border-radius: 10px;
            font-size: 10px;
        """)
        layout.addWidget(self.label)
