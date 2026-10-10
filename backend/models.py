
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from database import Base


# ---------------- USERS ----------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False)

    email = Column(String(255), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    applications = relationship(
        "Application",
        back_populates="user",
        cascade="all, delete"
    )


# ---------------- APPLICATIONS ----------------

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    company = Column(String(255), nullable=False)

    role = Column(String(255), nullable=False)

    location = Column(String(255), nullable=False)

    status = Column(String(50), nullable=False)

    applied_date = Column(String(30), nullable=False)

    deadline_date = Column(String(30), nullable=True)

    interview_date = Column(String(30), nullable=True)

    notes = Column(Text, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="applications"
    )
