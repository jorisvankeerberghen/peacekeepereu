import streamlit as st

import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def display_form():
    with st.form("form1"):
        username = st.text_input("Enter your name")
        user_age = st.number_input("Enter your age", min_value=0, max_value=100, step=1)
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.write(f"Hello {username}, you are {user_age} years old.")
        st.write(f"Entry to Schengen Zone is REFUSED")

def initiate_model():
    return "Calucation done"
    