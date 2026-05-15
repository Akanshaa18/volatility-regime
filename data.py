import os
import io
import requests
import pandas as pd
from fredapi import Fred
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("FRED_API_KEY")
if not api_key:
    raise ValueError("API Key not found")
fred = Fred(api_key=api_key) 

START = "2005-01-01"
END = "2024-12-31"
START_STQ = "20050101"    # for Stooq URL format: YYYYMMDD
END_STQ   = "20241231"

SERIES = {
    "vix": "VIXCLS", # CBOE VIX - target variables + features
    "t10y": "DGS10", # 10 year treasury yield
    "t2y": "DGS2", # 2 year treasury yield
    "fedfunds": "DFF",  # Federal Funds rate
    "credit": "BAA10Y" # BAA corporate soread over 10Y treasury
}

os.makedirs("data/raw", exist_ok= True)

for name, code in SERIES.items():
    print(f"Downloading {name} data")
    series = fred.get_series(code, observation_start=START, observation_end = END)
    df = series.to_frame(name = name)
    df.index.name = "date"
    filepath = f"data/raw/{name}.csv"
    df.to_csv(filepath)
    print(f"Saved to {filepath}")
    print(f"({len(df)} rows, {df.index[0].date()} → {df.index[-1].date()})")
print("\nAll series downloaded successfully.")

#Downloaded sp500 from Stooq directly, modifying csv to only keep close data
sp500 = pd.read_csv("data/raw/sp500.csv")
sp500.columns = sp500.columns.str.lower()
sp500["date"] = pd.to_datetime(sp500["date"])
sp500 = sp500.set_index("date").sort_index(ascending=True)
sp500 = sp500[["close"]].rename(columns={"close": "sp500"})
sp500.to_csv("data/raw/sp500.csv")