from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class EvaluationCreate(BaseModel):
    name: str
    status: Optional[str] = "draft"
    payload: dict

class EvaluationUpdate(BaseModel):
    name: Optional[str]
    status: Optional[str]
    payload: Optional[dict]

class EvaluationOut(BaseModel):
    id: int
    name: str
    status: str
    payload: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
