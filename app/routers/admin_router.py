from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.core.database import get_db
from app.models.models_db import User
from app.core.dependencies import get_current_active_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_active_admin)]
)

class UserStatusUpdate(BaseModel):
    status: str  # approved, pending, rejected

class UserRoleUpdate(BaseModel):
    role: str

class UserResponse(BaseModel):
    user_id: str
    username: str
    email: Optional[str]
    full_name: Optional[str]
    role: str
    approval_status: Optional[str]
    created_at: Optional[str] = None

    class Config:
        orm_mode = True

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.patch("/users/{user_id}/status")
async def update_user_status(user_id: str, status_update: UserStatusUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.approval_status = status_update.status
    db.commit()
    db.refresh(user)
    return {"message": f"User status updated to {status_update.status}"}

@router.patch("/users/{user_id}/role")
async def update_user_role(user_id: str, role_update: UserRoleUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = role_update.role
    db.commit()
    db.refresh(user)
    return {"message": f"User role updated to {role_update.role}"}
