# app/http_client.py
import requests
from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThreadPool

class HttpClientSignals(QObject):
    request_finished = Signal(object)
    request_error = Signal(str)

class ApiWorker(QRunnable):
    def __init__(self, method, url, headers=None, json_data=None, files=None):
        super().__init__()
        self.method = method
        self.url = url
        self.headers = headers
        self.json_data = json_data
        self.files = files
        self.signals = HttpClientSignals()

    @Slot()
    def run(self):
        try:
            response = requests.request(
                self.method,
                self.url,
                headers=self.headers,
                json=self.json_data,
                files=self.files,
                timeout=10 # 10-second timeout
            )
            response.raise_for_status()
            self.signals.request_finished.emit(response.json())
        except requests.exceptions.RequestException as e:
            error_message = str(e)
            if e.response is not None:
                error_message = f"{e.response.status_code}: {e.response.text}"
            self.signals.request_error.emit(error_message)
        except json.JSONDecodeError:
            self.signals.request_error.emit("Failed to decode server response.")

class HttpClient(QObject):
    BASE_URL = "http://localhost:3000"
    
    login_success = Signal(dict)
    login_error = Signal(str)

    register_success = Signal(dict)
    register_error = Signal(str)
    
    history_success = Signal(list)
    history_error = Signal(str)

    upload_success = Signal(dict)
    upload_error = Signal(str)

    user_search_success = Signal(list)
    user_search_error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread_pool = QThreadPool()
        self.token = None

    def _create_headers(self):
        if not self.token:
            return {}
        return {'Authorization': f'Bearer {self.token}'}

    def _execute_request(self, method, endpoint, on_success, on_error, json_data=None, files=None):
        # To support search, we need to handle params for GET requests
        url = f"{self.BASE_URL}{endpoint}"
        worker = ApiWorker(
            method=method,
            url=url,
            headers=self._create_headers(),
            json_data=json_data,
            files=files
        )
        worker.signals.request_finished.connect(on_success)
        worker.signals.request_error.connect(on_error)
        self.thread_pool.start(worker)

    def login(self, username, password):
        self._execute_request(
            'POST', '/api/auth/login',
            self.login_success.emit,
            self.login_error.emit,
            json_data={'username': username, 'password': password}
        )

    def register(self, username, password):
        self._execute_request(
            'POST', '/api/auth/register',
            self.register_success.emit,
            self.register_error.emit,
            json_data={'username': username, 'password': password}
        )

    def search_users(self, query):
        self._execute_request(
            'GET', f'/api/users/search?q={query}',
            self.user_search_success.emit,
            self.user_search_error.emit
        )

    def get_message_history(self, conversation_id):
        self._execute_request(
            'GET', f'/api/chat/{conversation_id}/messages',
            self.history_success.emit,
            self.history_error.emit
        )

    def upload_file(self, file_path):
        try:
            # File opening must be done in the main thread
            file_handle = open(file_path, 'rb')
            files = {'file': (file_path.split('/')[-1], file_handle)}
            self._execute_request(
                'POST', '/api/upload',
                self.upload_success.emit,
                self.upload_error.emit,
                files=files
            )
        except IOError as e:
            self.upload_error.emit(f"Failed to open file: {e}")

    def set_token(self, token):
        self.token = token
