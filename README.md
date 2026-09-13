# Portfolio Optimizer

An interactive Streamlit app for mean-variance (Markowitz) portfolio
optimization: upload daily price data, see the efficient frontier, find the
max-Sharpe "optimal" portfolio, compare it to an equal-weight benchmark, and
explore ~15 performance/risk metrics — with a built-in **Learn** tab that
explains every term in plain English.

Ported from an R (`PortfolioAnalytics`/`PerformanceAnalytics`) teaching
script; the optimization math is solved directly with `scipy.optimize`
(SLSQP, long-only + fully-invested constraints) so it has no R dependency.

## Features

- 📤 Upload your own CSV of daily prices (Date column + one column per
  asset/index), or use the bundled sample (Sensex + 13 Indian large-caps,
  Jul 2021–Jun 2026)
- 🧭 Interactive efficient frontier (Plotly) with individual assets plotted
  alongside it
- ⭐ Max-Sharpe optimal portfolio: weights, pie chart, Beta/Alpha vs your
  chosen benchmark
- 📊 Performance tab: Sharpe, Sortino, Calmar, VaR, CVaR, max drawdown,
  cumulative return and drawdown charts, Optimal vs Equal-Weight
- 📘 Learn tab: searchable glossary covering every concept used in the app
  (efficient frontier, Sharpe ratio, CAPM alpha/beta, VaR/CVaR, rebalancing,
  and more)

## Run locally

```bash
git clone <this-repo-url>
cd <repo-folder>
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Deploy on Streamlit Community Cloud (free)

1. Push this folder to a **public GitHub repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with
   GitHub.
3. Click **New app**, pick your repo/branch, and set the main file path to
   `app.py`.
4. Click **Deploy**. It will install `requirements.txt` automatically.

## Data format

CSV with a date column and one price column per asset:

```
Date,Sensex,Stock A,Stock B,...
2021-07-01,52318.60,2948.69,495.36,...
2021-07-02,52484.67,2935.06,497.26,...
```

- Any parseable date format works.
- Pick which column is the "market/benchmark" column in the sidebar (used
  for Beta/Alpha) — it's excluded from the optimizable asset universe.
- Missing prices are forward-filled.

## Project structure

```
app.py                   # Streamlit UI (4 tabs: Frontier, Optimal, Performance, Learn)
utils/optimization.py    # Data cleaning, returns, efficient frontier, max-Sharpe solver
utils/metrics.py         # Performance/risk metrics (Sharpe, Sortino, VaR, CVaR, drawdown...)
utils/glossary.py        # Learn-tab content
data/sample_data.csv     # Bundled example dataset
requirements.txt
```

## Methodology notes

- All portfolio-level math uses **simple (arithmetic) returns**, since
  portfolio return is a weighted sum of asset simple returns — that
  identity does not hold for log returns.
- Optimization is **long-only** (no short-selling, weights ≥ 0) and
  **fully invested** (weights sum to 100%) — no leverage.
- The efficient frontier sweeps target returns from the lowest to highest
  individual-asset return and solves the minimum-variance portfolio at each
  target via `scipy.optimize.minimize` (SLSQP).
- This is a **backward-looking** optimization: "optimal" means optimal
  given historical returns/covariances, not a forecast. Past performance
  is not indicative of future results.

## License

MIT — do whatever you like with it, attribution appreciated.
