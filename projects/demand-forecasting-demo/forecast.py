from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


DATA_PATH = Path(__file__).with_name("monthly_demand.csv")
OUTPUT_PATH = Path(__file__).with_name("forecast.svg")


def make_features(index: np.ndarray) -> np.ndarray:
    return np.column_stack(
        [
            index,
            np.sin(2 * np.pi * index / 12),
            np.cos(2 * np.pi * index / 12),
        ]
    )


def main() -> None:
    data = pd.read_csv(DATA_PATH, parse_dates=["month"])
    index = np.arange(len(data))
    features = make_features(index)

    split = max(len(data) - 6, 12)
    model = LinearRegression()
    model.fit(features[:split], data["demand"].iloc[:split])

    validation_predictions = model.predict(features[split:])
    mae = mean_absolute_error(
        data["demand"].iloc[split:],
        validation_predictions,
    )

    model.fit(features, data["demand"])

    horizon = 6
    future_index = np.arange(len(data), len(data) + horizon)
    future_features = make_features(future_index)
    forecast = model.predict(future_features)

    future_dates = pd.date_range(
        data["month"].iloc[-1] + pd.offsets.MonthBegin(1),
        periods=horizon,
        freq="MS",
    )

    results = pd.DataFrame(
        {
            "month": future_dates,
            "forecast_demand": np.round(forecast).astype(int),
        }
    )

    print(f"Validation MAE: {mae:.2f} units")
    print("\n6-month forecast")
    print(results.to_string(index=False))

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(data["month"], data["demand"], marker="o", label="Historical demand")
    ax.plot(future_dates, forecast, marker="o", linestyle="--", label="Forecast")
    ax.set_title("Monthly Demand Forecast")
    ax.set_ylabel("Units")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, format="svg")
    print(f"\nChart saved to {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
