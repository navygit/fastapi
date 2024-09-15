
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

# Get User via user_id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Get User via username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Create User
def create_user(db: Session, user: schemas.UserCreate):
    try:
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = models.User(username=user.username, email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already registered")


# Create Task for a user
def create_task_for_user(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Get Tasks for user by user_id
def get_tasks_for_user(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

# Complete Task
def complete_task(db: Session, task_id: int, user_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id).first()
    if db_task:
        db_task.is_completed = True
        db.commit()
        db.refresh(db_task)
    return db_task

def update_user(db: Session, user_id: int, user_update: schemas.UserCreate):
    try:
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        
        # Check if username or email is taken by someone else
        existing_user = db.query(models.User).filter(models.User.username == user_update.username).first()
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=400, detail="Username already taken")

        existing_email_user = db.query(models.User).filter(models.User.email == user_update.email).first()
        if existing_email_user and existing_email_user.id != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")

        if db_user:
            db_user.username = user_update.username
            db_user.email = user_update.email
            db_user.hashed_password = user_update.password + "notreallyhashed"
            db.commit()
            db.refresh(db_user)
            return db_user
        return None
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error, possibly duplicate key.")


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

