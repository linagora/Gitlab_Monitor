
# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com










"""Module qui va contenir les entités de la base 
de donnée. (reprendre schéma bdd)
    """

from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


group_user = Table(
    "group_user",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.user_id")),
    Column("group_id", Integer, ForeignKey("group.group_id")),
    Column("role_in_group", String),
)

project_user = Table(
    "project_user",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("project.project_id")),
    Column("user_id", Integer, ForeignKey("user.user_id")),
    Column("role_in_project", String),
)


class Project(Base):
    __tablename__ = "project"

    project_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    release = Column(String)
    visibility = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    group_id = Column(Integer, ForeignKey("group.group_id"))  # Clé étrangère vers Group

    group = relationship("Group", back_populates="projects")  # Relation one-to-many


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    projects = relationship(
        "Project", secondary=project_user, back_populates="users"
    )  # Relation many-to-many
    groups = relationship(
        "Group", secondary=group_user, back_populates="users"
    )  # Relation many-to-many


class Group(Base):
    __tablename__ = "group"

    group_id = Column(Integer, primary_key=True)
    name = Column(String)
    visibility = Column(String)
    projects = relationship("Project", back_populates="group")  # Relation one-to-many
    users = relationship(
        "User", secondary=group_user, back_populates="groups"
    )  # Relation many-to-many
