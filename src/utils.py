# src/app.py
from pathlib import Path
import pandas as pd
import streamlit as st

import utils  # optional, just to show which file was imported

st.set_page_config(page_title="Utility Demo", layout="wide")

def main():
    st.title("Utility function demo")

    # data.csv is in the project ROOT (one folder up from src/)
    data_path = Path(__file__).resolve().parent.parent / "data.csv"
    st.caption(f"Reading CSV from: {data_path}")

    if data_path.exists():
        df = pd.read_csv(data_path)
        st.dataframe(df.tail(5), use_container_width=True)
    else:
        st.warning("data.csv not found. Start the simulator or upload a CSV.")
        df = pd.DataFrame()

    # Show which utils.py is loaded (should be ...\src\utils.py)
    st.caption(f"utils module: {Path(utils.__file__).resolve()}")

    result = some_utility_function(df)
    st.subheader("Utility function output")
    st.json(result)

def some_utility_function(df):
    # Example: return the shape of the DataFrame
    return {"rows": df.shape[0], "columns": df.shape[1]}

if __name__ == "__main__":
    main()
