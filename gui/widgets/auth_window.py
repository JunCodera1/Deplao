# gui/widgets/auth_window.py
from PySide6.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                               QPushButton, QLabel, QStackedWidget, QFrame, QMessageBox)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon

class AuthWindow(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Welcome")
        self.setMinimumSize(360, 450)

        self.stacked_widget = QStackedWidget()
        self.login_widget = self._create_login_widget()
        self.register_widget = self._create_register_widget()
        # self.forgot_password_widget = self._create_forgot_password_widget() # For future use

        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.register_widget)
        # self.stacked_widget.addWidget(self.forgot_password_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)

        self._apply_styles()
        self._connect_signals()

    def _create_login_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("Login")
        title.setObjectName("title")
        
        # Username Input
        username_layout = QVBoxLayout()
        username_layout.setSpacing(5)
        username_label = QLabel("Username")
        username_label.setObjectName("input-label")
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.login_username)

        # Password Input
        password_layout = QVBoxLayout()
        password_layout.setSpacing(5)
        password_label = QLabel("Password")
        password_label.setObjectName("input-label")
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.login_password)
        
        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("submit-button")
        
        self.login_status_label = QLabel("")
        self.login_status_label.setObjectName("status-label")

        switch_to_register = QPushButton("Don't have an account? Sign Up")
        switch_to_register.setObjectName("link-button")
        switch_to_register.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        layout.addWidget(title)
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addWidget(self.login_button)
        layout.addWidget(self.login_status_label, 0, Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(switch_to_register, 0, Qt.AlignCenter)
        
        return widget

    def _create_register_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        title = QLabel("Create Account")
        title.setObjectName("title")

        # Username Input
        username_layout = QVBoxLayout()
        username_layout.setSpacing(5)
        username_label = QLabel("Username")
        username_label.setObjectName("input-label")
        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Choose a username")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.reg_username)

        # Password Input
        password_layout = QVBoxLayout()
        password_layout.setSpacing(5)
        password_label = QLabel("Password")
        password_label.setObjectName("input-label")
        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Create a password")
        self.reg_password.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.reg_password)

        # Confirm Password Input
        confirm_layout = QVBoxLayout()
        confirm_layout.setSpacing(5)
        confirm_label = QLabel("Confirm Password")
        confirm_label.setObjectName("input-label")
        self.reg_confirm_password = QLineEdit()
        self.reg_confirm_password.setPlaceholderText("Enter your password again")
        self.reg_confirm_password.setEchoMode(QLineEdit.Password)
        confirm_layout.addWidget(confirm_label)
        confirm_layout.addWidget(self.reg_confirm_password)

        self.register_button = QPushButton("Register")
        self.register_button.setObjectName("submit-button")

        self.reg_status_label = QLabel("")
        self.reg_status_label.setObjectName("status-label")

        switch_to_login = QPushButton("Already have an account? Sign In")
        switch_to_login.setObjectName("link-button")
        switch_to_login.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        layout.addWidget(title)
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addLayout(confirm_layout)
        layout.addWidget(self.register_button)
        layout.addWidget(self.reg_status_label, 0, Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(switch_to_login, 0, Qt.AlignCenter)

        return widget

    def _connect_signals(self):
        self.login_button.clicked.connect(self.handle_login)
        self.register_button.clicked.connect(self.handle_register)

        self.controller.login_success.connect(self.on_login_success)
        self.controller.login_error.connect(self.on_login_error)
        self.controller.register_success.connect(self.on_register_success)
        self.controller.register_error.connect(self.on_register_error)

    def handle_login(self):
        username = self.login_username.text()
        password = self.login_password.text()
        if username and password:
            self.login_button.setEnabled(False)
            self.login_status_label.setText("Logging in...")
            self.controller.login(username, password)
        else:
            self.login_status_label.setText("Fields cannot be empty.")

    def handle_register(self):
        username = self.reg_username.text()
        password = self.reg_password.text()
        confirm = self.reg_confirm_password.text()

        if not (username and password and confirm):
            self.reg_status_label.setText("All fields are required.")
            return
        if password != confirm:
            self.reg_status_label.setText("Passwords do not match.")
            return
        
        self.register_button.setEnabled(False)
        self.reg_status_label.setText("Registering...")
        self.controller.register(username, password)

    @Slot(dict)
    def on_login_success(self, user_info):
        self.accept()

    @Slot(str)
    def on_login_error(self, error_msg):
        self.login_button.setEnabled(True)
        self.login_status_label.setText("")
        QMessageBox.warning(self, "Login Failed", f"Could not log in: {error_msg}")

    @Slot(dict)
    def on_register_success(self, response):
        self.register_button.setEnabled(True)
        self.reg_status_label.setText("")
        QMessageBox.information(self, "Success", "Registration successful! You can now log in.")
        self.stacked_widget.setCurrentIndex(0) # Switch to login view

    @Slot(str)
    def on_register_error(self, error_msg):
        self.register_button.setEnabled(True)
        self.reg_status_label.setText("")
        QMessageBox.warning(self, "Registration Failed", f"Could not register: {error_msg}")

    def _apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f7f9fc;
            }
            #title {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                padding-bottom: 10px;
            }
            #input-label {
                font-size: 13px;
                font-weight: bold;
                color: #555;
                padding-left: 2px;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d7;
            }
            #submit-button {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            #submit-button:hover {
                background-color: #005a9e;
            }
            #submit-button:disabled {
                background-color: #b0b0b0;
            }
            #link-button {
                background-color: transparent;
                border: none;
                color: #0078d7;
                font-size: 12px;
                text-decoration: underline;
            }
            #link-button:hover {
                color: #005a9e;
            }
            #status-label {
                color: #d32f2f; /* Red for errors */
                font-size: 12px;
            }
        """)
