from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.analytics_model import AnalyticsData
from app.models.models_db import Task, Machine, OutsourceItem
from app.core.database import get_db
from collections import Counter

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=AnalyticsData)
async def get_analytics(db: Session = Depends(get_db)):
    # 1. Task Stats
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "completed").count()
    pending_tasks = db.query(Task).filter(Task.status == "pending").count()
    
    # Group by priority
    priority_counts = db.query(Task.priority, func.count(Task.priority)).group_by(Task.priority).all()
    tasks_by_priority = {p: count for p, count in priority_counts if p}
    
    # Group by status
    status_counts = db.query(Task.status, func.count(Task.status)).group_by(Task.status).all()
    tasks_by_status = {s: count for s, count in status_counts if s}
    
    # 2. Machine Usage
    machine_usage_counts = db.query(Task.machine_id, func.count(Task.machine_id)).filter(Task.machine_id != None).group_by(Task.machine_id).all()
    machine_usage = {m: count for m, count in machine_usage_counts if m}
    
    # 3. Revenue Estimation (Placeholder logic)
    # Sum of hourly rates of active machines? Or just a placeholder value for now.
    # Let's sum the cost of outsource items for now as a different metric, or keep it 0.
    revenue_estimated = 0.0
    
    return AnalyticsData(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        tasks_by_priority=tasks_by_priority,
        tasks_by_status=tasks_by_status,
        machine_usage=machine_usage,
        revenue_estimated=revenue_estimated
    )
