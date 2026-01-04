from pydantic import BaseModel


class AIFinancialSummary(BaseModel):
    BalanceSheets: list[float]
    CashFlowSheet: list[float]
    IncomeStatement: list[float]