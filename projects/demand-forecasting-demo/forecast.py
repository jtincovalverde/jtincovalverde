from pathlib import Path
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "monthly_demand.csv"
CHART_PATH = BASE_DIR / "forecast.svg"
PLANNING_SUMMARY_PATH = BASE_DIR / "planning_summary.csv"
EXECUTIVE_PLAN_PATH = BASE_DIR / "executive_plan.md"

FORECAST_HORIZON = 6

# Synthetic planning assumptions used to translate demand into an operations decision.
STANDARD_HOURS_PER_UNIT = 2.0
PRODUCTIVE_HOURS_PER_WORKER = 135.0
CURRENT_WORKERS = 4


def make_features(index: np.ndarray) -> np.ndarray:
    return np.column_stack(
        [
            index,
            np.sin(2 * np.pi * index / 12),
            np.cos(2 * np.pi * index / 12),
        ]
    )


def risk_level(utilization_pct: float, high_required_hours: float, available_hours: float) -> str:
    if utilization_pct > 100:
        return "CRITICAL"
    if high_required_hours > available_hours or utilization_pct >= 98:
        return "WATCH"
    return "HEALTHY"


def recommendation(row: pd.Series) -> str:
    if row["overtime_hours"] > 0:
        return (
            f"Use about {row['overtime_hours']:.0f} h of targeted overtime/flexible capacity "
            "before adding a permanent worker."
        )
    if row["high_required_hours"] > row["available_hours"]:
        return (
            "Base demand fits current capacity, but the high-demand scenario does not; "
            "reserve flexible overtime instead of permanent idle capacity."
        )
    if row["utilization_pct"] >= 98:
        return "Protect a small flexible-capacity buffer and monitor demand closely."
    return "Current workforce is sufficient; continue monitoring forecast versus actual demand."


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH, parse_dates=["month"])


