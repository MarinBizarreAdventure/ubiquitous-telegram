import json
from pathlib import Path

from app.models import User


class UserStorage:
    def __init__(self, data_dir: str) -> None:
        self._path = Path(data_dir) / "app_data.json"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._write({"users": {}})

    def _read(self) -> dict:
        with open(self._path) as f:
            return json.load(f)

    def _write(self, data: dict) -> None:
        with open(self._path, "w") as f:
            json.dump(data, f, indent=2)

    def get(self, user_id: str) -> User | None:
        raw = self._read()["users"].get(user_id)
        if raw is None:
            return None
        return User(**raw)

    def save(self, user: User) -> User:
        data = self._read()
        data["users"][user.id] = {
            "id": user.id,
            "name": user.name,
            "city": user.city,
            "preferences": user.preferences,
        }
        self._write(data)
        return user
