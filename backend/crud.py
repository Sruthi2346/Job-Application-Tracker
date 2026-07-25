from sqlalchemy.orm import Session
import models
import schemas


def create_application(db: Session, application: schemas.ApplicationCreate):
    duplicate = db.query(models.Application).filter(
        models.Application.company == application.company,
        models.Application.role == application.role
    ).first()

    if duplicate:
        return None

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


def get_applications(db: Session):
    return db.query(models.Application).all()


def update_application(db: Session, application_id: int, application: schemas.ApplicationCreate):
    existing = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()

    if not existing:
        return None

    existing.company = application.company
    existing.role = application.role
    existing.location = application.location
    existing.status = application.status

    db.commit()
    db.refresh(existing)

    return existing


def delete_application(db: Session, application_id: int):
    existing = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()

    if not existing:
        return False

    db.delete(existing)
    db.commit()

    return True