from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    company: str
    role: str
    location: str
    status: str
    applied_date: str
    deadline_date: str | None = None
    interview_date: str | None = None
    notes: str | None = None


class ApplicationResponse(ApplicationCreate):
    id: int

    class Config:
        from_attributes = True