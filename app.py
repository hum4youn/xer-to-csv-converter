import streamlit as st
from xerparser import Parser
import pandas as pd
import io

st.title("Primavera XER to CSV Converter")

uploaded_file = st.file_uploader("Upload XER File", type=["xer"])

if uploaded_file is not None:
    st.success("File uploaded!")

    content = uploaded_file.read()
    xer_file = io.StringIO(content.decode("utf-8", errors="ignore"))
    parser = Parser(xer_file)

    for name, df in parser.dataframes.items():
        st.subheader(name)
        st.dataframe(df.head())

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(f"Download {name}.csv", csv, file_name=f"{name}.csv", mime="text/csv")
