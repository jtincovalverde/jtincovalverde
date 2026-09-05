from pathlib import Path
import math

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "operations_data.csv"
CHART_PATH = BASE_DIR / "capacity_vs_load.svg"
SUMMARY_CSV_PATH = BASE_DIR / "management_summary.csv"
EXECUTIVE_REPORT_PATH = BASE_DIR / "executive_summary.md"


def risk_level(utilization_pct: float) -> str:
    if utilization_pct > 100:
        return "CRITICAL"
    if utilization_pct >= 90:
        return "WATCH"
    return "HEALTHY"


def management_action(row: pd.Series) -> str:
    if row["utilization_pct"] > 100:
        return "Add targeted capacity, overtime, or rebalance work if skills allow."
    if row["utilization_pct"] >= 90:
        return "Monitor closely and protect a capacity buffer before demand increases."
    return "Maintain buffer and evaluate whether spare capacity can support constrained areas."


def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data["capacity_gap"] = data["available_hours"] - data["required_hours"]
    data["utilization_pct"] = data["required_hours"] / data["available_hours"] * 100
    data["risk"] = data["utilization_pct"].apply(risk_level)
    data["management_action"] = data.apply(management_action, axis=1)
    return data


def build_management_snapshot(data: pd.DataFrame) -> dict:
    bottleneck = data.loc[data["utilization_pct"].idxmax()]
    total_required = data["required_hours"].sum()
    total_available = data["available_hours"].sum()
    total_buffer = total_available - total_required
    overall_utilization = total_required / total_available * 100
    overloaded_hours = (-data.loc[data["capacity_gap"] < 0, "capacity_gap"]).sum()
    positive_buffer = data.loc[data["capacity_gap"] > 0, "capacity_gap"].sum()

    targeted_hours = math.ceil(max(0.0, -float(bottleneck["capacity_gap"])))
    scenario_capacity = float(bottleneck["available_hours"]) + targeted_hours
    scenario_utilization = float(bottleneck["required_hours"]) / scenario_capacity * 100
    scenario_gap = scenario_capacity - float(bottleneck["required_hours"])

    return {
        "total_required": total_required,
        "total_available": total_available,
        "total_buffer": total_buffer,
        "overall_utilization": overall_utilization,
        "overloaded_hours": overloaded_hours,
        "positive_buffer": positive_buffer,
        "bottleneck": str(bottleneck["work_center"]),
        "bottleneck_utilization": float(bottleneck["utilization_pct"]),
        "bottleneck_gap": float(bottleneck["capacity_gap"]),
        "targeted_hours": targeted_hours,
        "scenario_capacity": scenario_capacity,
        "scenario_utilization": scenario_utilization,
        "scenario_gap": scenario_gap,
    }


def print_summary(data: pd.DataFrame, snapshot: dict) -> None:
    print("OPERATIONS MANAGEMENT CONTROL CENTER")
    print("-" * 78)
    for row in data.itertuples():
        print(
            f"{row.work_center:12} | "
            f"utilization={row.utilization_pct:6.1f}% | "
            f"gap={row.capacity_gap:6.1f} h | "
            f"risk={row.risk}"
        )

    print("-" * 78)
    print(f"Overall utilization: {snapshot['overall_utilization']:.1f}%")
    print(f"System capacity buffer: {snapshot['total_buffer']:.1f} h")
    print(
        f"Bottleneck: {snapshot['bottleneck']} "
        f"({snapshot['bottleneck_utilization']:.1f}% utilization, "
        f"{snapshot['bottleneck_gap']:.1f} h gap)"
    )
    print(
        f"Targeted scenario: +{snapshot['targeted_hours']} h at "
        f"{snapshot['bottleneck']} -> {snapshot['scenario_utilization']:.1f}% utilization"
    )


def export_management_summary(data: pd.DataFrame) -> None:
    columns = [
        "work_center",
        "required_hours",
        "available_hours",
        "capacity_gap",
        "utilization_pct",
        "risk",
        "management_action",
    ]
    data[columns].to_csv(SUMMARY_CSV_PATH, index=False)


