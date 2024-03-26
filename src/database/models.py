from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
# from ..enums import RoleTypes
from enum import Enum

from sqlalchemy import ForeignKey, DateTime
import datetime
from sqlalchemy.sql import func


class RoleTypes(Enum):
    ADMIN = 'admin'
    VIEWER = 'viewer'


class Base(DeclarativeBase):
    create_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    deleted: Mapped[Optional[bool]]
    delete_at: Mapped[Optional[datetime.datetime]]
    pass


class Organizations(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    members: Mapped[List["Members"]] = relationship(
        back_populates="organization")
    member_keys: Mapped[List["MemberKeys"]] = relationship(
        back_populates="organization")
    keys: Mapped[List["Keys"]] = relationship(back_populates="organization")
    key_namespaces: Mapped[List["KeyNamespaces"]
                           ] = relationship(back_populates="organization")
    namespaces: Mapped[List["Namespaces"]] = relationship(
        back_populates="organization")


class Members(Base):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    name: Mapped[str]
    role: Mapped[RoleTypes] = mapped_column(nullable=False)
    organization: Mapped["Organizations"] = relationship(
        back_populates="members")
    member_key: Mapped["MemberKeys"] = relationship(
        back_populates="member")


class MemberKeys(Base):
    __tablename__ = "member_keys"
    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    key_id: Mapped[int] = mapped_column(ForeignKey("keys.id"))
    organization: Mapped["Organizations"] = relationship(
        back_populates="member_keys")
    member: Mapped["Members"] = relationship(
        back_populates="member_key")
    key: Mapped["Keys"] = relationship(back_populates="member_key")


class Keys(Base):
    __tablename__ = "keys"
    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    name: Mapped[str]
    secret: Mapped[str]
    expire_at: Mapped[datetime.datetime]
    organization: Mapped["Organizations"] = relationship(
        back_populates="keys")
    member_key: Mapped["MemberKeys"] = relationship(back_populates="key")
    key_namespace: Mapped["KeyNamespaces"] = relationship(
        back_populates="key")


class KeyNamespaces(Base):
    __tablename__ = "key_namespaces"
    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    key_id: Mapped[int] = mapped_column(ForeignKey("keys.id"))
    namespace_id: Mapped[int] = mapped_column(ForeignKey("namespaces.id"))
    organization: Mapped["Organizations"] = relationship(
        back_populates="key_namespaces")
    key: Mapped["Keys"] = relationship(back_populates="key_namespace")
    namespace: Mapped["Namespaces"] = relationship(
        back_populates="key_namespace")
    requests: Mapped[List["Requests"]] = relationship(
        back_populates="key_namespace")


class Namespaces(Base):
    __tablename__ = "namespaces"
    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    name: Mapped[str]
    description: Mapped[str]
    organization: Mapped["Organizations"] = relationship(
        back_populates="namespaces")
    key_namespace: Mapped["KeyNamespaces"] = relationship(
        back_populates="namespace")


class Requests(Base):
    __tablename__ = "requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    key_namespace_id: Mapped[int] = mapped_column(
        ForeignKey("key_namespaces.id"))
    namespace_id: Mapped[int] = mapped_column(ForeignKey("namespaces.id"))
    unit: Mapped[str]
    amount: Mapped[int]
    key_namespace: Mapped["KeyNamespaces"] = relationship(
        back_populates="requests")


class Person(Base):
    __tablename__ = "Person"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
