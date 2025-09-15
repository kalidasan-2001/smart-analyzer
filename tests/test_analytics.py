import pandas as pd
from analytics import zscore_anomalies

def test_empty_series():
    s = pd.Series(dtype=float)
    out = zscore_anomalies(s)
    assert out.empty

def test_outlier_flagged():
    s = pd.Series([10,10,10,50])
    out = zscore_anomalies(s, threshold=2.0)
    assert out.iloc[-1] and not out.iloc[0]