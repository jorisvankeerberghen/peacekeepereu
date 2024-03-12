import streamlit as st
from TravelAuth import display_form 
from PIL import Image
from anomaly_detection import airline_anomaly_detection_streamlit_anomalies_page as anomalies_page
from anomaly_detection import airline_anomaly_detection_streamlit_anomaly_detector_page as anomaly_detector_page


# Define a function for each of your pages
def home_page():
    st.title("EU Peace Keeper Project")
    image_url = "https://i.ibb.co/gdw5kz4/PK2.jpg"
    #st.write("Welcome to the home page!")
    #img = Image.open(".\images\PK2.jpg")
    st.image(image_url)

def page1():
    st.title("Travel Authorisation Form")
    display_form()

def page2():
    st.title("Anomalies On Statistics")
    anomalies_page.show()

def page3():
    st.title("Anomaly Detection")
    anomaly_detector_page.show()


# Use a sidebar for navigation between pages
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("EU Peace Keeper Project", "Travel authorisation", "Anomalies On Statistics", "Anomaly Detection"))

# Display the selected page with the radio buttons
if page == "EU Peace Keeper Project":
    home_page()
elif page == "Travel authorisation":
    page1()
elif page == "Anomalies On Statistics":
    page2()
elif page == "Anomaly Detection":
    page3()

