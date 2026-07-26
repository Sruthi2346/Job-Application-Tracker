from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base

import models
import schemas
import crud
import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application Tracker API",
    version="3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = auth.verify_token(token)

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(models.User).filter(
        models.User.id == payload["user_id"]
    ).first()

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


@app.get("/")
def home():

    return {
        "message": "Job Application Tracker Backend Running - Version 3.0"
    }


# ---------------- REGISTER ----------------

@app.post("/register")
def register(
    user: schemas.UserRegister,
    db: Session = Depends(get_db)
):

    result = crud.register_user(db, user)

    if result is None:

        raise HTTPException(
            status_code=400,
            detail="Email or Username already exists"
        )

    return {
        "message": "Registration Successful"
    }


# ---------------- LOGIN ----------------

@app.post("/login", response_model=schemas.Token)
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):

    existing = crud.login_user(db, user)

    if existing is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = auth.create_access_token(
        {
            "user_id": existing.id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ---------------- CREATE APPLICATION ----------------

@app.post(
    "/applications",
    response_model=schemas.ApplicationResponse
)
def create_application(
    application: schemas.ApplicationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    result = crud.create_application(
        db,
        application,
        current_user.id
    )

    if result is None:

        raise HTTPException(
            status_code=400,
            detail="Application already exists"
        )

    return result


# ---------------- GET APPLICATIONS ----------------

@app.get(
    "/applications",
    response_model=list[schemas.ApplicationResponse]
)
def get_applications(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return crud.get_applications(
        db,
        current_user.id
    )


# ---------------- UPDATE APPLICATION ----------------

@app.put(
    "/applications/{application_id}",
    response_model=schemas.ApplicationResponse
)
def update_application(
    application_id: int,
    application: schemas.ApplicationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    result = crud.update_application(
        db,
        application_id,
        application,
        current_user.id
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return result


# ---------------- DELETE APPLICATION ----------------

@app.delete("/applications/{application_id}")
def delete_application(
    application_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    deleted = crud.delete_application(
        db,
        application_id,
        current_user.id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return {
        "message": "Application deleted successfully"
    }