import json
import os
from pathlib import Path

from app.domain.entities import ChatMessage, ChatSession, User
from app.domain.ports import StoragePort


class JsonFileStorage(StoragePort):
    def __init__(self, data_dir: str) -> None:
        self._path = Path(data_dir) / "app_data.json"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._write({"users": {}, "sessions": {}})

    def _read(self) -> dict:
        with open(self._path, "r") as f:
            return json.load(f)

    def _write(self, data: dict) -> None:
        with open(self._path, "w") as f:
            json.dump(data, f, indent=2)

    def get_user(self, user_id: str) -> User | None:
        data = self._read()
        raw = data["users"].get(user_id)
        if raw is None:
            return None
        return User(**raw)

    def save_user(self, user: User) -> User:
        data = self._read()
        data["users"][user.id] = {
            "id": user.id,
            "name": user.name,
            "city": user.city,
            "preferences": user.preferences,
        }
        self._write(data)
        return user

    def delete_user(self, user_id: str) -> None:
        data = self._read()
        data["users"].pop(user_id, None)
        data["sessions"] = {
            sid: s for sid, s in data["sessions"].items() if s["user_id"] != user_id
        }
        self._write(data)

    def get_session(self, session_id: str) -> ChatSession | None:
        data = self._read()
        raw = data["sessions"].get(session_id)
        if raw is None:
            return None
        messages = [ChatMessage(**m) for m in raw["messages"]]
        return ChatSession(id=raw["id"], user_id=raw["user_id"], messages=messages)

    def save_session(self, session: ChatSession) -> ChatSession:
        data = self._read()
        data["sessions"][session.id] = {
            "id": session.id,
            "user_id": session.user_id,
            "messages": [
                {"role": m.role, "content": m.content, "timestamp": m.timestamp}
                for m in session.messages
            ],
        }
        self._write(data)
        return session

    def delete_session(self, session_id: str) -> None:
        data = self._read()
        data["sessions"].pop(session_id, None)
        self._write(data)

    def get_sessions_by_user(self, user_id: str) -> list[ChatSession]:
        data = self._read()
        sessions = []
        for raw in data["sessions"].values():
            if raw["user_id"] == user_id:
                messages = [ChatMessage(**m) for m in raw["messages"]]
                sessions.append(ChatSession(id=raw["id"], user_id=raw["user_id"], messages=messages))
        return sessions
