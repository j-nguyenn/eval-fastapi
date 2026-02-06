from pydantic import BaseModel
from typing import Optional
from datetime import date


class DividendRecord(BaseModel):
    payment_date: str
    ticker: str
    currency: str
    dividend: float


class DividendHistoryResponse(BaseModel):
    ticker: str
    currency: str
    dividends: list[DividendRecord]
