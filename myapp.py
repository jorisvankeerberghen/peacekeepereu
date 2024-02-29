import streamlit as st
from TravelAuth import display_form initiate_model

# Define a function for each of your pages
def home_page():
    st.title("EU Peace Keeper Project")
    st.write("Welcome to the home page!")

def page1():
    st.title("Analyse des données")
    st.write("This is page 1.")

def page2():
    st.title("Travel authorisation")
    st.write("Initiate the risk model")
    if st.button('Perform Calculation'):
        # Call the function
        result = initiate_model()
        # Display the result
        st.write(result)

    display_form()

def page3():
    st.title("Page 3")
    st.write("This is page 3.")

def page4():
    st.title("Page 4")
    st.write("This is page 4.")

# Use a sidebar for navigation between pages
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ('Home', 'Analyse des données', 'Travel authorisation', 'Page 3', 'Page 4'))

# Display the selected page with the radio buttons
if page == 'Home':
    home_page()
elif page == 'Analyse des données':
    page1()
elif page == 'Travel authorisation':
    page2()
elif page == 'Page 3':
    page3()
elif page == 'Page 4':
    page4()
