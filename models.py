from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from datetime import datetime
from database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, default="New Chat")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class ChatMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    chat_id = Column(
        Integer,
        ForeignKey("chats.id")
    )

    role = Column(String)

    content = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )