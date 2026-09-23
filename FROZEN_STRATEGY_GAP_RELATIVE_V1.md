# Gap Relative Continuation V1 — Frozen Strategy Specification

**Status:** Frozen before locked validation  
**SHA-256 of canonical strategy spec:** `c4280315b983cefe0d1a1b94aad53ba0d6901c2e44f1de67db3eddba8f831a6b`

## Rules

- Universe: AXISBANK, HDFCBANK, ICICIBANK, INFY, LT, RELIANCE, SBIN, TCS.
- 5-minute candles. Capital ₹2,00,000. No leverage. Maximum 2 trades/day.
- Gap = 09:15 open / prior regular-session close - 1. Ignore absolute gaps above 8%.
- Market gap = median gap across the fixed 8-stock universe. Relative gap = stock gap - market gap.
- At 10:15, after the 10:10–10:15 candle closes:
  - LONG when gap >= +1.5%, relative gap >= +0.5%, and 10:15 close > 09:15 open.
  - SHORT when gap <= -1.5%, relative gap <= -0.5%, and 10:15 close < 09:15 open.
- If more than two stocks qualify, take the two largest absolute relative gaps.
- Enter at the next 5-minute bar open at 10:15.
- Position sizing: ₹1,000 risk budget per trade; maximum ₹1,00,000 notional per trade.
- Stop: 1.0% adverse from actual entry. Target: 1.5% favorable.
- Time exit: 11:45 close. No re-entry. If stop and target are both touched in one candle, assume stop first.
- Baseline execution model: 2 bps adverse slippage at entry and normal exit plus 2 bps adverse stop-fill slippage; current Angel One equity-intraday fees applied to every historical trade.

## Research results before locked validation

| Sample | Trades | Net P&L | Win rate | Profit factor | Avg R | Max DD |
|---|---:|---:|---:|---:|---:|---:|
| Train: Jan–Sep 2024 | 18 | ₹1,552.07 | 55.6% | 1.36 | +0.089R | -₹2,462.45 |
| Development holdout: Oct 2024–Mar 2025 | 11 | ₹2,320.69 | 72.7% | 4.18 | +0.213R | -₹385.13 |
| Secondary research: Sep 2025–Jul 2026, pre-CAS | 43 | ₹7,409.91 | 62.8% | 2.02 | +0.174R | -₹2,703.54 |
| Combined research only | 72 | ₹11,282.68 | 62.5% | 1.92 | +0.159R | -₹2,703.54 |

These are research results, not a guarantee of future profitability. The locked Apr–Sep 2025 sample has not been inspected and must be tested without changing the frozen rules.
