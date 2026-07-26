from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


# ---------------- USERS ----------------

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    applications = relationship(
        "Application",
        back_populates="user",
        cascade="all, delete"
    )


# ---------------- APPLICATIONS ----------------

class Application(Base):

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    company = Column(String, nullable=False)

    role = Column(String, nullable=False)

    location = Column(String, nullable=False)

    status = Column(String, nullable=False)

    applied_date = Column(String, nullable=False)

    deadline_date = Column(String, nullable=True)

    interview_date = Column(String, nullable=True)

    notes = Column(String, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="applications"
    )