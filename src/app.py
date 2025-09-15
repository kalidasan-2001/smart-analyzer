# src/app.py
from pathlib import Path
import pandas as pd
import streamlit as st
import utils as utils_mod              # for debug: shows which utils is imported
from utils import some_utility_function

st.set_page_config(page_title="Utility Demo", layout="wide")

def main():
    st.title("Utility function demo")

    # data.csv is in the PROJECT ROOT, not in src/
    data_path = Path(__file__).resolve().parent.parent / "data.csv"
    st.caption(f"Reading CSV from: {data_path}")

    if data_path.exists():
        df = pd.read_csv(data_path)
        st.dataframe(df.tail(5), use_container_width=True)
    else:
        st.warning("data.csv not found yet. Start the simulator or upload a CSV.")
        df = pd.DataFrame()

    # DEBUG: show which utils.py was imported
    st.caption(f"Using utils at: {Path(utils_mod.__file__).resolve()}")

    # Call your utility WITH the dataframe
    result = some_utility_function(df)
    st.subheader("Utility function output")
    st.json(result)

if __name__ == "__main__":
    main()
