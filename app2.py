import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Palmer Penguins Dataset Explorer")

# Daten laden
url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/inst/extdata/penguins.csv"
df = pd.read_csv(url)

st.subheader("Vorschau auf das Penguins-Dataset")
st.dataframe(df) 