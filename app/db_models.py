from sqlalchemy import JSON, Column, String

from app.database import Base


class UserRow(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    preferences = Column(JSON, nullable=False, default=dict)
