import streamlit as st

def display_form():
    with st.form("form1"):
        username = st.text_input("Enter your name")
        user_age = st.number_input("Enter your age", min_value=0, max_value=100, step=1)
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.write(f"Hello {username}, you are {user_age} years old.")