def build_chart(data: pd.DataFrame) -> None:
    positions = range(len(data))
    width = 0.36

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.bar(
        [position - width / 2 for position in positions],
        data["required_hours"],
        width,
        label="Required hours",
    )
    ax.bar(
        [position + width / 2 for position in positions],
        data["available_hours"],
        width,
        label="Available hours",
    )

    ax.set_title("Capacity vs. Required Workload")
    ax.set_ylabel("Hours")
    ax.set_xticks(list(positions))
    ax.set_xticklabels(data["work_center"])
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHART_PATH, format="svg")


def build_executive_report(data: pd.DataFrame, snapshot: dict) -> None:
    rows = []
    for row in data.itertuples():
        rows.append(
            f"| {row.work_center} | {row.required_hours:.1f} h | "
            f"{row.available_hours:.1f} h | {row.utilization_pct:.1f}% | "
            f"{row.capacity_gap:+.1f} h | {row.risk} |"
        )

    report = f"""# Executive Operations Summary

## Management question

**Does the operation need more capacity everywhere, or is the problem concentrated in one work center?**

The data indicates a **localized constraint**, not a system-wide shortage. Total available capacity is **{snapshot['total_available']:.1f} h** against **{snapshot['total_required']:.1f} h** of required workload, leaving a net system buffer of **{snapshot['total_buffer']:.1f} h**. However, **{snapshot['bottleneck']}** is overloaded by **{abs(snapshot['bottleneck_gap']):.1f} h** and reaches **{snapshot['bottleneck_utilization']:.1f}% utilization**.

## Executive KPIs

| KPI | Result |
| --- | ---: |
| Total required workload | {snapshot['total_required']:.1f} h |
| Total available capacity | {snapshot['total_available']:.1f} h |
| Overall utilization | {snapshot['overall_utilization']:.1f}% |
| Net system capacity buffer | {snapshot['total_buffer']:.1f} h |
| Local overloaded hours | {snapshot['overloaded_hours']:.1f} h |
| Positive buffer in non-overloaded centers | {snapshot['positive_buffer']:.1f} h |
| Primary bottleneck | {snapshot['bottleneck']} |

## Work-center diagnosis

| Work center | Required | Available | Utilization | Gap | Risk |
| --- | ---: | ---: | ---: | ---: | --- |
{chr(10).join(rows)}

## Recommended management decision

1. **Do not add capacity everywhere by default.** The system has aggregate spare capacity.
2. **Address {snapshot['bottleneck']} first.** Its local gap is the immediate constraint.
3. **Check transferability before spending.** Determine whether any spare capacity in other centers can realistically support the constrained activity; capacity is not automatically interchangeable across skills, equipment, or routing.
4. **Test targeted capacity.** A scenario adding **{snapshot['targeted_hours']} h** to {snapshot['bottleneck']} raises local capacity to **{snapshot['scenario_capacity']:.1f} h**, reducing utilization to **{snapshot['scenario_utilization']:.1f}%** and leaving a **{snapshot['scenario_gap']:.1f} h** buffer.
5. **Protect resilience.** A utilization level near 100% removes the overload but still leaves little protection against variability, downtime, rework, or demand growth.

## Management lesson

**Aggregate capacity can look healthy while one local constraint still limits the operation.** The management task is not simply to add resources; it is to identify where the constraint is, validate whether spare capacity is transferable, and target the intervention where it changes system performance.

---

*Portfolio lab using synthetic data for demonstration purposes.*
"""
    EXECUTIVE_REPORT_PATH.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    dataset = load_data()
    management_snapshot = build_management_snapshot(dataset)
    print_summary(dataset, management_snapshot)
    export_management_summary(dataset)
    build_chart(dataset)
    build_executive_report(dataset, management_snapshot)
    print("\nGenerated:")
    print(f"- {SUMMARY_CSV_PATH.name}")
    print(f"- {CHART_PATH.name}")
    print(f"- {EXECUTIVE_REPORT_PATH.name}")