def fit_and_forecast(data: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    index = np.arange(len(data))
    features = make_features(index)

    split = max(len(data) - 6, 12)
    validation_model = LinearRegression()
    validation_model.fit(features[:split], data["demand"].iloc[:split])

    validation_predictions = validation_model.predict(features[split:])
    mae = mean_absolute_error(data["demand"].iloc[split:], validation_predictions)

    model = LinearRegression()
    model.fit(features, data["demand"])

    future_index = np.arange(len(data), len(data) + FORECAST_HORIZON)
    future_forecast = model.predict(make_features(future_index))
    future_dates = pd.date_range(
        data["month"].iloc[-1] + pd.offsets.MonthBegin(1),
        periods=FORECAST_HORIZON,
        freq="MS",
    )

    forecast = pd.DataFrame(
        {
            "month": future_dates,
            "base_forecast": np.rint(future_forecast).astype(int),
            # MAE is used as a transparent planning band, not a formal statistical interval.
            "low_scenario": np.floor(np.maximum(0, future_forecast - mae)).astype(int),
            "high_scenario": np.ceil(future_forecast + mae).astype(int),
        }
    )
    return forecast, mae


def build_capacity_plan(forecast: pd.DataFrame) -> pd.DataFrame:
    plan = forecast.copy()
    plan["required_hours"] = plan["base_forecast"] * STANDARD_HOURS_PER_UNIT
    plan["high_required_hours"] = plan["high_scenario"] * STANDARD_HOURS_PER_UNIT
    plan["available_hours"] = CURRENT_WORKERS * PRODUCTIVE_HOURS_PER_WORKER
    plan["capacity_units"] = plan["available_hours"] / STANDARD_HOURS_PER_UNIT
    plan["capacity_gap_hours"] = plan["available_hours"] - plan["required_hours"]
    plan["utilization_pct"] = plan["required_hours"] / plan["available_hours"] * 100
    plan["workers_required"] = np.ceil(
        plan["required_hours"] / PRODUCTIVE_HOURS_PER_WORKER
    ).astype(int)
    plan["overtime_hours"] = plan["capacity_gap_hours"].apply(
        lambda gap: max(0.0, -float(gap))
    )
    plan["risk"] = plan.apply(
        lambda row: risk_level(
            row["utilization_pct"],
            row["high_required_hours"],
            row["available_hours"],
        ),
        axis=1,
    )
    plan["management_action"] = plan.apply(recommendation, axis=1)
    return plan


def print_summary(plan: pd.DataFrame, mae: float) -> None:
    capacity_units = CURRENT_WORKERS * PRODUCTIVE_HOURS_PER_WORKER / STANDARD_HOURS_PER_UNIT
    peak = plan.loc[plan["base_forecast"].idxmax()]
    months_over_capacity = int((plan["capacity_gap_hours"] < 0).sum())

    print("DEMAND & CAPACITY PLANNING SYSTEM")
    print("-" * 84)
    print(f"Validation MAE: {mae:.2f} units")
    print(
        f"Current capacity: {capacity_units:.0f} units/month "
        f"({CURRENT_WORKERS} workers × {PRODUCTIVE_HOURS_PER_WORKER:.0f} productive h)"
    )
    print(f"Months over base capacity: {months_over_capacity}/{len(plan)}")
    print(
        f"Peak base forecast: {peak['base_forecast']:.0f} units "
        f"({peak['month']:%Y-%m})"
    )
    print("-" * 84)
    print(
        plan[
            [
                "month",
                "base_forecast",
                "high_scenario",
                "utilization_pct",
                "capacity_gap_hours",
                "risk",
            ]
        ].to_string(index=False)
    )


def export_planning_summary(plan: pd.DataFrame) -> None:
    output = plan.copy()
    output["month"] = output["month"].dt.strftime("%Y-%m")
    columns = [
        "month",
        "base_forecast",
        "low_scenario",
        "high_scenario",
        "required_hours",
        "available_hours",
        "capacity_gap_hours",
        "utilization_pct",
        "workers_required",
        "overtime_hours",
        "risk",
        "management_action",
    ]
    output[columns].to_csv(PLANNING_SUMMARY_PATH, index=False)


def build_chart(history: pd.DataFrame, plan: pd.DataFrame) -> None:
    capacity_units = (
        CURRENT_WORKERS * PRODUCTIVE_HOURS_PER_WORKER / STANDARD_HOURS_PER_UNIT
    )

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(history["month"], history["demand"], marker="o", label="Historical demand")
    ax.plot(
        plan["month"],
        plan["base_forecast"],
        marker="o",
        linestyle="--",
        label="Base forecast",
    )
    ax.fill_between(
        plan["month"],
        plan["low_scenario"],
        plan["high_scenario"],
        alpha=0.18,
        label="Planning band (± validation MAE)",
    )
    ax.axhline(
        capacity_units,
        linestyle=":",
        linewidth=2,
        label=f"Current capacity ({capacity_units:.0f} units/month)",
    )

    ax.set_title("Demand Forecast vs. Current Operating Capacity")
    ax.set_ylabel("Units per month")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(CHART_PATH, format="svg")


def build_executive_plan(plan: pd.DataFrame, mae: float) -> None:
    capacity_hours = CURRENT_WORKERS * PRODUCTIVE_HOURS_PER_WORKER
    capacity_units = capacity_hours / STANDARD_HOURS_PER_UNIT

    peak = plan.loc[plan["base_forecast"].idxmax()]
    months_over_capacity = int((plan["capacity_gap_hours"] < 0).sum())
    watch_or_critical = int(plan["risk"].isin(["WATCH", "CRITICAL"]).sum())

    rows = []
    for row in plan.itertuples():
        rows.append(
            f"| {row.month:%Y-%m} | {row.base_forecast:.0f} | {row.low_scenario:.0f} | "
            f"{row.high_scenario:.0f} | {row.utilization_pct:.1f}% | "
            f"{row.capacity_gap_hours:+.1f} h | {row.risk} |"
        )

    permanent_worker_extra_hours = PRODUCTIVE_HOURS_PER_WORKER
    targeted_peak_overtime = max(0.0, -float(peak["capacity_gap_hours"]))

    report = f"""# Executive Demand & Capacity Plan

## Management question

**How much demand should the operation prepare for over the next six months, and does that forecast justify more permanent capacity?**

The forecast is translated into labor capacity so the output is not only a prediction; it becomes a staffing and capacity decision.

## Planning assumptions

| Assumption | Value |
| --- | ---: |
| Current workforce | {CURRENT_WORKERS} workers |
| Productive hours per worker | {PRODUCTIVE_HOURS_PER_WORKER:.0f} h/month |
| Standard labor time | {STANDARD_HOURS_PER_UNIT:.1f} h/unit |
| Current monthly capacity | {capacity_units:.0f} units |
| Validation MAE | {mae:.2f} units |

> The dataset and planning assumptions are synthetic. The MAE band is a transparent planning scenario, not a formal statistical confidence interval.

## Six-month planning view

| Month | Base | Low | High | Utilization | Capacity gap | Risk |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
{chr(10).join(rows)}

## Executive interpretation

- The **peak base forecast** is **{peak['base_forecast']:.0f} units in {peak['month']:%B %Y}**.
- Current capacity is **{capacity_units:.0f} units/month**.
- The base plan exceeds current capacity in **{months_over_capacity} of {len(plan)} months**.
- **{watch_or_critical} months** require a watch/critical flag once the higher-demand planning scenario is considered.
- The highest base-case overload is **{targeted_peak_overtime:.1f} labor hours**.

## Recommended management decision

**Do not add one permanent worker solely because of this six-month forecast.**

At the peak base forecast, the shortage is about **{targeted_peak_overtime:.1f} h**. A permanent worker would add approximately **{permanent_worker_extra_hours:.0f} productive h/month**, creating much more capacity than the base-case shortage requires.

A more efficient first response is:

1. reserve targeted overtime or flexible capacity for peak months;
2. monitor actual demand against the forecast every month;
3. protect a small buffer when the high-demand scenario exceeds current capacity;
4. reconsider permanent hiring only if overload becomes persistent rather than seasonal.

## Why this matters

Forecasting becomes useful to management when it changes a decision. The objective is not merely to predict demand; it is to **prepare enough capacity without creating unnecessary idle time or permanent cost**.

---

*Portfolio lab using synthetic data and synthetic operating assumptions for demonstration purposes.*
"""
    EXECUTIVE_PLAN_PATH.write_text(report, encoding="utf-8")


def main() -> None:
    history = load_data()
    forecast, mae = fit_and_forecast(history)
    plan = build_capacity_plan(forecast)

    print_summary(plan, mae)
    export_planning_summary(plan)
    build_chart(history, plan)
    build_executive_plan(plan, mae)

    print("\nGenerated:")
    print(f"- {PLANNING_SUMMARY_PATH.name}")
    print(f"- {CHART_PATH.name}")
    print(f"- {EXECUTIVE_PLAN_PATH.name}")


if __name__ == "__main__":
    main()
