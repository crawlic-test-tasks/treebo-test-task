from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class IntModel(SQLModel):
    id: Optional[int] = Field(primary_key=True, default=None)


class User(IntModel, table=True):
    __tablename__ = "users"

    name: str
    email: str
    telegram_id: int

    notes: list["Note"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "order_by": "Note.reminder_time.desc()",
        },
    )


class Note(IntModel, table=True):
    __tablename__ = "notes"

    user_id: int = Field(foreign_key="users.id")
    text: str
    reminder_time: datetime

    user: User = Relationship(back_populates="notes")
