# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import streamlit as st

st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value = 1, max_value = 5, help = "Select the number of forecast days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
# using fstring because the header is dynamic (any change in place, days or option would change the header)
st.subheader(f"{option} for the next {days} days in {place}")