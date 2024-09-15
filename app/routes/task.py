
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("/{user_id}/tasks", response_model=schemas.Task)
def create_task_for_user(user_id: int, task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    return crud.create_task_for_user(db=db, task=task, user_id=user_id)

@router.get("/{user_id}/tasks", response_model=list[schemas.Task])
def get_tasks_for_user(user_id: int, db: Session = Depends(database.get_db)):
    return crud.get_tasks_for_user(db=db, user_id=user_id)

@router.post("/{user_id}/tasks/{task_id}/complete", response_model=schemas.Task)
def complete_task_for_user(user_id: int, task_id: int, db: Session = Depends(database.get_db)):
    db_task = crud.complete_task(db=db, task_id=task_id, user_id=user_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found or you're not the owner")
    return db_task
