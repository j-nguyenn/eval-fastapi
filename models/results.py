from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from datetime import datetime
from db import Base

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)

    # Link back to an Evaluation
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"), index=True, nullable=False)
    evaluation_name = Column(String, index=True)

    # Per-item result fields
    item_id = Column(String, index=True)
    reviewer_id = Column(String, index=True)
    reviewer_name = Column(String, index=True)

    submitted_at = Column(DateTime, nullable=True)
    time_spent = Column(Integer, nullable=True)

    responses = Column(JSON, nullable=False)
    original_data = Column(JSON, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
