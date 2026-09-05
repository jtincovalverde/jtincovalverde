# Executive Demand & Capacity Plan

## Management question

**How much demand should the operation prepare for over the next six months, and does that forecast justify more permanent capacity?**

The forecast is translated into labor capacity so the output is not only a prediction; it becomes a staffing and capacity decision.

## Planning assumptions

| Assumption | Value |
| --- | ---: |
| Current workforce | 4 workers |
| Productive hours per worker | 135 h/month |
| Standard labor time | 2.0 h/unit |
| Current monthly capacity | 270 units |
| Validation MAE | 6.27 units |

> The dataset and planning assumptions are synthetic. The MAE band is a transparent planning scenario, not a formal statistical confidence interval.

## Six-month planning view

| Month | Base | Low | High | Utilization | Capacity gap | Risk |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 2026-07 | 270 | 263 | 277 | 100.0% | +0.0 h | WATCH |
| 2026-08 | 264 | 258 | 271 | 97.8% | +12.0 h | WATCH |
| 2026-09 | 262 | 255 | 268 | 97.0% | +16.0 h | HEALTHY |
| 2026-10 | 263 | 256 | 270 | 97.4% | +14.0 h | HEALTHY |
| 2026-11 | 269 | 262 | 276 | 99.6% | +2.0 h | WATCH |
| 2026-12 | 279 | 272 | 286 | 103.3% | -18.0 h | CRITICAL |

## Executive interpretation

- The **peak base forecast** is **279 units in December 2026**.
- Current capacity is **270 units/month**.
- The base plan exceeds current capacity in **1 of 6 months**.
- **4 months** require a WATCH/CRITICAL flag once the higher-demand planning scenario is considered.
- The highest base-case overload is **18.0 labor hours**.

## Recommended management decision

**Do not add one permanent worker solely because of this six-month forecast.**

At the peak base forecast, the shortage is about **18.0 h**. A permanent worker would add approximately **135 productive h/month**, creating much more capacity than the base-case shortage requires.

A more efficient first response is:

1. reserve targeted overtime or flexible capacity for peak months;
2. monitor actual demand against the forecast every month;
3. protect a small buffer when the high-demand scenario exceeds current capacity;
4. reconsider permanent hiring only if overload becomes persistent rather than seasonal.

## Management lesson

Forecasting becomes useful when it changes a decision. The objective is not merely to predict demand; it is to **prepare enough capacity without creating unnecessary idle time or permanent cost**.

---

*Portfolio lab using synthetic data and synthetic operating assumptions for demonstration purposes.*
