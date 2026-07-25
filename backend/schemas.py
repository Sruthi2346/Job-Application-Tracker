from pydantic import BaseModel


class ApplicationBase(BaseModel):
    company: str
    role: str
    location: str
    status: str


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationResponse(ApplicationBase):
    id: int

    class Config:
        from_attributes = True