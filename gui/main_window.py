# gui/main_window.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from app.chat_controller import ChatController
from .widgets.auth_window import AuthWindow
from .widgets.dashboard import Dashboard

class MainWindow(QMainWindow):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Deplao Messenger")
        self.setGeometry(100, 100, 800, 600)

        # The main view after login
        self.dashboard = Dashboard(self.controller)
        self.setCentralWidget(self.dashboard)

    def closeEvent(self, event):
        """Ensure sockets are closed on exit."""
        self.controller.shutdown()
        event.accept()

def run_app():
    app = QApplication(sys.argv)
    
    # Controller is the core of the app, created first
    chat_controller = ChatController()

    # Show auth window first
    auth_dialog = AuthWindow(chat_controller)
    
    # If login is successful, show the main window
    if auth_dialog.exec() == QDialog.Accepted:
        main_window = MainWindow(chat_controller)
        main_window.show()
        sys.exit(app.exec())
    else:
        # User closed the login dialog or failed to log in
        sys.exit(0)
