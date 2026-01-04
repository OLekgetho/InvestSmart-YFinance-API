from typing import List

import pandas as pd
import yfinance as yf
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from formats.numberFormats import format_number_human, format_percentage, format_ratio, safe_cagr
from models.company_info import Company
from models.company_news import CompanyNews
from models.news import News
from models.personal_kpi import PersonalKpi
from models.stockProfile import StockProfile

app = FastAPI()

# Show all rows and columns
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# Remove scientific notation
pd.options.display.float_format = "{:,.0f}".format

# Financial AI Summary
@app.get("/stocks/profile/financials")
async def get_financials_for_summary(symbol: str):
    dat = yf.Ticker(symbol)
    income_stat = dat.income_stmt
    cashflow_stat = dat.cash_flow
    balance_sheet = dat.balance_sheet

    revenue = income_stat.loc["Total Revenue"].iloc[0:2]
    gross_profit = income_stat.loc["Gross Profit"].iloc[0:2]
    operating_income = income_stat.loc["Operating Income"].iloc[0:2]
    net_icome = income_stat.loc["Net Income"].iloc[0:2]
    basic_eps = income_stat.loc["Basic EPS"].iloc[0:2]

    total_assets = balance_sheet.loc["Total Assets"].iloc[0:2]
    total_liabilities = balance_sheet.loc["Total Liabilities Net Minority Interest"].iloc[0:2]
    total_equity = balance_sheet.loc["Total Equity Gross Minority Interest"].iloc[0:2]
    cash_and_cash_equavalent = balance_sheet.loc["Cash And Cash Equivalents"].iloc[0:2]
    current_assets = balance_sheet.loc["Current Assets"].iloc[0:2]
    current_liabilities = balance_sheet.loc["Current Liabilities"].iloc[0:2]
    working_capital = balance_sheet.loc["Working Capital"].iloc[0:2]
    total_debt = balance_sheet.loc["Total Debt"].iloc[0:2]

    net_income_from_continuing_operations = cashflow_stat.loc["Net Income From Continuing Operations"].iloc[0:2]
    investing_cash_flow = cashflow_stat.loc["Investing Cash Flow"].iloc[0:2]
    financing_cash_flow = cashflow_stat.loc["Financing Cash Flow"].iloc[0:2]
    free_cash_flow = cashflow_stat.loc["Free Cash Flow"].iloc[0:2]
    changes_in_cash = cashflow_stat.loc["Changes In Cash "].iloc[0:2]


# Personal Metrics
@app.get("/stocks/personal/metrics/{symbol}", response_model=PersonalKpi)
async def get_personalmetrics(symbol: str):
    dat = yf.Ticker(symbol)
    info = dat.info

    # Current TTM data
    incomestat_ttm = dat.ttm_income_stmt
    cashflow_ttm = dat.ttm_cash_flow
    balancesheet_ttm = dat.balance_sheet.iloc[0]
    revenue = incomestat_ttm.loc["Total Revenue"].iloc[0]
    net_income_current = incomestat_ttm.loc["Net Income"].iloc[0]
    gross_profit = incomestat_ttm.loc["Gross Profit"].iloc[0]
    marketcap = info.get("marketCap")
    freecashflow = cashflow_ttm.loc["Free Cash Flow"].iloc[0]



    # Historical annual data
    incomestat_annual = dat.financials
    cashflow_annual = dat.cash_flow


    # Only keep specific years
    years_to_include = [2024, 2023, 2022, 2021]
    existing_years = [col for col in incomestat_annual.columns if col.year in years_to_include]
    existing_years_cashflow = [col for col in cashflow_annual.columns if col.year in years_to_include]

    # Net income for the selected years
    net_income_selected = incomestat_annual.loc[
        "Net Income", existing_years] if "Net Income" in incomestat_annual.index else pd.Series(dtype=float)

    # Revenue for the selcted years
    revenue_selected = incomestat_annual.loc[
        "Total Revenue", existing_years] if "Total Revenue" in incomestat_annual.index else pd.Series(dtype=float)

    # Free Cashflow for the selected years
    freecashflow_selected = cashflow_annual.loc[
        "Free Cash Flow", existing_years_cashflow] if "Free Cash Flow" in cashflow_annual.index else pd.Series(dtype=float)


    # Average of 4-year net income
    avg_net_income = net_income_selected.mean() if not net_income_selected.empty else net_income_current

    # Average of 4-year revenue
    avg_revenue = revenue_selected.mean() if not revenue_selected.empty else revenue

    # Average of 4-year free cash flow
    avg_freecashflow = freecashflow_selected.mean() if not freecashflow_selected.empty else freecashflow

    #P/E (TTM)
    traillingpe = marketcap/net_income_current

    # Price to Sale
    psratio = marketcap/revenue

    # Profit Margin
    profitM = net_income_current/revenue

    # 4-year Average Profit Margin
    avg_ProfitM = avg_net_income/avg_revenue

    # Gross Profit Margin
    gross_profit_margin = gross_profit/revenue

    # Price to Free Cash Flow TTM
    pe_free_cash_flow = marketcap / freecashflow

    # Enterprise Value
    ev = info.get("enterpriseValue")

    # Cash Flow Conversion
    fcf_to_net_income = freecashflow / net_income_current if net_income_current else None

    # Net Debt
    total_debt = info.get("totalDebt")
    cash = info.get("totalCash")
    net_debt = total_debt - cash if total_debt and cash else None

    revenue_cagr = safe_cagr(revenue_selected)
    net_income_cagr = safe_cagr(net_income_selected)
    fcf_cagr = safe_cagr(freecashflow_selected)
    return PersonalKpi(
        marketCap= format_number_human(marketcap),
        revenue= format_number_human(revenue),
        netIncome= format_number_human(net_income_current),
        fouryearNetIncomeAvg= format_number_human(avg_net_income),
        trailingpe= format_ratio(traillingpe),
        pricetosaleratio= format_ratio(psratio),
        profitMarginTTM= format_percentage(profitM),
        fouryearProfitMargin= format_percentage(avg_ProfitM),
        grossProfitMargin= format_percentage(gross_profit_margin),
        freeCashFlowTTM= format_number_human(freecashflow),
        fouryearFreeCashFlow=format_number_human(avg_freecashflow),
        pEFreeCashFlow=format_ratio(pe_free_cash_flow,2),
        enterpriseValue=format_number_human(ev),
        fcf_to_net_income=format_percentage(fcf_to_net_income),
        netDebt=format_number_human(net_debt),
        revenue_cagr=format_percentage(revenue_cagr),
        net_income_cagr=format_percentage(net_income_cagr),
        fcf_cagr=format_percentage(fcf_cagr),
    )


# Analyst Price Targets
@app.get("/stocks/profile/analyst/{symbol}")
async def get_analystpricetargets(symbol: str):
    dat = yf.Ticker(symbol)
    df = dat.analyst_price_targets
    return df


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
    profile = symbol.info
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

    top_articles = news_headlines[:8]

    news_items = []
    for article in top_articles:
        news_items.append(article)


    return news_items

