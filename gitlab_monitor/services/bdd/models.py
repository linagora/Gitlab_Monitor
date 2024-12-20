# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


"""
Module that contains the database entities. (refer to the database schema)

Mypy type ignore due to the fact that the sqlalchemy module is not typed
(error: Module "sqlalchemy.orm" has no attribute "declarative_base [attr-defined] and
error: Module "sqlalchemy.orm" has no attribute "Mapped"; maybe "Mapper"?  [attr-defined]).
"""

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import declarative_base  # type: ignore
from sqlalchemy.orm import relationship


Base = declarative_base()


class Project(Base):  # type: ignore # pylint: disable=too-few-public-methods
    """Dimension table Project."""

    __tablename__ = "project"

    project_id = Column(Integer, primary_key=True)
    # group_id = Column(Integer, ForeignKey('group.group_id')) # Clé étrangère vers Group
    name = Column(String, nullable=False)
    path = Column(String)
    description = Column(String)
    release = Column(String)
    visibility = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # group = relationship('Group', back_populates='projects')
    # project_users = relationship('ProjectUser', back_populates='project')
    commits: Mapped[list["Commit"]] = relationship("Commit", back_populates="project")


#     merge_requests = relationship('MergeRequest', back_populates='project')


# # Table de dimension : Group
# class Group(Base):
#     __tablename__ = 'group'

#     group_id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     visibility = Column(String)

#     projects = relationship('Project', back_populates='group')
#     group_users = relationship('GroupUser', back_populates='group')
#     commits = relationship('Commit', back_populates='group')
#     merge_requests = relationship('MergeRequest', back_populates='group')


# # Table de dimension : User
# class User(Base):
#     __tablename__ = 'user'

#     user_id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)

#     project_users = relationship('ProjectUser', back_populates='user')
#     group_users = relationship('GroupUser', back_populates='user')
#     commits = relationship('Commit', back_populates='user')
#     merge_requests = relationship('MergeRequest', back_populates='user')


# # Table de dimension : Datetime
# class Datetime(Base):
#     __tablename__ = 'datetime'

#     date_id = Column(Integer, primary_key=True)
#     date = Column(DateTime, nullable=False)
#     year = Column(Integer)
#     month = Column(Integer)
#     day = Column(Integer)
#     day_name = Column(String)
#     month_name = Column(String)

#     commits = relationship('Commit', back_populates='datetime')
#     merge_requests = relationship('MergeRequest', back_populates='datetime')


# Table de faits : Commit
class Commit(Base):  # type: ignore # pylint: disable=too-few-public-methods
    """Fact table Commit."""

    __tablename__ = "commit"

    commit_id = Column(String, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.project_id"))
    message = Column(Text)
    date = Column(DateTime)
    author = Column(String)
    # date_id = Column(Integer, ForeignKey('datetime.date_id'))
    # group_id = Column(Integer, ForeignKey('group.group_id'))
    # merge_request_id = Column(Integer, ForeignKey('merge_request.merge_request_id'))
    # user_id = Column(Integer, ForeignKey('user.user_id'))

    project: Mapped["Project"] = relationship("Project", back_populates="commits")
    # datetime = relationship('Datetime', back_populates='commits')
    # group = relationship('Group', back_populates='commits')
    # user = relationship('User', back_populates='commits')
    # merge_request = relationship('MergeRequest', back_populates='commits')


# # Table de faits : MergeRequest
# class MergeRequest(Base):
#     __tablename__ = 'merge_request'

#     merge_request_id = Column(Integer, primary_key=True)
#     project_id = Column(Integer, ForeignKey('project.project_id'))
#     group_id = Column(Integer, ForeignKey('group.group_id'))
#     user_id = Column(Integer, ForeignKey('user.user_id'))
#     date_id = Column(Integer, ForeignKey('datetime.date_id'))
#     commit_id = Column(Integer, ForeignKey('commit.commit_id'))
#     reviewer_id = Column(Integer, ForeignKey('user.user_id'))

#     project = relationship('Project', back_populates='merge_requests')
#     group = relationship('Group', back_populates='merge_requests')
#     user = relationship('User', foreign_keys=[user_id], back_populates='merge_requests')
#     reviewer = relationship('User', foreign_keys=[reviewer_id])
#     datetime = relationship('Datetime', back_populates='merge_requests')
#     commits = relationship('Commit', back_populates='merge_request')


# # Table d'association : ProjectUser
# class ProjectUser(Base):
#     __tablename__ = 'project_user'

#     project_id = Column(Integer, ForeignKey('project.project_id'), primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
#     role_in_project = Column(String)

#     project = relationship('Project', back_populates='project_users')
#     user = relationship('User', back_populates='project_users')


# # Table d'association : GroupUser
# class GroupUser(Base):
#     __tablename__ = 'group_user'

#     group_id = Column(Integer, ForeignKey('group.group_id'), primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
#     role_in_group = Column(String)

#     group = relationship('Group', back_populates='group_users')
#     user = relationship('User', back_populates='group_users')
