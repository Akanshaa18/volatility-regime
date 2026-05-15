import pandas as pd
import numpy as np

def generate_final_panel():
    """
    Initial cleaning and generating final panel
    """
    #loading all CSVs into df
    creditdf = pd.read_csv("data/raw/credit.csv", index_col="date", parse_dates=True)
    fedfundsdf = pd.read_csv("data/raw/fedfunds.csv",index_col="date", parse_dates=True)
    sp500df = pd.read_csv("data/raw/sp500.csv",index_col="date", parse_dates=True)
    t2ydf = pd.read_csv("data/raw/t2y.csv", index_col="date", parse_dates=True)
    t10ydf = pd.read_csv("data/raw/t10y.csv", index_col="date", parse_dates=True)
    vixdf = pd.read_csv("data/raw/vix.csv", index_col="date", parse_dates=True)

    #aligning calendar for all the series to match S&P500
    trading_calendar = sp500df.index

    creditdf = creditdf.reindex(trading_calendar)
    fedfundsdf = fedfundsdf.reindex(trading_calendar)
    t2ydf = t2ydf.reindex(trading_calendar)
    t10ydf = t10ydf.reindex(trading_calendar)
    vixdf = vixdf.reindex(trading_calendar)

    #dealing with missing values in credit and treasury 
    #reported data for federal holidays

    #setting limit as 3 to account for instances that the holiday
    # is Monday and last business day is a Friday
    t10ydf = t10ydf.ffill(limit=3)
    t2ydf = t2ydf.ffill(limit=3)
    creditdf = creditdf.ffill(limit=3)

    finaldf = sp500df.copy()
    finaldf = finaldf.join([vixdf, t10ydf, t2ydf, fedfundsdf, creditdf])
    print("Missing values after alignment and forward fill:")
    print(finaldf.isna().sum())
    print(f"\nDate range: {finaldf.index[0].date()} to {finaldf.index[-1].date()}")
    print(f"Total trading days: {len(finaldf)}")
    
    return finaldf

def apply_transformation(df):
    """
    Apply stationarity transformations to all the raw data
    - sp500 : log return
    - vix : first difference
    - t2y, t10y : first difference
    - fedfunds : first difference
    - credit : first difference

    Returns a new df with all the transformed columns
    """

    #log return for price
    df["sp500_return"] = np.log(df["sp500"].diff())
    df.drop(columns = ["sp500"], inplace=True)

    #first difference
    for col in ["vix", "t2y", "t10y", "fedfunds", "credit"]:
        df[f"{col}_diff"] = df[col].diff()
        df.drop(columns=[col], inplace=True)

    df.dropna(inplace=True)

    return df


if __name__ == "__main__":
    finaldf = generate_final_panel()
    
    finaldf = apply_transformation(finaldf)
    print(finaldf.head())
    print(f"\nShape: {finaldf.shape}")
    print(f"\nColumns: {finaldf.columns.tolist()}")
    print(f"\nMissing values:\n{finaldf.isna().sum()}")


    finaldf.to_csv("data/processed/master.csv")