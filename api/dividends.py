from datetime import date

import pandas as pd
import yfinance as yf
from fastapi import APIRouter, HTTPException, Query

from schemas.dividends import (
    BulkDividendHistoryResponse,
    BulkDividendRequest,
    DividendHistoryResponse,
    DividendRecord,
)

router = APIRouter(prefix="/dividends", tags=["Dividends"])


@router.post("/bulk", response_model=BulkDividendHistoryResponse)
def get_bulk_dividend_history(request: BulkDividendRequest):
    """Return dividend history for a list of tickers."""
    results: list[DividendHistoryResponse] = []
    errors: list[dict] = []

    for ticker in request.tickers:
        try:
            stock = yf.Ticker(ticker)
            currency = stock.info.get("currency", "USD")
            dividends = stock.dividends

            if dividends.empty:
                results.append(DividendHistoryResponse(ticker=ticker, currency=currency, dividends=[]))
                continue

            df = dividends.reset_index()
            df.columns = ["Payment Date", "Dividend"]
            df["Payment Date"] = pd.to_datetime(df["Payment Date"]).dt.tz_localize(None)
            df["Dividend"] = pd.to_numeric(df["Dividend"], errors="coerce")

            if request.start_date:
                df = df[df["Payment Date"] >= pd.Timestamp(request.start_date)]
            if request.end_date:
                df = df[df["Payment Date"] <= pd.Timestamp(request.end_date)]

            df = df.sort_values("Payment Date", ascending=False)

            # Fetch historical closing prices to match each dividend date
            hist_start = df["Payment Date"].min()
            hist_end = df["Payment Date"].max() + pd.Timedelta(days=1)
            history = stock.history(start=hist_start, end=hist_end)
            if not history.empty:
                history.index = pd.to_datetime(history.index).tz_localize(None)

            records = []
            for _, row in df.iterrows():
                pay_date = row["Payment Date"]
                dividend = round(row["Dividend"], 6)
                price = None
                div_yield = None

                if not history.empty:
                    mask = history.index <= pay_date
                    if mask.any():
                        price = round(float(history.loc[mask, "Close"].iloc[-1]), 4)
                        if price > 0:
                            div_yield = round((dividend / price) * 100, 4)

                records.append(
                    DividendRecord(
                        payment_date=pay_date.strftime("%Y-%m-%d"),
                        ticker=ticker,
                        currency=currency,
                        dividend=dividend,
                        price_per_share=price,
                        dividend_yield=div_yield,
                    )
                )

            results.append(DividendHistoryResponse(ticker=ticker, currency=currency, dividends=records))

        except Exception as e:
            errors.append({"ticker": ticker, "detail": str(e)})

    return BulkDividendHistoryResponse(results=results, errors=errors)


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

        # Fetch historical closing prices to match each dividend date
        hist_start = df["Payment Date"].min()
        hist_end = df["Payment Date"].max() + pd.Timedelta(days=1)
        history = stock.history(start=hist_start, end=hist_end)
        if not history.empty:
            history.index = pd.to_datetime(history.index).tz_localize(None)

        records = []
        for _, row in df.iterrows():
            pay_date = row["Payment Date"]
            dividend = round(row["Dividend"], 6)
            price = None
            div_yield = None

            if not history.empty:
                # Find the closest trading day on or before the payment date
                mask = history.index <= pay_date
                if mask.any():
                    price = round(float(history.loc[mask, "Close"].iloc[-1]), 4)
                    if price > 0:
                        div_yield = round((dividend / price) * 100, 4)

            records.append(
                DividendRecord(
                    payment_date=pay_date.strftime("%Y-%m-%d"),
                    ticker=ticker,
                    currency=currency,
                    dividend=dividend,
                    price_per_share=price,
                    dividend_yield=div_yield,
                )
            )

        return DividendHistoryResponse(
            ticker=ticker,
            currency=currency,
            dividends=records,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dividend data for {ticker}: {e}")
