from sqlalchemy import Column, Integer, String
from database import Base


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