from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

def create_task(db: Session, task_data: TaskCreate, user_id: int) -> Task:
    task = Task(**task_data.model_dump(), user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session, user_id: int, status: str = None, priority: str = None):
    query = db.query(Task).filter(Task.user_id == user_id)
    if status == "completed":
        query = query.filter(Task.completed == True)
    elif status == "pending":
        query = query.filter(Task.completed == False)
    if priority:
        query = query.filter(Task.priority == priority)
    return query.all()

def get_task_by_id(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

def update_task(db: Session, task_id: int, user_id: int, task_data: TaskUpdate):
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        return None
    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True

def search_tasks(db: Session, user_id: int, query: str):
    return db.query(Task).filter(
        Task.user_id == user_id,
        or_(
            Task.title.ilike(f"%{query}%"),
            Task.description.ilike(f"%{query}%")
        )
    ).all()

def get_dashboard_stats(db: Session, user_id: int):
    all_tasks = db.query(Task).filter(Task.user_id == user_id).all()
    now = datetime.utcnow()
    return {
        "total": len(all_tasks),
        "completed": sum(1 for t in all_tasks if t.completed),
        "pending": sum(1 for t in all_tasks if not t.completed),
        "overdue": sum(1 for t in all_tasks if not t.completed and t.due_date and t.due_date.replace(tzinfo=None) < now)
    }