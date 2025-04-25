from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from sqlalchemy.dialects.postgresql import UUID

from db import Base

class SubscriptionType(str, enum.Enum):
    free = "Free"
    premium = "Premium"


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    subscription = relationship("Subscription", uselist=False, back_populates="user", cascade="all, delete-orphan", lazy="joined")
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")


class Subscription(Base):
    __tablename__ = 'subscription'
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.id'))
    type = Column(Enum(SubscriptionType, native_enum=True), default=SubscriptionType.free)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="subscription")


class Chat(Base):
    __tablename__ = 'chat'
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_archived = Column(Boolean, default=False)

    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = 'message'
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey('chat.id'))
    sender = Column(String, nullable=False)  # 'user' or 'model'
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")
    attachments = relationship("Attachment", back_populates="message", cascade="all, delete-orphan")


class Attachment(Base):
    __tablename__ = 'attachment'
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    message_id = Column(BigInteger, ForeignKey('message.id'))
    file_url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)

    message = relationship("Message", back_populates="attachments")
