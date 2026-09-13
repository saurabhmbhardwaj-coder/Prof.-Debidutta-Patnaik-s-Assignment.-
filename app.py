"""
Portfolio Optimizer -- Streamlit app
Mean-variance (Markowitz) portfolio optimization with an interactive
efficient frontier, performance metrics, and a built-in glossary.

Run locally:    streamlit run app.py
Deploy:         push this repo to GitHub, then deploy on streamlit.io
                 (Community Cloud) pointing at app.py.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from optimization import (
    clean_price_data, compute_simple_returns, annualized_mean, annualized_cov,
    efficient_frontier, max_sharpe_portfolio, equal_weight_portfolio,
    portfolio_beta_alpha, portfolio_return, portfolio_vol,
)
from metrics import compute_metrics, drawdown_series, cumulative_returns
from glossary import GLOSSARY

st.set_page_config(page_title="Portfolio Optimizer", page_icon="📈", layout="wide")

# ------------------------------------------------------------------ #
# Sidebar -- data input & settings
# ------------------------------------------------------------------ #
st.sidebar.title("📈 Portfolio Optimizer")
st.sidebar.markdown("Mean-variance optimization, powered by your own price data.")

uploaded = st.sidebar.file_uploader(
    "Upload a CSV of daily prices (Date + one column per asset)", type=["csv"]
)
use_sample = st.sidebar.checkbox("Use bundled sample data (Sensex + 13 stocks)",
                                  value=uploaded is None)

if uploaded is not None and not use_sample:
    raw_df = pd.read_csv(uploaded)
else:
    raw_df = pd.read_csv("sample_data.csv")

date_col = st.sidebar.selectbox(
    "Date column", options=list(raw_df.columns),
    index=list(raw_df.columns).index("Date") if "Date" in raw_df.columns else 0,
)

prices = clean_price_data(raw_df, date_col=date_col)
all_cols = list(prices.columns)

market_col = st.sidebar.selectbox(
    "Market / benchmark column", options=all_cols,
    index=all_cols.index("Sensex") if "Sensex" in all_cols else 0,
    help="Used for Beta/Alpha and as the comparison benchmark.",
)

risk_free_rate = st.sidebar.number_input(
    "Risk-free rate (annual, decimal)", min_value=0.0, max_value=0.5,
    value=0.0696, step=0.001, format="%.4f",
)

n_frontier_points = st.sidebar.slider("Efficient frontier resolution (# portfolios)", 10, 100, 50)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Long-only, fully-invested constraints throughout: weights are between 0% "
    "and 100% and always sum to 100% (no shorting, no leverage)."
)

# ------------------------------------------------------------------ #
# Core calculations (shared across tabs)
# ------------------------------------------------------------------ #
returns = compute_simple_returns(prices)
market_returns = returns[market_col]
asset_returns = returns.drop(columns=[market_col])
asset_names = list(asset_returns.columns)

mu = annualized_mean(asset_returns)
cov = annualized_cov(asset_returns)

opt_weights, opt_return, opt_vol, opt_sharpe = max_sharpe_portfolio(mu, cov, risk_free_rate)
opt_beta, opt_alpha, opt_port_returns = portfolio_beta_alpha(
    opt_weights, asset_returns, market_returns, risk_free_rate
)

eq_weights = equal_weight_portfolio(asset_names)
eq_return = portfolio_return(eq_weights.values, mu)
eq_vol = portfolio_vol(eq_weights.values, cov)
eq_sharpe = (eq_return - risk_free_rate) / eq_vol if eq_vol else np.nan
eq_beta, eq_alpha, eq_port_returns = portfolio_beta_alpha(
    eq_weights, asset_returns, market_returns, risk_free_rate
)

frontier_df, frontier_weights = efficient_frontier(mu, cov, n_frontier_points)

# ------------------------------------------------------------------ #
# Tabs
# ------------------------------------------------------------------ #
tab_frontier, tab_optimal, tab_perf, tab_learn = st.tabs(
    ["🧭 Efficient Frontier", "⭐ Optimal Portfolio", "📊 Performance", "📘 Learn"]
)

# ---------------- Efficient Frontier tab ---------------- #
with tab_frontier:
    st.header("Efficient Frontier")
    st.markdown(
        f"Built from **{len(asset_names)} assets** and **{len(returns):,} trading days** "
        f"of returns ({returns.index.min().date()} to {returns.index.max().date()})."
    )

    asset_vol = pd.Series(np.sqrt(np.diag(cov.values)), index=asset_names)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=frontier_df["Volatility"], y=frontier_df["Return"],
        mode="lines+markers", name="Efficient Frontier",
        line=dict(color="#1f77b4"), marker=dict(size=5),
    ))
    fig.add_trace(go.Scatter(
        x=[opt_vol], y=[opt_return], mode="markers", name="Max-Sharpe Optimal",
        marker=dict(color="red", size=16, symbol="star"),
    ))
    fig.add_trace(go.Scatter(
        x=[eq_vol], y=[eq_return], mode="markers", name="Equal-Weight",
        marker=dict(color="orange", size=12, symbol="diamond"),
    ))
    fig.add_trace(go.Scatter(
        x=asset_vol, y=mu, mode="markers+text", name="Individual Assets",
        marker=dict(color="green", size=9, symbol="triangle-up"),
        text=asset_names, textposition="top center", textfont=dict(size=9),
    ))
    fig.update_layout(
        xaxis_title="Annualized Volatility", yaxis_title="Annualized Return",
        height=600, legend=dict(orientation="h", y=-0.15),
        xaxis_tickformat=".0%", yaxis_tickformat=".0%",
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Per-asset return & volatility table"):
        st.dataframe(
            pd.DataFrame({"Annualized Return": mu, "Annualized Volatility": asset_vol})
            .style.format("{:.2%}"),
            use_container_width=True,
        )

    with st.expander("Full frontier weight vectors (download-ready)"):
        show_df = pd.concat([frontier_df.reset_index(drop=True), frontier_weights], axis=1)
        st.dataframe(show_df.style.format({c: "{:.2%}" for c in show_df.columns}),
                     use_container_width=True)
        st.download_button(
            "Download frontier as CSV", show_df.to_csv(index=False),
            file_name="efficient_frontier_weights.csv", mime="text/csv",
        )

# ---------------- Optimal Portfolio tab ---------------- #
with tab_optimal:
    st.header("Max-Sharpe Optimal Portfolio")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Weights")
        w_show = opt_weights[opt_weights > 1e-4].sort_values(ascending=False)
        fig_pie = go.Figure(data=[go.Pie(labels=w_show.index, values=w_show.values, hole=0.4)])
        fig_pie.update_layout(height=420, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Headline numbers")
        m1, m2, m3 = st.columns(3)
        m1.metric("Expected Return", f"{opt_return:.2%}")
        m2.metric("Volatility", f"{opt_vol:.2%}")
        m3.metric("Sharpe Ratio", f"{opt_sharpe:.2f}")
        m4, m5 = st.columns(2)
        m4.metric("Beta vs " + market_col, f"{opt_beta:.2f}")
        m5.metric("Alpha", f"{opt_alpha:.2%}")

        st.markdown("**vs. Equal-Weight benchmark**")
        comp = pd.DataFrame({
            "Optimal": [opt_return, opt_vol, opt_sharpe],
            "Equal-Weight": [eq_return, eq_vol, eq_sharpe],
        }, index=["Return", "Volatility", "Sharpe"])
        st.dataframe(comp.style.format("{:.3f}"), use_container_width=True)

    st.subheader("Full weight table")
    st.dataframe(
        w_show.rename("Weight").to_frame().style.format("{:.2%}"),
        use_container_width=True,
    )

# ---------------- Performance tab ---------------- #
with tab_perf:
    st.header("Performance & Risk Metrics")
    st.caption("Naive (freely-rebalanced) daily weighted-return simulation -- no transaction costs.")

    opt_metrics = compute_metrics(opt_port_returns, risk_free_rate, market_returns)
    eq_metrics = compute_metrics(eq_port_returns, risk_free_rate, market_returns)

    metrics_df = pd.DataFrame({"Optimal": opt_metrics, "Equal-Weight": eq_metrics})
    st.dataframe(metrics_df.style.format("{:.4f}"), use_container_width=True)

    st.subheader("Cumulative Return")
    cum_opt = cumulative_returns(opt_port_returns)
    cum_eq = cumulative_returns(eq_port_returns)
    cum_mkt = cumulative_returns(market_returns)
    fig_cum = go.Figure()
    fig_cum.add_trace(go.Scatter(x=cum_opt.index, y=cum_opt, name="Optimal"))
    fig_cum.add_trace(go.Scatter(x=cum_eq.index, y=cum_eq, name="Equal-Weight"))
    fig_cum.add_trace(go.Scatter(x=cum_mkt.index, y=cum_mkt, name=market_col))
    fig_cum.update_layout(height=420, yaxis_tickformat=".0%", legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig_cum, use_container_width=True)

    st.subheader("Drawdown")
    dd_opt = drawdown_series(opt_port_returns)
    fig_dd = go.Figure()
    fig_dd.add_trace(go.Scatter(x=dd_opt.index, y=dd_opt, fill="tozeroy",
                                 line=dict(color="crimson"), name="Optimal Drawdown"))
    fig_dd.update_layout(height=320, yaxis_tickformat=".0%")
    st.plotly_chart(fig_dd, use_container_width=True)

# ---------------- Learn tab ---------------- #
with tab_learn:
    st.header("📘 Learn: Concepts & Terminology")
    st.markdown(
        "Every metric and chart in this app is explained here in plain English. "
        "Click a term to expand it."
    )
    search = st.text_input("Search terms", "")
    for entry in GLOSSARY:
        if search and search.lower() not in entry["term"].lower() and search.lower() not in entry["long"].lower():
            continue
        with st.expander(f"**{entry['term']}** — {entry['short']}"):
            st.write(entry["long"])
