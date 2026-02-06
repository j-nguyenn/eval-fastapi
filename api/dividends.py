from datetime import date

import pandas as pd
import yfinance as yf
from fastapi import APIRouter, HTTPException, Query

from schemas.dividends import DividendHistoryResponse, DividendRecord

router = APIRouter(prefix="/dividends", tags=["Dividends"])


@router.get("/{ticker}", response_model=DividendHistoryResponse)
def get_dividend_history(
    ticker: str,
    start_date: date = Query(None, description="Start date (YYYY-MM-DD). Defaults to earliest available."),
    end_date: date = Query(None, description="End date (YYYY-MM-DD). Defaults to today."),
):
    """Return dividend history and currency for a given ticker between start and end dates."""
    try:
        stock = yf.Ticker(ticker)
        currency = stock.info.get("currency", "USD")
        dividends = stock.dividends

        if dividends.empty:
            return DividendHistoryResponse(ticker=ticker, currency=currency, dividends=[])

        df = dividends.reset_index()
        df.columns = ["Payment Date", "Dividend"]
        df["Payment Date"] = pd.to_datetime(df["Payment Date"]).dt.tz_localize(None)
        df["Dividend"] = pd.to_numeric(df["Dividend"], errors="coerce")

        # Apply date filters
        if start_date:
            df = df[df["Payment Date"] >= pd.Timestamp(start_date)]
        if end_date:
            df = df[df["Payment Date"] <= pd.Timestamp(end_date)]

        df = df.sort_values("Payment Date", ascending=False)

        records = [
            DividendRecord(
                payment_date=row["Payment Date"].strftime("%Y-%m-%d"),
                ticker=ticker,
                currency=currency,
                dividend=round(row["Dividend"], 6),
            )
            for _, row in df.iterrows()
        ]

        return DividendHistoryResponse(
            ticker=ticker,
            currency=currency,
            dividends=records,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dividend data for {ticker}: {e}")
