"""Performance & risk metrics for a portfolio return series."""

import numpy as np
import pandas as pd

TRADING_DAYS = 252


def compute_metrics(port_returns: pd.Series, risk_free_rate: float,
                     market_returns: pd.Series | None = None) -> dict:
    r = port_returns.dropna()
    ann_return = r.mean() * TRADING_DAYS
    ann_vol = r.std() * np.sqrt(TRADING_DAYS)

    win_ratio = (r > 0).mean()
    skew = r.skew()
    kurt = r.kurt()

    var_5 = r.quantile(0.05)
    cvar_5 = r[r <= var_5].mean()

    sharpe = (ann_return - risk_free_rate) / ann_vol if ann_vol else np.nan

    daily_rf = risk_free_rate / TRADING_DAYS
    downside = r[r < daily_rf] - daily_rf
    downside_dev = np.sqrt((downside ** 2).mean()) * np.sqrt(TRADING_DAYS) if len(downside) else np.nan
    sortino = (ann_return - risk_free_rate) / downside_dev if downside_dev else np.nan

    cum = (1 + r).cumprod()
    running_max = cum.cummax()
    drawdown = (cum - running_max) / running_max
    max_dd = drawdown.min()
    calmar = ann_return / abs(max_dd) if max_dd != 0 else np.nan

    metrics = {
        "Annualized Return": ann_return,
        "Annualized Volatility": ann_vol,
        "Sharpe Ratio": sharpe,
        "Sortino Ratio": sortino,
        "Winning Day Ratio": win_ratio,
        "Skewness": skew,
        "Kurtosis": kurt,
        "VaR (5%, daily)": var_5,
        "CVaR (5%, daily)": cvar_5,
        "Max Drawdown": max_dd,
        "Calmar Ratio": calmar,
    }

    if market_returns is not None:
        common = r.index.intersection(market_returns.index)
        rc = r.loc[common]
        mc = market_returns.loc[common]
        cov_pm = np.cov(rc, mc)[0, 1] * TRADING_DAYS
        mkt_var = mc.var() * TRADING_DAYS
        beta = cov_pm / mkt_var if mkt_var else np.nan
        mkt_ann_return = mc.mean() * TRADING_DAYS
        alpha = ann_return - (risk_free_rate + beta * (mkt_ann_return - risk_free_rate))
        tracking_error = (rc - mc).std() * np.sqrt(TRADING_DAYS)
        info_ratio = (ann_return - mkt_ann_return) / tracking_error if tracking_error else np.nan
        metrics.update({
            "Beta": beta,
            "Alpha": alpha,
            "Tracking Error": tracking_error,
            "Information Ratio": info_ratio,
        })

    return metrics


def drawdown_series(port_returns: pd.Series) -> pd.Series:
    r = port_returns.dropna()
    cum = (1 + r).cumprod()
    running_max = cum.cummax()
    return (cum - running_max) / running_max


def cumulative_returns(port_returns: pd.Series) -> pd.Series:
    return (1 + port_returns.dropna()).cumprod() - 1
