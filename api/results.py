from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal
from models.results import Result
from schemas.results import (
    ResultCreate,
    ResultUpdate,
    ResultOut
)

router = APIRouter(prefix="/results", tags=["Results"]) 


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ResultOut)
def create_result(result: ResultCreate, db: Session = Depends(get_db)):
    obj = Result(
        evaluation_id=result.evaluationId,
        evaluation_name=result.evaluationName,
        item_id=result.itemId,
        reviewer_id=result.reviewerId,
        reviewer_name=result.reviewerName,
        submitted_at=result.submittedAt,
        time_spent=result.timeSpent,
        responses=result.responses,
        original_data=result.originalData,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[ResultOut])
def list_results(db: Session = Depends(get_db)):
    return db.query(Result).all()


@router.get("/{result_id}", response_model=ResultOut)
def get_result(result_id: int, db: Session = Depends(get_db)):
    obj = db.query(Result).filter(Result.id == result_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Result not found")
    return obj


@router.put("/{result_id}", response_model=ResultOut)
def update_result(result_id: int, update: ResultUpdate, db: Session = Depends(get_db)):
    obj = db.query(Result).filter(Result.id == result_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Result not found")

    # Map camelCase input fields to SQLAlchemy column attributes
    field_map = {
        "evaluationName": "evaluation_name",
        "itemId": "item_id",
        "reviewerId": "reviewer_id",
        "reviewerName": "reviewer_name",
        "submittedAt": "submitted_at",
        "timeSpent": "time_spent",
        "responses": "responses",
        "originalData": "original_data",
    }

    for field, value in update.dict(exclude_unset=True).items():
        setattr(obj, field_map.get(field, field), value)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{result_id}")
def delete_result(result_id: int, db: Session = Depends(get_db)):
    obj = db.query(Result).filter(Result.id == result_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Result not found")

    db.delete(obj)
    db.commit()
    return {"deleted": True, "id": result_id}
