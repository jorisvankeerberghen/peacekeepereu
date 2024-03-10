import streamlit as st
from TravelAuth import display_form 
from TravelAuth import initiate_model 
from PIL import Image

# Define a function for each of your pages
def home_page():
    st.title("EU Peace Keeper Project")
    #st.write("Welcome to the home page!")
    img = Image.open(".\images\PK2.jpg")
    st.image(img)

def page1():
    st.title("Analyse des données")
    st.write("This is page 1.")

def page2():
    st.title("Travel Authorisation Form")
    display_form()


# Use a sidebar for navigation between pages
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ('Home', 'Analyse des données', 'Travel authorisation'))

# Display the selected page with the radio buttons
if page == 'Home':
    home_page()
elif page == 'Analyse des données':
    page1()
elif page == 'Travel authorisation':
    page2()

