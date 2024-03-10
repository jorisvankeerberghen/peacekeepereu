import streamlit as st
import pandas as pd
import joblib
import tempfile
import requests
import tensorflow as tf
from tensorflow.keras.models import load_model

def display_form():
    with st.form("form1"):
        name = st.text_input("Enter your name:")
        gender = st.selectbox('Gender:',('Male', 'Female'))
        nationalities = get_nationalities()
        nationality = st.selectbox ('Nationality:', nationalities)
        schengen_countries = get_schengen_countries()
        country = st.selectbox('Travel to:', schengen_countries)
        user_age = st.number_input("Enter your age", min_value=0, max_value=100, step=1)
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.header("Results")
        #st.write(f"Hello {name}, you are a {gender}, from {nationality}, travelling to {country} and {user_age} years old.")
        authorisation, risk = calculate_authorisation(gender, nationality, country,user_age)
        if authorisation:
            st.success(f"Hello {name},\n"
                       "You are authorised to travel to the Schengen Zone.\n"
                       f"Your risk profile is {risk}%")
        else:
            st.error(f"""Hello {name},
                     Unfortunately your access to the Schengen Zone has been REFUSED! 
                     Your risk profile is {risk}%""")
            
        
        

def calculate_authorisation(gender, nationality, country, user_age):
    df = pd.read_csv("./prediction_model/empty_travel_record.csv")
    df = df.drop([1, 2])
    df = df.drop(columns=['Unnamed: 0'])
    
    with tempfile.NamedTemporaryFile(delete=False) as model_temp_file, tempfile.NamedTemporaryFile(delete=False) as scaler_temp_file:
        download_file('https://github.com/jorisvankeerberghen/peacekeepereu/raw/main/prediction_model/model_v4.h5', model_temp_file.name)
        download_file('https://github.com/jorisvankeerberghen/peacekeepereu/raw/main/prediction_model/scaler_v3.joblib', scaler_temp_file.name)

        loaded_model = load_model(model_temp_file.name)
        scaler = joblib.load(scaler_temp_file.name)
    #loaded_model = load_model("./prediction_model/model_v4.h5")
    #scaler = joblib.load("./prediction_model/scaler_v3.joblib")
    
    gender_t = transform_gender(gender)
    df.iloc[0, df.columns.get_loc(gender_t)] = 1
    
    nationality_t = transform_nationality(nationality)
    df.iloc[0, df.columns.get_loc(nationality_t)] = 1

    country_t = transform_country(country)
    df.iloc[0, df.columns.get_loc(country_t)] = 1

    df.iloc[0, df.columns.get_loc('Age')] = user_age

    scaler_df = scaler.transform(df)
    prediction = loaded_model.predict(scaler_df)
    risk_value = (1-prediction)*100
    risk_perc = "{:.2f}".format(risk_value[0][0])
    
    if risk_value[0] < 6:
        return True, risk_perc
    else:
        return False, risk_perc

    #st.write(df.head())
    #st.write(f"{prediction}")
    

def transform_gender(text):
    prefix = "Gender_"
    return prefix + text.strip()

def transform_nationality(text):
    prefix ="Nationality_"
    return prefix + text.strip()

def transform_country(text):
    prefix = "Airport Country Code_"
    country_code = get_schengen_code(text)
    return prefix + country_code.strip()

def download_file(url, local_path):
    response = requests.get(url)
    with open(local_path, 'wb') as f:
        f.write(response.content)

def get_schengen_code(text):
    schengen_zone = {
        "Austria": "AT",
        "Belgium": "BE",
      "Czech Republic": "CZ",
      "Denmark": "DK",
      "Estonia": "EE",
      "Finland": "FI",
      "France": "FR",
      "Germany": "DE",
      "Greece": "GR",
      "Hungary": "HU",
      "Iceland": "IS",
      "Italy": "IT",
      "Latvia": "LV",
      "Liechtenstein": "LI",
      "Lithuania": "LT",
      "Luxembourg": "LU",
      "Malta": "MT",
      "Netherlands": "NL",
      "Norway": "NO",
      "Poland": "PL",
      "Portugal": "PT",
      "Slovakia": "SK",
      "Slovenia": "SI",
      "Spain": "ES",
      "Sweden": "SE",
      "Switzerland": "CH"
    }

    if text in schengen_zone:
        return schengen_zone[text]
    else:
        return None

def get_schengen_countries():
    return ['Austria', 'Belgium', 'Switzerland', 'Czech Republic', 'Germany',
            'Denmark', 'Estonia', 'Spain', 'Finland', 'France', 'Greece',
            'Hungary', 'Iceland', 'Italy', 'Lithuania', 'Luxembourg', 'Latvia',
            'Malta', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Sweden',
            'Slovenia', 'Slovakia']

def get_nationalities():
    return['Afghanistan', 'Aland Islands', 'Albania' ,'American Samoa', 'Andorra'
        'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia',
        'Austria', 'Azerbaijan', 'Bahrain' ,'Bangladesh' ,'Barbados', 'Belarus',
        'Belgium', 'Belize', 'Benin', 'Bolivia', 'Bonaire, Saint Eustatius and Saba ',
        'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso',
        'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic',
        'Chad', 'Chile', 'China', 'Christmas Island', 'Colombia', 'Comoros',
        'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic',
        'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica',
        'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea',
        'Eritrea', 'Estonia', 'Ethiopia', 'Faroe Islands', 'Finland', 'France',
        'French Guiana', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany',
        'Ghana', 'Greece', 'Greenland', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea',
        'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland',
        'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast',
        'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo',
        'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Liberia', 'Libya',
        'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia',
        'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania',
        'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Mongolia', 'Montserrat',
        'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands',
        'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea',
        'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau',
        'Palestinian Territory', 'Panama', 'Paraguay', 'Peru', 'Philippines',
        'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Republic of the Congo',
        'Reunion', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia',
        'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia', 'Sierra Leone', 'Slovenia',
        'Somalia', 'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka',
        'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan',
        'Tanzania', 'Thailand', 'Togo', 'Tunisia', 'Turkmenistan' ,'Uganda', 'Ukraine',
        'United Arab Emirates', 'United Kingdom', 'United States' ,'Uruguay',
        'Uzbekistan' ,'Vanuatu' ,'Venezuela' ,'Vietnam' ,'Yemen' ,'Zambia', 'Zimbabwe']
    