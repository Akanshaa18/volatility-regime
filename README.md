# Volatility Regime Detection: Can LSTMs Outperform GARCH?

Predicting whether tomorrow's market will be **calm** (VIX ≤ 20) or **turbulent** (VIX > 20)
using classical GARCH(1,1) and an LSTM neural network trained on daily financial features.

---

## Quickstart

```bash
chmod +x job.sh
./job.sh          # creates conda env, runs all notebooks sequentially
```

---
`data.py` : downloads raw data
## Notebooks

| # | Notebook | Description |
|---|----------|-------------|
| 1 | `preprocessing_eda.ipynb` | Load 6 raw series, align to trading calendar, forward-fill gaps, transformation, ADF stationarity tests, EDA plots |
| 2 | `garch_baseline.ipynb` | Fit GARCH(1,1) on S&P 500 returns via walk-forward validation, convert variance forecasts to regime predictions, evaluate with accuracy / precision / recall / F1 / AUC |
| 3 | `feature_engineering.ipynb` | Build 21-day rolling realized volatility and yield curve spread, standardize features, construct sliding 20-day window sequences, create PyTorch Dataset and DataLoader, save X_train/val/test arrays |
| 4 | `lstm_model.ipynb` | Define LSTM architecture (1 layer, 64 hidden units, dropout 0.2), hyperparameter search over window/hidden/dropout, train final model with early stopping and weighted loss, evaluate on test set |
| 5 | `walk_forward_cv.ipynb` | 5-fold expanding-window cross-validation — refit both GARCH and LSTM from scratch at each fold, collect fold-level metrics, produce mean ± std summary |
| 6 | `comparison_analysis.ipynb` | Head-to-head metrics table, ROC curves, confusion matrices, regime prediction timeline, sensitivity check at VIX=30, crisis period breakdown |

---

## Data

All raw data saved to `data/raw/` after running `data.py` once.
Processed features and model results saved to `data/processed/`.

| Series | Source | FRED Code |
|--------|--------|-----------|
| VIX | FRED | `VIXCLS` |
| S&P 500 | Stooq | `^SPX` |
| 10Y Treasury | FRED | `DGS10` |
| 2Y Treasury | FRED | `DGS2` |
| Fed Funds Rate | FRED | `DFF` |
| Credit Spread | FRED | `BAA10Y` |

---

## Project Structure

```
├── data/
│   ├── raw/              # downloaded CSVs
│   └── processed/        # master.csv, X/y arrays, model results
├── preprocessing_eda.ipynb/
├── garch_baseline.ipynb/
├── feature_engineering.ipynb/
├── lstm_model.ipynb/
├── walk_forward_cv.ipynb/
├── comparison_analysis.ipynb/              
├── models/               # saved LSTM weights + scaler
├── plots/                # all generated figures
├── logs/                 # nbconvert execution logs
├── data.py      # run once to fetch raw data
├── environment.yaml      # conda environment
└── job.sh                # pipeline runner
```
