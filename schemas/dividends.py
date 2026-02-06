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


class BulkDividendRequest(BaseModel):
    tickers: list[str]
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class BulkDividendHistoryResponse(BaseModel):
    results: list[DividendHistoryResponse]
    errors: list[dict]
