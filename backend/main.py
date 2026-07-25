from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base

import schemas
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application Tracker API",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "Job Application Tracker Backend Running"
    }


@app.post("/applications", response_model=schemas.ApplicationResponse)
def create_application(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db)
):

    result = crud.create_application(db, application)

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Application already exists"
        )

    return result


@app.get("/applications", response_model=list[schemas.ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    return crud.get_applications(db)


@app.put("/applications/{application_id}",
         response_model=schemas.ApplicationResponse)
def update_application(
    application_id: int,
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db)
):

    result = crud.update_application(
        db,
        application_id,
        application
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return result


@app.delete("/applications/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
):

    deleted = crud.delete_application(
        db,
        application_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return {
        "message": "Application deleted successfully"
    }