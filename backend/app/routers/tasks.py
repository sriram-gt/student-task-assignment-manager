from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service
from app.routers.auth import get_authenticated_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_authenticated_user)):
    return task_service.create_task(db, task, current_user.id)

@router.get("", response_model=List[TaskResponse])
def get_tasks(status: Optional[str] = None, priority: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_authenticated_user)):
    return task_service.get_tasks(db, current_user.id, status, priority)

@router.get("/search", response_model=List[TaskResponse])
def search(q: str = Query(..., min_length=1), db: Session = Depends(get_db), current_user: User = Depends(get_authenticated_user)):
    return task_service.search_tasks(db, current_user.id, q)

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_authenticated_user)):
    return task_service.get_dashboard_stats(db, current_user.id)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_authenticated_user)):
    task = task_service.get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_authenticated_user)):
    updated = task_service.update_task(db, task_id, current_user.id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_authenticated_user)):
    if not task_service.delete_task(db, task_id, current_user.id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}