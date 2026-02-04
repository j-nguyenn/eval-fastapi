from sqlalchemy import Boolean, Column, Integer, String, DateTime, JSON
from datetime import datetime
from db import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    instructions = Column(String)

    criteria = Column(JSON, nullable=False)
    column_roles = Column("columnRoles", JSON, nullable=False)
    data = Column(JSON, nullable=False)
    context = Column(JSON)

    total_items = Column("totalItems", Integer)
    randomization_enabled = Column("randomizationEnabled", Boolean)

    status = Column(String, index=True)
    group_by = Column("groupBy", String)

    created_at = Column(
        "createdAt",
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    completed_at = Column(
        "completedAt",
        DateTime,
        nullable=True
    )
