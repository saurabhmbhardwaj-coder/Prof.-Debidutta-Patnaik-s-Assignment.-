"""Plain-English glossary content for the Learn tab."""

GLOSSARY = [
    {
        "term": "Simple Return",
        "short": "How much a price moved, in percent, over one period.",
        "long": (
            "Return = (Price_today - Price_yesterday) / Price_yesterday. "
            "If a stock goes from 100 to 105, that's a 5% simple return. "
            "Portfolio math uses simple returns (not log returns) because a "
            "portfolio's return is just a weighted average of its holdings' "
            "simple returns — that identity only holds for simple returns."
        ),
    },
    {
        "term": "Volatility (Standard Deviation)",
        "short": "How much returns bounce around their average — the usual stand-in for 'risk'.",
        "long": (
            "A stock that returns +1%, -1%, +1%, -1% every day has the same "
            "average return as one that returns +10%, -10%, +10%, -10%, but "
            "the second is far riskier. Volatility captures that. It's "
            "usually annualized by multiplying the daily standard deviation "
            "by sqrt(252), since there are about 252 trading days in a year."
        ),
    },
    {
        "term": "Covariance & Correlation",
        "short": "Whether two assets tend to move together, and how strongly.",
        "long": (
            "Covariance measures whether two assets move in the same "
            "direction (positive), opposite directions (negative), or "
            "independently (near zero). Correlation is the same idea "
            "rescaled to always fall between -1 and +1, which makes it "
            "easier to interpret. This matters for diversification: mixing "
            "assets that *don't* move together reduces portfolio risk more "
            "than mixing assets that do."
        ),
    },
    {
        "term": "Diversification",
        "short": "Combining assets so the portfolio's ups and downs partly cancel out.",
        "long": (
            "Because different assets don't move in perfect lockstep, a mix "
            "of them is usually less volatile than the average volatility of "
            "the pieces. This is the only free lunch in investing — you can "
            "often reduce risk without giving up expected return, just by "
            "combining assets that aren't perfectly correlated."
        ),
    },
    {
        "term": "Efficient Frontier",
        "short": "The curve of best possible portfolios — max return for each level of risk.",
        "long": (
            "For any target return, there's a mix of assets that achieves it "
            "with the *least* possible risk. Plot all of those (risk, return) "
            "points and you get a curve — the efficient frontier. Any "
            "portfolio sitting to the right of the curve is 'dominated': "
            "some frontier portfolio gets the same return with less risk, or "
            "more return for the same risk. Individual assets almost always "
            "sit to the right of the frontier, which is the mathematical "
            "case for diversifying rather than holding one stock."
        ),
    },
    {
        "term": "Sharpe Ratio",
        "short": "Return earned per unit of risk taken, above the risk-free rate.",
        "long": (
            "Sharpe = (Portfolio Return - Risk-Free Rate) / Portfolio "
            "Volatility. Two portfolios can have the same return, but the "
            "one that got there with less bumpiness has the higher (better) "
            "Sharpe ratio. The 'max-Sharpe' or 'tangency' portfolio is the "
            "single point on the efficient frontier with the best "
            "risk-adjusted return — it's the portfolio this app highlights "
            "as 'optimal.'"
        ),
    },
    {
        "term": "Risk-Free Rate",
        "short": "The return on an investment considered to have (near) zero risk.",
        "long": (
            "Usually proxied by government treasury yields (e.g. a 91-day "
            "T-bill rate). It's the baseline return you could get for taking "
            "essentially no risk, so it's the benchmark every risk-adjusted "
            "metric (Sharpe, Treynor, Alpha) measures 'extra' return against."
        ),
    },
    {
        "term": "CAPM: Beta",
        "short": "How sensitive an asset is to overall market moves.",
        "long": (
            "Beta = Covariance(asset, market) / Variance(market). A beta of "
            "1.0 means the asset tends to move with the market. Beta > 1 "
            "means it amplifies market moves (more volatile than the "
            "market); beta < 1 means it dampens them. A negative beta "
            "(rare) means it tends to move opposite the market."
        ),
    },
    {
        "term": "CAPM: Alpha",
        "short": "Return earned above what beta and the market would predict.",
        "long": (
            "The Capital Asset Pricing Model predicts an expected return "
            "based only on an asset's beta: Expected Return = Risk-Free "
            "Rate + Beta x (Market Return - Risk-Free Rate). Alpha is the "
            "gap between what actually happened and that prediction. "
            "Positive alpha means the portfolio outperformed what its "
            "market risk alone would justify -- the number active managers "
            "are usually judged on."
        ),
    },
    {
        "term": "Sortino Ratio",
        "short": "Like Sharpe, but only punishes downside volatility.",
        "long": (
            "The Sharpe ratio penalizes ALL volatility, including big "
            "positive days, which investors don't actually mind. Sortino "
            "only counts volatility from returns falling below a minimum "
            "acceptable return, so it doesn't punish a portfolio for having "
            "occasional great days."
        ),
    },
    {
        "term": "Value at Risk (VaR)",
        "short": "The loss you'd expect to exceed only in your worst 5% of days.",
        "long": (
            "5% VaR answers: 'What's the return threshold such that only 5% "
            "of days were worse than this?' If daily 5% VaR is -3%, it means "
            "on 95% of days you lost less than 3% (or gained). It's a "
            "common regulatory and risk-management benchmark, though it "
            "says nothing about how bad that worst 5% actually gets."
        ),
    },
    {
        "term": "Conditional VaR (CVaR / Expected Shortfall)",
        "short": "The average loss on those worst days VaR only draws a line at.",
        "long": (
            "CVaR fixes VaR's blind spot: instead of just the threshold, it "
            "averages all the returns that fell beyond that threshold. If "
            "VaR is -3%, CVaR might be -5%, telling you that when things go "
            "bad, they average -5%, not just 'worse than -3%.'"
        ),
    },
    {
        "term": "Maximum Drawdown",
        "short": "The worst peak-to-trough decline the portfolio ever experienced.",
        "long": (
            "If a portfolio grows to its highest-ever value, then falls "
            "before recovering, max drawdown is the size of that largest "
            "fall (e.g. -25% means it lost a quarter of its value from its "
            "prior peak at some point). It's a visceral, easy-to-explain "
            "risk metric because it's literally 'how bad did it get.'"
        ),
    },
    {
        "term": "Skewness & Kurtosis",
        "short": "The shape of the return distribution — lopsidedness and fat tails.",
        "long": (
            "Skewness measures asymmetry: negative skew means occasional "
            "large losses are more common than large gains (a long left "
            "tail) — common in equities. Kurtosis measures how 'fat-tailed' "
            "the distribution is versus a normal bell curve; high kurtosis "
            "means extreme days (in either direction) happen more often "
            "than a normal distribution would predict."
        ),
    },
    {
        "term": "Rebalancing",
        "short": "Periodically trading back to your target weights as they drift.",
        "long": (
            "If you start 50/50 in two assets and one grows faster, you "
            "drift away from 50/50 over time. Rebalancing means periodically "
            "selling some of the winner and buying the laggard to restore "
            "target weights. It has a cost (transaction fees, and taxes in "
            "some jurisdictions), which is why frequency (daily vs monthly "
            "vs yearly) is a real trade-off, not just a technicality."
        ),
    },
    {
        "term": "Long-Only / Full Investment Constraint",
        "short": "Rules that keep the optimizer realistic: no shorting, no leverage.",
        "long": (
            "An unconstrained optimizer might suggest short-selling one "
            "stock to buy more of another, or borrowing money to invest more "
            "than 100% of your capital. 'Long-only' (weights >= 0) forbids "
            "shorting; 'full investment' (weights sum to 100%) forbids "
            "leverage or holding cash outside the model. This app applies "
            "both, matching how most retail/student portfolios are expected "
            "to behave."
        ),
    },
    {
        "term": "Backtesting",
        "short": "Testing a strategy on historical data it didn't get to see in advance.",
        "long": (
            "A naive backtest checks how a strategy would have performed on "
            "the same data used to build it — which flatters the strategy, "
            "since it was optimized to fit exactly that history. A more "
            "honest 'walk-forward' backtest re-optimizes only on past data "
            "and tests forward on unseen data, repeating this through time, "
            "so it doesn't get credit for hindsight."
        ),
    },
    {
        "term": "Monte Carlo Simulation",
        "short": "Simulating thousands of possible futures to see a range of outcomes.",
        "long": (
            "Instead of relying on one historical path, Monte Carlo "
            "simulation generates many random future return paths (based on "
            "the historical mean/volatility/correlations) and looks at the "
            "spread of outcomes. It's useful for answering 'what's the range "
            "of plausible outcomes,' not just 'what's the single expected "
            "outcome.'"
        ),
    },
]
