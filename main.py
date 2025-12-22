import pandas as pd
import yfinance as yf
from fastapi import FastAPI
from pydantic import BaseModel

from models.company_info import Company

app = FastAPI()

@app.get("/stocks/{symbols}", response_model=Company)
async def stocktitleinfo(symbols: str):
    dat = yf.Ticker(symbols)

    df = dat.info

    dffive = dat.history(period="5y")

    five_year_row = dffive.iloc[0]
    five_year_price = five_year_row["Close"]
    five_year_date = five_year_row.name

    latest_row = dffive.iloc[-1]
    latest_price = latest_row["Close"]

    five_year_return = (latest_price / five_year_price - 1) * 100
    five_year_date_str = five_year_date.strftime("%Y-%m-%d")
    five_year_diff = latest_price - five_year_price;
    return Company(
        symbol = df.get("symbol"),
        displayName= df.get("displayName"),
        shortName=df.get("shortName"),
        regularMarketPrice=df.get("regularMarketPrice"),
        regularMarketChange=df.get("regularMarketChange"),
        regularMarketChangePercent=df.get("regularMarketChangePercent"),
        regularMarketPreviousClose=df.get("regularMarketPreviousClose"),
        fiveYrDate=five_year_date_str,
        fiveYrPercentage= five_year_return,
        fiveYrDiff=five_year_diff
    )