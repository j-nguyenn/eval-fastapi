from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class EvaluationBase(BaseModel):
    id: int
    name: str
    instructions: Optional[str]

    criteria: list

    columnRoles: list = Field(alias="column_roles")
    data: list
    context: Optional[list] = Field(alias="context")

    totalItems: Optional[int] = Field(alias="total_items")
    randomizationEnabled: Optional[bool] = Field(alias="randomization_enabled")

    status: Optional[str]

    groupBy: Optional[str] = Field(alias="group_by")
class EvaluationCreate(EvaluationBase):
    pass

class EvaluationUpdate(BaseModel):
    name: Optional[str]
    instructions: Optional[str]
    criteria: Optional[list]
    columnRoles: Optional[list]
    data: Optional[list]
    context: Optional[list]
    status: Optional[str]

class EvaluationOut(EvaluationBase):
    id: int
    createdAt: datetime = Field(alias="created_at")
    completedAt: Optional[datetime] = Field(alias="completed_at")

    class Config:
        from_attributes = True
