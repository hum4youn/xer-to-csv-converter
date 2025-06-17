import streamlit as st
import pandas as pd
from xerparser import Xer
import io

st.title("Primavera XER → CSV Converter")

uploaded_file = st.file_uploader("Upload .XER file", type=["xer"])
if uploaded_file:
    data = uploaded_file.read()
    with st.spinner("Parsing XER file…"):
        try:
            xer = Xer.reader(io.BytesIO(data))
        except Exception as e:
            st.error(f"Failed to parse XER: {e}")
            st.stop()

        # Convert top-level tables to DataFrames
        tables = {
            "Projects": xer.projects,
            "Tasks": xer.tasks,
            "Resources": xer.resources,
            # add more if needed
        }
        for name, items in tables.items():
            if not items:
                continue
            df = pd.DataFrame([vars(obj) for obj in items.values()]) if isinstance(items, dict) else pd.DataFrame(items)
            st.subheader(name)
            st.dataframe(df.head())
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(f"Download {name}.csv", csv, file_name=f"{name}.csv", mime="text/csv")
