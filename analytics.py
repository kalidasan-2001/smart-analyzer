import pandas as pd

def zscore_anomalies(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    """
    Returns a boolean Series where True indicates an anomaly (|z-score| > threshold).
    """
    if series.empty:
        return pd.Series([], dtype=bool)
    z = (series - series.mean()) / series.std()
    return