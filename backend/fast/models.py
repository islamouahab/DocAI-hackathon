from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import Base

class SubscriptionType(str, enum.Enum):
    free = "Free"
    premium = "Premium"

class User(Base):
    __tablename__ = 'api_users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    subscription = relationship("Subscription", uselist=False, back_populates="user", cascade="all, delete-orphan")
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")

class Subscription(Base):
    __tablename__ = 'api_subscriptions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('api_users.id'))
    type = Column(Enum(SubscriptionType, native_enum=True), default=SubscriptionType.free)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="subscription")

class Chat(Base):
    __tablename__ = 'api_chats'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('api_users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_archived = Column(Boolean, default=False)

    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = 'api_messages'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey('api_chats.id'))
    sender = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")
    attachments = relationship("Attachment", back_populates="message", cascade="all, delete-orphan")

class Attachment(Base):
    __tablename__ = 'api_attachments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey('api_messages.id'))
    file_url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)

    message = relationship("Message", back_populates="attachments")
