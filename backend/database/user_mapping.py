# backend/routes/user_mapping.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.db_session import get_db
from backend.models.user_mapping import UserMapping
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/user-mapping", tags=["User Mapping"])

# 📌 Pydantic 모델 정의
class UserMappingCreate(BaseModel):
    platform: str
    platform_user_id: str
    internal_user_id: str
    alias: Optional[str] = None
    external_tool: Optional[str] = None
    external_user_id: Optional[str] = None

class UserMappingOut(UserMappingCreate):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 대응

# ✅ GET - 사용자 매핑 단건 조회
@router.get("/{platform}/{user_id}", response_model=UserMappingOut)
def get_user_mapping(platform: str, user_id: str, db: Session = Depends(get_db)):
    record = db.query(UserMapping).filter_by(
        platform=platform,
        platform_user_id=user_id
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="User mapping not found")
    return record

# ✅ POST - 사용자 매핑 등록 (UPSERT)
@router.post("/", response_model=UserMappingOut)
def upsert_user_mapping(payload: UserMappingCreate, db: Session = Depends(get_db)):
    record = UserMapping(
        platform=payload.platform,
        platform_user_id=payload.platform_user_id,
        internal_user_id=payload.internal_user_id,
        alias=payload.alias,
        external_tool=payload.external_tool,
        external_user_id=payload.external_user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.merge(record)
    db.commit()
    return record

# ✅ DELETE - 사용자 매핑 삭제
@router.delete("/{platform}/{user_id}")
def delete_user_mapping(platform: str, user_id: str, db: Session = Depends(get_db)):
    record = db.query(UserMapping).filter_by(
        platform=platform,
        platform_user_id=user_id
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="User mapping not found")
    db.delete(record)
    db.commit()
    return {"detail": "User mapping deleted"}

# ✅ LIST - 사용자 매핑 전체 조회
@router.get("/list", response_model=List[UserMappingOut])
def list_user_mappings(db: Session = Depends(get_db)):
    return db.query(UserMapping).all()
