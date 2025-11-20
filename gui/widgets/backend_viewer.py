import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt

class BackendViewer(QWidget):
    """
    A widget to interact with the Node.js backend.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Backend Interaction")

        self.layout = QVBoxLayout(self)
        self.fetch_button = QPushButton("Tải dữ liệu từ Backend")
        self.result_label = QLabel("Chưa có dữ liệu")
        self.result_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.fetch_button)
        self.layout.addWidget(self.result_label)

        self.fetch_button.clicked.connect(self.fetch_data)

    def fetch_data(self):
        """
        Fetches data from the backend and updates the label.
        """
        self.result_label.setText("Đang tải...")
        try:
            # Make sure your Node.js backend is running
            response = requests.get("http://localhost:3000/api/data")
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()
            message = data.get("message", "Không có thông điệp")
            self.result_label.setText(message)
        except requests.exceptions.RequestException as e:
            self.result_label.setText("Lỗi khi kết nối tới backend!")
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối tới backend:\n{e}")
