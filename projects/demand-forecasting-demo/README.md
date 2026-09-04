# Demand Forecasting Demo

A small forecasting project that predicts the next six months of demand from synthetic monthly historical data.

> Portfolio lab project created with AI-assisted development. The dataset is synthetic and is intended only to demonstrate a practical forecasting workflow.

## What it demonstrates

- Time-series feature engineering
- Trend and seasonality modeling
- Linear regression
- Holdout validation
- Mean Absolute Error (MAE)
- Six-month demand forecasting
- Data visualization with Matplotlib

## Forecast preview

![Demand forecast](forecast.svg)

The model uses a time trend plus sine/cosine seasonal features. It validates on the latest six historical months before refitting on the full dataset and producing a six-month forecast.

## Run locally

```bash
pip install -r requirements.txt
python forecast.py
```

The script prints the validation MAE and future monthly forecasts, then generates `forecast.svg`.

## Files

```text
demand-forecasting-demo/
├── forecast.py
├── monthly_demand.csv
├── forecast.svg
└── requirements.txt
```

## Why this project matters

Forecasting supports purchasing, staffing, inventory, production planning, and budgeting. This project demonstrates a transparent baseline approach that is simple enough to explain while still capturing trend and annual seasonality.
