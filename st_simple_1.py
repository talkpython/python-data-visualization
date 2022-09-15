from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

src_file = Path.cwd() / "data" / "raw" / "EPA_fuel_economy_summary.csv"
df = pd.read_csv(src_file)

fig = px.histogram(
    df,
    x="fuelCost08",
    color="class_summary",
    labels={"fuelCost08": "Annual Fuel Cost"},
    nbins=40,
    title="Fuel Cost Distribution",
)

st.title("Simple Example")
st.write(fig)

