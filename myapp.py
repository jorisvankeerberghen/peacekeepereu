import streamlit as st
from TravelAuth import display_form 
from PIL import Image

# Define a function for each of your pages
def home_page():
    st.title("EU Peace Keeper Project")
    image_url = "https://i.ibb.co/gdw5kz4/PK2.jpg"
    #st.write("Welcome to the home page!")
    #img = Image.open(".\images\PK2.jpg")
    st.image(image_url)

def page1():
    st.title("Data Analysis")
    st.write("This is page 1.")

def page2():
    st.title("Travel Authorisation Form")
    display_form()


# Use a sidebar for navigation between pages
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ('EU Peace Keeper Project', 'Data Analysis', 'Travel authorisation'))

# Display the selected page with the radio buttons
if page == 'EU Peace Keeper Project':
    home_page()
elif page == 'Data Analysis':
    page1()
elif page == 'Travel authorisation':
    page2()

