from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
from src.enums import RoleTypes

from sqlalchemy import ForeignKey, DateTime
import datetime
from sqlalchemy.sql import func


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


"""
class OrganizationDb(BaseDb):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"OrganizationDb(id={self.id!r}, name={self.name!r})"


class MemberDb(BaseDb):
    __tablename__ = "members"

    id: Mapped[str] = mapped_column(primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey(
            f"{OrganizationDb.__tablename__}.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )
    uid: Mapped[str] = mapped_column(String())
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32))

    def __repr__(self) -> str:
        details = ", ".join(
            [
                f"id={self.id!r}",
                f"org_id={self.org_id!r}",
                f"name={self.name!r}",
                f"role={self.role!r}",
            ]
        )
        return f"MemberDb({details})"


class APIKeyDb(BaseDb):
    __tablename__ = "api_keys"

    id: Mapped[str] = mapped_column(primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey(
            f"{OrganizationDb.__tablename__}.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )
    name: Mapped[str] = mapped_column(String(255))
    key: Mapped[str] = mapped_column(String(512))
    expire_at: Mapped[Optional[datetime]] = mapped_column(default=None, nullable=True)

    def __repr__(self) -> str:
        details = ", ".join(
            [
                f"id={self.id!r}",
                f"org_id={self.org_id!r}",
                f"name={self.name!r}",
                f"key={self.key[:3]}***{self.key[-3:]}",
                f"expire_at={self.expire_at!r}",
            ]
        )
        return f"APIKeyDb({details})"


class NamespaceDb(BaseDb):
    __tablename__ = "namespaces"

    id: Mapped[str] = mapped_column(primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey(
            f"{OrganizationDb.__tablename__}.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )
    description: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        details = ", ".join(
            [
                f"id={self.id!r}",
                f"org_id={self.org_id!r}",
                f"description={self.description!r}",
            ]
        )
        return f"Namespace({details})"


class MemberKeyDb(BaseDb):
    __tablename__ = "member_keys"

    id: Mapped[str] = mapped_column(primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey(
            f"{OrganizationDb.__tablename__}.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )
    member_id: Mapped[str] = mapped_column(
        ForeignKey(
            f"{MemberDb.__tablename__}.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )
    key_id: Mapped[str] = mapped_column(
        ForeignKey(
            f"{APIKeyDb.__tablename__}.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )

    def __repr__(self) -> str:
        details = ", ".join(
            [
                f"id={self.id!r}",
                f"org_id={self.org_id!r}",
                f"member_id={self.member_id!r}",
                f"key_id={self.key_id!r}",
            ]
        )
        return f"MemberKeyDb({details})"


class NamespaceKeyDb(BaseDb):
    __tablename__ = "namespace_keys"

    id: Mapped[str] = mapped_column(primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey(
            f"{OrganizationDb.__tablename__}.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )
    namespace_id: Mapped[str] = mapped_column(
        ForeignKey(
            f"{NamespaceDb.__tablename__}.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )
    key_id: Mapped[str] = mapped_column(
        ForeignKey(
            f"{APIKeyDb.__tablename__}.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        )
    )

    def __repr__(self) -> str:
        details = ", ".join(
            [
                f"id={self.id!r}",
                f"org_id={self.org_id!r}",
                f"key_id={self.key_id!r}",
            ]
        )
        return f"MemberKeyDb({details})"

"""
