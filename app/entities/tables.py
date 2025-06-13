from sqlalchemy import String, Integer, ForeignKey, Table, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import StrEnum
from uuid import uuid4
from ulid import ULID
from datetime import datetime as dt, timezone
from ..database.core import Base


friend_association = Table(
    "user_friends",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("friend_id", Integer, ForeignKey("user.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    friends = relationship(
        "User",
        secondary=friend_association,
        primaryjoin=id == friend_association.c.user_id,
        secondaryjoin=id == friend_association.c.friend_id,
        backref="friend_of",
    )

    sent_messages = relationship(
        "Message", back_populates="sender", foreign_keys="Message.from_user_id"
    )
    received_messages = relationship(
        "Message", back_populates="receiver", foreign_keys="Message.to_user_id"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username='{self.username}' email='{self.email}'>"


class Message(Base):
    __tablename__ = "message"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(ULID())
    )
    message: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[dt] = mapped_column(DateTime, default=dt.now(timezone.utc))

    from_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False
    )
    to_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False
    )

    sender = relationship(
        "User", back_populates="sent_messages", foreign_keys=[from_user_id]
    )
    receiver = relationship(
        "User", back_populates="received_messages", foreign_keys=[to_user_id]
    )


class GroupRoles(StrEnum):
    ADMIN = "admin"  # can kick other members and decide roles in the group
    MEMBER = "member"  # regular member, no special powers
    INVITOR = "invitor"  # can add/invite others


group_user = Table(
    "group_member_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("group_id", String, ForeignKey("group.group_id"), primary_key=True),
    Column("role", String, nullable=False, default=GroupRoles.MEMBER.value),
)


class Group(Base):
    group_id: Mapped[str] = mapped_column(String, default=str(uuid4()))
    group_members = relationship(
        "User", secondary="group_member_association", back_populates="groups"
    )
    group_name: Mapped[str] = mapped_column(String, nullable=False)
    group_description: Mapped[str] = mapped_column(String, nullable=True)
