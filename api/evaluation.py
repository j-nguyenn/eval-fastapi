from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal
from models.evaluation import Evaluation
from schemas.evaluation import (
    EvaluationCreate,
    EvaluationUpdate,
    EvaluationOut
)

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EvaluationOut)
def create_evaluation(
    evaluation: EvaluationCreate,
    db: Session = Depends(get_db)
):
    obj = Evaluation(
        name=evaluation.name,
        status=evaluation.status,
        payload=evaluation.payload
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[EvaluationOut])
def list_evaluations(db: Session = Depends(get_db)):
    return db.query(Evaluation).all()

@router.get("/{evaluation_id}", response_model=EvaluationOut)
def get_evaluation(evaluation_id: int, db: Session = Depends(get_db)):
    obj = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return obj

@router.put("/{evaluation_id}", response_model=EvaluationOut)
def update_evaluation(
    evaluation_id: int,
    update: EvaluationUpdate,
    db: Session = Depends(get_db)
):
    obj = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    for field, value in update.dict(exclude_unset=True).items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{evaluation_id}")
def delete_evaluation(evaluation_id: int, db: Session = Depends(get_db)):
    obj = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    db.delete(obj)
    db.commit()
    return {"deleted": True, "id": evaluation_id}
