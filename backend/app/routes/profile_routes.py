from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..database import get_db
from ..models.models import User
from ..models.schemas import ProfileUpdate, ProfileResponse

router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.get("", response_model=ProfileResponse)
def get_profile(user: User = Depends(get_current_user)):
    return user


@router.put("", response_model=ProfileResponse)
def update_profile(
    data: ProfileUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    for field, value in data.model_dump().items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user
