"""
Core mean-variance portfolio optimization engine.

Methodology note (mirrors the original R/PortfolioAnalytics script this was
ported from): all portfolio-level math uses SIMPLE (arithmetic) returns,
because portfolio return is a weighted SUM of asset simple returns
(R_p = sum(w_i * R_i)) -- that identity only holds for simple returns, not
log returns. Log returns are reserved for time-series forecasting elsewhere.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize

TRADING_DAYS = 252


def clean_price_data(df: pd.DataFrame, date_col: str = "Date") -> pd.DataFrame:
    """Parse dates, coerce prices to numeric, forward-fill gaps, sort, dedupe.

    Tries ISO/default parsing first (unambiguous for YYYY-MM-DD), then falls
    back to day-first parsing only if that leaves most dates unparsed --
    mirrors the original R script's multi-format fallback, and avoids
    forcing dayfirst=True onto already-unambiguous ISO dates (which silently
    swaps day/month and corrupts the index).
    """
    df = df.copy()
    raw = df[date_col]
    parsed = pd.to_datetime(raw, errors="coerce")
    if parsed.isna().mean() > 0.5:
        parsed = pd.to_datetime(raw, errors="coerce", dayfirst=True)
    df[date_col] = parsed
    df = df.dropna(subset=[date_col]).drop_duplicates(subset=[date_col])
    df = df.sort_values(date_col).set_index(date_col)

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.ffill().fillna(0)
    return df


def compute_simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna(how="all")


def annualized_mean(returns: pd.DataFrame) -> pd.Series:
    return returns.mean() * TRADING_DAYS


def annualized_cov(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.cov() * TRADING_DAYS


def portfolio_return(weights: np.ndarray, mu: pd.Series) -> float:
    return float(np.dot(weights, mu))


def portfolio_vol(weights: np.ndarray, cov: pd.DataFrame) -> float:
    return float(np.sqrt(weights @ cov.values @ weights))


def _long_only_full_investment_constraints(n: int):
    bounds = tuple((0.0, 1.0) for _ in range(n))
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]
    return bounds, constraints


def min_variance_for_target(mu: pd.Series, cov: pd.DataFrame, target: float):
    """Minimum-variance long-only portfolio that hits an exact target annual return."""
    n = len(mu)
    bounds, constraints = _long_only_full_investment_constraints(n)
    constraints = constraints + [
        {"type": "eq", "fun": lambda w: np.dot(w, mu.values) - target}
    ]
    x0 = np.repeat(1.0 / n, n)
    res = minimize(
        lambda w: w @ cov.values @ w,
        x0, method="SLSQP", bounds=bounds, constraints=constraints,
        options={"maxiter": 500, "ftol": 1e-12},
    )
    if not res.success:
        return None
    w = np.clip(res.x, 0, None)
    w = w / w.sum()
    return pd.Series(w, index=mu.index)


def efficient_frontier(mu: pd.Series, cov: pd.DataFrame, n_points: int = 50) -> pd.DataFrame:
    """Sweep target returns from min to max asset return, solving min-variance at each."""
    targets = np.linspace(mu.min(), mu.max(), n_points)
    rows = []
    weight_rows = []
    for t in targets:
        w = min_variance_for_target(mu, cov, t)
        if w is not None:
            vol = portfolio_vol(w.values, cov)
            rows.append({"Return": t, "Volatility": vol})
            weight_rows.append(w)
    frontier = pd.DataFrame(rows)
    weights_df = pd.DataFrame(weight_rows).reset_index(drop=True)
    return frontier, weights_df


def max_sharpe_portfolio(mu: pd.Series, cov: pd.DataFrame, risk_free_rate: float):
    """Solve directly for the tangency (max-Sharpe) long-only portfolio."""
    n = len(mu)
    bounds, constraints = _long_only_full_investment_constraints(n)
    x0 = np.repeat(1.0 / n, n)

    def neg_sharpe(w):
        ret = np.dot(w, mu.values)
        vol = np.sqrt(w @ cov.values @ w)
        if vol == 0:
            return 1e6
        return -(ret - risk_free_rate) / vol

    res = minimize(neg_sharpe, x0, method="SLSQP", bounds=bounds,
                    constraints=constraints, options={"maxiter": 1000, "ftol": 1e-12})
    w = np.clip(res.x, 0, None)
    w = w / w.sum()
    weights = pd.Series(w, index=mu.index)
    ret = portfolio_return(w, mu)
    vol = portfolio_vol(w, cov)
    sharpe = (ret - risk_free_rate) / vol
    return weights, ret, vol, sharpe


def equal_weight_portfolio(asset_names):
    n = len(asset_names)
    return pd.Series(np.repeat(1.0 / n, n), index=asset_names)


def portfolio_beta_alpha(weights: pd.Series, asset_returns: pd.DataFrame,
                          market_returns: pd.Series, risk_free_rate: float):
    port_ret_series = asset_returns @ weights
    cov_pm = np.cov(port_ret_series, market_returns)[0, 1] * TRADING_DAYS
    market_var = market_returns.var() * TRADING_DAYS
    beta = cov_pm / market_var
    port_ann_return = port_ret_series.mean() * TRADING_DAYS
    market_ann_return = market_returns.mean() * TRADING_DAYS
    alpha = port_ann_return - (risk_free_rate + beta * (market_ann_return - risk_free_rate))
    return beta, alpha, port_ret_series
