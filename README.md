# InvestSmart – YFinance Python Backend

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)](https://fastapi.tiangolo.com/)
[![yfinance](https://img.shields.io/badge/yfinance-Latest-green)](https://pypi.org/project/yfinance/)
![Code](https://custom-icon-badges.demolab.com/github/languages/code-size/OLEKGETHO/InvestSmart-YFinance-API?logo=file-code&logoColor=white)

## 🎥 App Demo

<p align="center">
  <img src="https://raw.githubusercontent.com/OLekgetho/InvestSmart-YFinance-API/Prod/InvestSmart%20Demo.gif" width="250" style="margin: 0 10px; border-radius: 15px;" />
  <img src="https://raw.githubusercontent.com/OLekgetho/InvestSmart-YFinance-API/Prod/InvestSmart%20Demo%20part%202.gif" width="250" style="margin: 0 10px; border-radius: 15px;" />
</p>

## Overview

The InvestSmart YFinance API is a dedicated Python-based microservice responsible for retrieving, processing, and exposing financial market data using the yfinance library.

This service acts as the financial data provider within the InvestSmart system and is intentionally separated from the main application backend to ensure scalability, maintainability, and clean system design.

### Core idea:
*Financial data retrieval is isolated from business logic.*


## Purpose of This Backend

The Python backend exists to:

* Retrieve real-time and historical market data from Yahoo Finance
* Normalize and format raw financial data into clean JSON responses
* Abstract third-party data providers away from the main system
* Provide a stable REST API consumed by the Spring Boot backend

*This service does not manage users, authentication, or persistence. Its responsibility is strictly data acquisition and transformation.*

### System Architecture

*The InvestSmart application follows a multi-backend architecture:*

```sh
┌─────────────────────┐
│  React Native App   │
│  (Expo Go)          │
└─────────▲───────────┘
          │ 
          │
┌─────────┴───────────┐
│  Spring Boot API    │
│  (Main Backend)     │
│                     │
│ - Business Logic    │
│ - Users             │
│ - Portfolios        │
│ - Validation        │
└─────────▲───────────┘
          │ REST API
          │
┌─────────┴───────────┐
│ Python YFinance API │
│ (This Service)      │
│                     │
│ - Market Data       │
│ - Historical Prices │
│ - Data Formatting   │
└─────────▲───────────┘
          │
          │ yfinance
          │
┌─────────┴───────────┐
│ Yahoo Finance       │
│ (External Provider) │
└─────────────────────┘

```

## Project Structure

```sh
InvestSmart-YFinance-API/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container definition
├── .dockerignore
├── models/                 # Pydantic models for request/response validation
├── formats/                # Data formatting & transformation helpers
├── .github/workflows/      # CI/CD pipelines (GitHub Actions)
└── .idea/                  # PyCharm config (gitignore recommended)
```

## Quick Start
### Prerequisites

* Python 3.9+
* pip
* (optional) Docker

### Local Development

```sh
# 1. Clone the repository
git clone https://github.com/OLekgetho/InvestSmart-YFinance-API.git
cd InvestSmart-YFinance-API

# 2. Create & activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the API (development mode with auto-reload)
uvicorn main:app --reload --port 8000
```

### Docker (Recommended for Production/Testing)

```sh
# Build
docker build -t investsmart-yfinance-api .

# Run (maps port 8000)
docker run -d -p 8000:8000 --name yfinance-api investsmart-yfinance-api
```

## Feedback & Contributions

Contributions, suggestions, and improvements are welcome.
If you’d like to extend this service, optimize performance, or integrate additional data sources, feel free to open an issue or submit a pull request.


#### *Made with ❤️ © 2025–2026 Ofentse Lekgetho*
