import uuid

from app.domain.entities import User
from app.domain.ports import StoragePort


class UserUseCase:
    def __init__(self, storage: StoragePort) -> None:
        self._storage = storage

    def create_user(self, name: str, city: str, preferences: dict) -> User:
        user = User(id=str(uuid.uuid4()), name=name, city=city, preferences=preferences)
        return self._storage.save_user(user)

    def get_user(self, user_id: str) -> User:
        user = self._storage.get_user(user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")
        return user

    def update_user(self, user_id: str, name: str | None, city: str | None, preferences: dict | None) -> User:
        user = self.get_user(user_id)
        if name is not None:
            user.name = name
        if city is not None:
            user.city = city
        if preferences is not None:
            user.preferences = preferences
        return self._storage.save_user(user)

    def delete_user(self, user_id: str) -> None:
        self.get_user(user_id)
        self._storage.delete_user(user_id)
