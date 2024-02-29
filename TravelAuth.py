import streamlit as st

def display_form():
    with st.form("form1"):
        name = st.text_input("Enter your name")
        gender = st.selectbox('Gender:',('Male', 'Female'))
        nationality = st.selectbox ('Nationality:',('Afghanistan', 'Aland Islands', 'Albania' ,'American Samoa', 'Andorra'
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
 'Uzbekistan' ,'Vanuatu' ,'Venezuela' ,'Vietnam' ,'Yemen' ,'Zambia', 'Zimbabwe'))
        country = st.selectbox('Travel to:',('AT', 'BE', 'CH', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR', 'HU', 'IS', 'IT',
 'LT', 'LU', 'LV', 'MT', 'NL', 'NO', 'PL', 'PT', 'SE', 'SI', 'SK'))
        user_age = st.number_input("Enter your age", min_value=0, max_value=100, step=1)
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.write(f"Hello {name}, you are a {gender}, from {nationality}, travelling to {country} and {user_age} years old.")
        st.write(f"Unfortunately your entry to Schengen Zone is REFUSED")

def initiate_model():
    return "Calucation done"
    