from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_PATH = Path(__file__).with_name("operations_data.csv")
OUTPUT_PATH = Path(__file__).with_name("capacity_vs_load.svg")


def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data["capacity_gap"] = data["available_hours"] - data["required_hours"]
    data["utilization_pct"] = (
        data["required_hours"] / data["available_hours"] * 100
    )
    return data


def print_summary(data: pd.DataFrame) -> None:
    bottleneck = data.loc[data["utilization_pct"].idxmax()]

    print("OPERATIONS KPI SUMMARY")
    print("-" * 48)
    for row in data.itertuples():
        status = "OVER CAPACITY" if row.capacity_gap < 0 else "OK"
        print(
            f"{row.work_center:12} | "
            f"utilization={row.utilization_pct:6.1f}% | "
            f"gap={row.capacity_gap:6.1f} h | {status}"
        )

    print("-" * 48)
    print(
        f"Bottleneck: {bottleneck['work_center']} "
        f"({bottleneck['utilization_pct']:.1f}% utilization)"
    )


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
    fig.savefig(OUTPUT_PATH, format="svg")
    print(f"Chart saved to {OUTPUT_PATH.name}")


if __name__ == "__main__":
    dataset = load_data()
    print_summary(dataset)
    build_chart(dataset)
