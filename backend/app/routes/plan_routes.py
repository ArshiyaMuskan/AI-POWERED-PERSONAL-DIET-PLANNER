from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..database import get_db
from ..models.models import User, DietPlan
from ..models.schemas import PlanResponse
from ..services.ai_service import generate_plan

router = APIRouter(prefix="/api/plans", tags=["Diet Plans"])


@router.post("/generate", response_model=PlanResponse, status_code=201)
def generate_diet_plan(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user.dietary_preference or not user.goal:
        raise HTTPException(
            status_code=400,
            detail="Complete dietary preference and goal in your profile first",
        )

    plan_data, _source = generate_plan({
        "age": user.age,
        "height": user.height,
        "weight": user.weight,
        "activity_level": user.activity_level,
        "dietary_preference": user.dietary_preference,
        "goal": user.goal,
        "allergies": user.allergies,
    })

    plan = DietPlan(user_id=user.id, **plan_data)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("", response_model=list[PlanResponse])
def list_plans(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(DietPlan)
        .filter(DietPlan.user_id == user.id)
        .order_by(DietPlan.created_at.desc())
        .all()
    )


@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan(plan_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(DietPlan).filter(
        DietPlan.id == plan_id,
        DietPlan.user_id == user.id,
    ).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.delete("/{plan_id}", status_code=204)
def delete_plan(plan_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(DietPlan).filter(
        DietPlan.id == plan_id,
        DietPlan.user_id == user.id,
    ).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(plan)
    db.commit()
