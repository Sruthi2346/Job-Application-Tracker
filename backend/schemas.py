from pydantic import BaseModel, EmailStr


# ---------------- USER REGISTER ----------------

class UserRegister(BaseModel):

    username: str

    email: EmailStr

    password: str


# ---------------- USER LOGIN ----------------

class UserLogin(BaseModel):

    email: EmailStr

    password: str


# ---------------- TOKEN ----------------

class Token(BaseModel):

    access_token: str

    token_type: str


# ---------------- APPLICATION ----------------

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

    user_id: int

    class Config:

        from_attributes = True