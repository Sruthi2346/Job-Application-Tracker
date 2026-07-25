from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application Tracker API",
    version="2.0"
)

# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Database ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Home ----------------

@app.get("/")
def home():
    return {
        "message": "Job Application Tracker Backend Running"
    }

# ---------------- Create ----------------

@app.post("/applications", response_model=schemas.ApplicationResponse)
def create_application(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db)
):

    duplicate = db.query(models.Application).filter(
        models.Application.company == application.company,
        models.Application.role == application.role
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Application already exists"
        )

    new_application = models.Application(
        company=application.company,
        role=application.role,
        location=application.location,
        status=application.status
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application

# ---------------- Read ----------------

@app.get("/applications", response_model=list[schemas.ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    return db.query(models.Application).all()

# ---------------- Update ----------------

@app.put("/applications/{application_id}",
         response_model=schemas.ApplicationResponse)
def update_application(
    application_id: int,
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    existing.company = application.company
    existing.role = application.role
    existing.location = application.location
    existing.status = application.status

    db.commit()
    db.refresh(existing)

    return existing

# ---------------- Delete ----------------

@app.delete("/applications/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
):

    existing = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    db.delete(existing)
    db.commit()

    return {
        "message": "Application deleted successfully"
    }