import streamlit as st

# Define a function for each of your pages
def home_page():
    st.title("Home Page")
    st.write("Welcome to the home page!")

def page1():
    st.title("Page 1")
    st.write("This is page 1.")

def page2():
    st.title("Page 2")
    st.write("This is page 2.")

def page3():
    st.title("Page 3")
    st.write("This is page 3.")

def page4():
    st.title("Page 4")
    st.write("This is page 4.")

# Use a sidebar for navigation between pages
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ('Home', 'Page 1', 'Page 2', 'Page 3', 'Page 4'))

# Display the selected page with the radio buttons
if page == 'Home':
    home_page()
elif page == 'Page 1':
    page1()
elif page == 'Page 2':
    page2()
elif page == 'Page 3':
    page3()
elif page == 'Page 4':
    page4()
