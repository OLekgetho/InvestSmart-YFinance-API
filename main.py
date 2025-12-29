from typing import List

import pandas as pd
import yfinance as yf
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from models.company_info import Company
from models.company_news import CompanyNews
from models.news import News
from models.stockProfile import StockProfile

app = FastAPI()

# Show all rows and columns
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# Remove scientific notation
pd.options.display.float_format = "{:,.0f}".format

# Income Statement
@app.get("/stocks/profile/incomestatment/{symbol}")
async def get_incomestatement(symbol: str):
    dat = yf.Ticker(symbol)
    df = dat.income_stmt
    annual = df / 1_000
    annual = annual.fillna("---")
    return annual


# Balance Sheet
@app.get("/stocks/profile/cashflowstatment/{symbol}")
async def get_cashflowstatement(symbol: str):
    dat = yf.Ticker(symbol)
    df = dat.cash_flow
    annual = df / 1_000
    annual = annual.fillna("---")
    return annual

# Balance Sheet
@app.get("/stocks/profile/balancesheet/{symbol}")
async def get_balancesheet(symbol: str):
    dat = yf.Ticker(symbol)
    df = dat.balance_sheet
    annual = df / 1_000
    annual = annual.fillna("---")
    return annual

#StockProfile
@app.get("/stocks/profile/{symbol}", response_model=StockProfile)
async def get_profile(symbol: str):
    symbol = yf.Ticker(symbol)
    profile = symbol.infoz
    return StockProfile(**profile)

# Charts RestAPI
@app.get("/stocks/chart/{symbol}/{period}")
async def get_chart(symbol: str, period: str = "1mo"):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    hist.reset_index(inplace=True)

    data = [
        {"date": row["Date"],
         "open": float(row["Open"]),
         "close": float(row["Close"]),
         "low": float(row["Low"]),
         "high": float(row["High"]),
         }
        for i, row in hist.iterrows()
    ]
    return {"data": data}


# StockPrice Title
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

    oneonthdffive = dat.history(period="1mo")

    one_Month_year = oneonthdffive.iloc[0]
    one_Month_year_price = one_Month_year["Close"]
    one_Month_year_date = one_Month_year.name

    one_month_return = (latest_price / one_Month_year_price - 1) * 100
    one_month_diff = latest_price - one_Month_year_price;
    one_month_date_str = one_Month_year_date.strftime("%Y-%m-%d")

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
        fiveYrDiff=five_year_diff,
        oneMonthDate=one_month_date_str,
        oneMonthDiff=one_month_diff,
        oneMonthPercentage=one_month_return,
        oneMonthPrice=one_Month_year_price
    )

# News
@app.get("/stock/articles/{symbol}")
async def get_articles(symbol: str):
    dat = yf.Ticker(symbol)
    news_headlines = dat.news

    top_articles = news_headlines[:5]

    news_items = []
    for article in top_articles:
        news_items.append(article)


    return news_items
