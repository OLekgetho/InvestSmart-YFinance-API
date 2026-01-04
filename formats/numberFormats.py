import pandas as pd


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format a float as a percentage string.

    Example:
        0.1234 -> "12.34%"
        5 -> "500%"
    """
    if value is None:
        return "N/A"

    return f"{value * 100:.{decimals}f}%"


def format_number_human(value: float) -> str:
    if value is None:
        return "N/A"
    abs_val = abs(value)
    if abs_val >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:,.2f}T"
    elif abs_val >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}B"
    elif abs_val >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"
    else:
        return f"${value:,.0f}"


def format_ratio(value: float, decimals: int = 2) -> str:
    """
    Format a numeric ratio or P/E to a string with fixed decimals.
    Returns 'N/A' if value is None, <= 0, or not finite.
    """
    if value is None or value <= 0 or not pd.notna(value) or value in [float('inf'), float('-inf')]:
        return "N/A"
    return f"{value:.{decimals}f}"


def safe_cagr(series):
    """
    Calculate CAGR (Compound Annual Growth Rate) for a pandas Series.
    Handles missing values (NaN), negative values, and avoids divide-by-zero.
    """
    # Remove missing values
    series_valid = series.dropna()

    # Need at least 2 valid data points
    if len(series_valid) < 2:
        return None

    # Oldest value cannot be zero
    start = series_valid.iloc[-1]
    end = series_valid.iloc[0]
    if start == 0:
        return None

    # CAGR formula
    return (abs(end) / abs(start)) ** (1 / (len(series_valid) - 1)) - 1