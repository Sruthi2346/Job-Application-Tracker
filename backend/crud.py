from sqlalchemy.orm import Session

import models
import schemas
import auth


# ---------------- REGISTER ----------------

def register_user(db: Session, user: schemas.UserRegister):

    existing = db.query(models.User).filter(
        (models.User.email == user.email) |
        (models.User.username == user.username)
    ).first()

    if existing:
        return None

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=auth.hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ---------------- LOGIN ----------------

def login_user(
    db: Session,
    user: schemas.UserLogin
):

    existing = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing is None:
        return None

    if not auth.verify_password(
        user.password,
        existing.password
    ):
        return None

    return existing


# ---------------- CREATE APPLICATION ----------------

def create_application(
    db: Session,
    application: schemas.ApplicationCreate,
    user_id: int
):

    duplicate = db.query(models.Application).filter(
        models.Application.company == application.company,
        models.Application.role == application.role,
        models.Application.user_id == user_id
    ).first()

    if duplicate:
        return None

    new_application = models.Application(
        company=application.company,
        role=application.role,
        location=application.location,
        status=application.status,
        applied_date=application.applied_date,
        deadline_date=application.deadline_date,
        interview_date=application.interview_date,
        notes=application.notes,
        user_id=user_id
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


# ---------------- GET APPLICATIONS ----------------

def get_applications(
    db: Session,
    user_id: int
):

    return db.query(models.Application).filter(
        models.Application.user_id == user_id
    ).all()


# ---------------- UPDATE APPLICATION ----------------

def update_application(
    db: Session,
    application_id: int,
    application: schemas.ApplicationCreate,
    user_id: int
):

    existing = db.query(models.Application).filter(
        models.Application.id == application_id,
        models.Application.user_id == user_id
    ).first()

    if existing is None:
        return None

    existing.company = application.company
    existing.role = application.role
    existing.location = application.location
    existing.status = application.status
    existing.applied_date = application.applied_date
    existing.deadline_date = application.deadline_date
    existing.interview_date = application.interview_date
    existing.notes = application.notes

    db.commit()
    db.refresh(existing)

    return existing


# ---------------- DELETE APPLICATION ----------------

def delete_application(
    db: Session,
    application_id: int,
    user_id: int
):

    existing = db.query(models.Application).filter(
        models.Application.id == application_id,
        models.Application.user_id == user_id
    ).first()

    if existing is None:
        return False

    db.delete(existing)
    db.commit()

    return True