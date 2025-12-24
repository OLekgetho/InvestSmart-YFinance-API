from typing import List

import pandas as pd
import yfinance as yf
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from models.company_info import Company
from models.company_news import CompanyNews
from models.news import News

app = FastAPI()


# Charts RestAPI
@app.get("/stocks/chart/{symbol}/{period}")
async def get_chart(symbol: str, period: str = "1mo"):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    hist.reset_index(inplace=True)

    data = [
        {"x": i, "open": float(row["Open"]), "close": float(row["Close"])}
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

# News
@app.get("/stock/articles/{symbol}")
async def get_articles(symbol: str):
    dat = yf.Ticker(symbol)
    news_headlines = dat.news

    top_articles = news_headlines[:2]

    news_items = []
    for article in top_articles:
        news_items.append(article)


    return news_items
