# app/file_upload_manager.py
import requests
from PySide6.QtCore import QObject, Signal, QRunnable, Slot

class FileUploadSignals(QObject):
    upload_complete = Signal(dict)
    upload_error = Signal(str)

class FileUploadWorker(QRunnable):
    def __init__(self, file_path, token, host='http://localhost:3000'):
        super().__init__()
        self.file_path = file_path
        self.token = token
        self.host = host
        self.signals = FileUploadSignals()

    @Slot()
    def run(self):
        try:
            with open(self.file_path, 'rb') as f:
                files = {'file': f}
                headers = {'Authorization': f'Bearer {self.token}'}
                response = requests.post(f'{self.host}/api/upload', files=files, headers=headers)
                response.raise_for_status()
                self.signals.upload_complete.emit(response.json())
        except requests.exceptions.RequestException as e:
            self.signals.upload_error.emit(str(e))

class FileUploadManager(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        # You would typically use a QThreadPool to manage workers
    
    def upload_file(self, file_path, token):
        # In a real app, you'd create a worker and run it in a QThreadPool
        # For simplicity, this is a blocking example. Use QThreadPool for production.
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.post('http://localhost:3000/api/upload', files=files, headers=headers)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Upload failed: {e}")
            return None
