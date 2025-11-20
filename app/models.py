# app/models.py
import json
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    is_online: bool = False

@dataclass
class FileInfo:
    url: str
    name: str
    type: str

@dataclass
class Message:
    id: int
    conversation_id: int
    sender_id: int
    content_type: str  # 'text', 'image', 'file', 'system'
    content: str
    created_at: str # Keep as string for easier parsing from JSON
    sender_username: str
    file_info: FileInfo | None = None

    def __post_init__(self):
        # Parse content for file/image messages
        if self.content_type in ['image', 'file']:
            try:
                data = json.loads(self.content)
                self.file_info = FileInfo(url=data.get('url'), name=data.get('name'), type=data.get('type'))
                # The visual bubble can now use self.file_info
            except (json.JSONDecodeError, TypeError):
                self.content_type = 'system' # Fallback if content is invalid
                self.content = "Error: Could not display received file."

    @property
    def display_time(self) -> str:
        try:
            # Assumes ISO format with timezone from backend
            dt_obj = datetime.fromisoformat(self.created_at)
            return dt_obj.strftime('%H:%M')
        except (ValueError, TypeError):
            return ''

@dataclass
class Conversation:
    id: int
    participants: list[User] = field(default_factory=list)
    last_message: Message | None = None

    @property
    def name(self) -> str:
        # For one-on-one chat, return the other participant's name
        # This needs to be adapted for group chats later
        if len(self.participants) > 1:
            # A simple implementation assuming the first participant is not the current user
            return self.participants[1].username
        elif self.participants:
            return self.participants[0].username
        return "Unknown Conversation"