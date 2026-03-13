import json
from pathlib import Path

from app.models import User


class JsonUserStorage:
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


class PostgresUserStorage:
    def get(self, user_id: str) -> User | None:
        from app.database import get_session
        from app.db_models import UserRow

        with get_session() as session:
            row = session.get(UserRow, user_id)
            if row is None:
                return None
            return User(id=row.id, name=row.name, city=row.city, preferences=row.preferences or {})

    def save(self, user: User) -> User:
        from app.database import get_session
        from app.db_models import UserRow

        with get_session() as session:
            existing = session.get(UserRow, user.id)
            if existing:
                existing.name = user.name
                existing.city = user.city
                existing.preferences = user.preferences
            else:
                session.add(UserRow(id=user.id, name=user.name, city=user.city, preferences=user.preferences))
            session.commit()
        return user


def create_storage(database_url: str | None, data_dir: str) -> JsonUserStorage | PostgresUserStorage:
    if database_url:
        from app.database import init_db
        init_db(database_url)
        return PostgresUserStorage()
    return JsonUserStorage(data_dir)
