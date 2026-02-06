from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ResultBase(BaseModel):
    evaluationId: int = Field(alias="evaluation_id")
    evaluationName: Optional[str] = Field(alias="evaluation_name")

    itemId: Optional[str] = Field(alias="item_id")
    reviewerId: Optional[str] = Field(alias="reviewer_id")
    reviewerName: Optional[str] = Field(alias="reviewer_name")

    submittedAt: Optional[datetime] = Field(alias="submitted_at")
    timeSpent: Optional[int] = Field(alias="time_spent")

    responses: Dict[str, Any]
    originalData: Dict[str, Any] = Field(alias="original_data")

class ResultCreate(ResultBase):
    pass

class ResultUpdate(BaseModel):
    evaluationName: Optional[str]
    itemId: Optional[str]
    reviewerId: Optional[str]
    reviewerName: Optional[str]
    submittedAt: Optional[datetime]
    timeSpent: Optional[int]
    responses: Optional[Dict[str, Any]]
    originalData: Optional[Dict[str, Any]]

class ResultOut(ResultBase):
    id: int
    createdAt: datetime = Field(alias="created_at")

    class Config:
        from_attributes = True
