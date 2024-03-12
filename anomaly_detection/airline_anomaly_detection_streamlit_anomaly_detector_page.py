import streamlit as st
import pandas as pd
import time
import sys
import os

from joblib import load
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

#Get the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

def show():

    #Load trained anomaly detection model
    model = load(os.path.join(script_dir, 'model_airline_anomalies_detection.joblib'))

    #Load datasets
    file_path_anomalies = os.path.join(script_dir, 'airline_anomalies_dataset.csv')
    df_anomalies = pd.read_csv(file_path_anomalies)

    file_path_next = os.path.join(script_dir, 'airline_next_2_days_dataset.csv')
    df_next = pd.read_csv(file_path_next)
    df_ml_next = df_next.drop(['Airport Name', 'Country Name', 'First Name', 'Last Name', 'Departure Date'], axis=1)

    #Display tabs
    tab1, tab2 = st.tabs(["To check", "Atypical passengers"])

    with tab1:

        st.subheader("To check in the next 2 days")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Detect anomalies"):

            progress_text = "Detecting..."
            progbar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.01)
                progbar.progress(percent_complete + 1, text=progress_text)
                
            time.sleep(1)
            progbar.empty()

            #Encode categorical variables
            label_encoders = {}
            for column in ['Gender', 'Nationality', 'Arrival Airport', 'Airport Country Code']:
                le = LabelEncoder()
                df_ml_next[column] = le.fit_transform(df_ml_next[column])
                label_encoders[column] = le

            Y = df_ml_next.drop(['Passenger ID'], axis=1) #Exclude the Passenger ID from features

            #Predict anomalies (-1 for anomalies, 1 for normal) in the next 2 days dataset
            df_ml_next['anomaly'] = model.predict(Y)

            #Filter out the anomalies
            anomalies = df_ml_next[df_ml_next['anomaly'] == -1]

            #Get the subset of initial dataframe that matches the anomalies detected in the training dataframe
            #Merge this subset with df to find matching rows based on 'Passenger ID' and 'Departure Date Ordinal'
            df_unique_anomalies = anomalies[['Passenger ID', 'Departure Date Ordinal']].drop_duplicates()
            matched_rows = pd.merge(df_next, df_unique_anomalies, on=['Passenger ID', 'Departure Date Ordinal'], how='inner')
            matched_rows = matched_rows.drop(['Passenger ID', 'Airport Country Code', 'Flight Count', 'Departure Date Ordinal'], axis=1)
            matched_rows.sort_values(by=['Departure Date', 'Country Name', 'Arrival Airport', 'Last Name', 'First Name'], inplace=True)
            matched_rows = matched_rows.reset_index(drop=True)

            # Desired order of columns
            new_order = ['Departure Date', 'Country Name', 'Arrival Airport', 'Last Name', 'First Name', 'Gender', 'Age', 'Nationality', 'Airport Name']
            #Reorder columns
            df_reordered = matched_rows[new_order]

            #Display the results table
            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(df_reordered)
 

    with tab2:

        st.subheader("Main atypical passengers")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Compiling the results"):

            progress_text = "Compiling..."
            progbar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.01)
                progbar.progress(percent_complete + 1, text=progress_text)
            
            time.sleep(1)
            progbar.empty()

            #Find top 4 suspicious passengers
            top_passengers = df_anomalies['Passenger ID'].value_counts().head(4)
            top_passengers = top_passengers.reset_index()
            top_passengers.columns = ['Passenger ID', 'Count Atypique Flights']

            final_results = pd.DataFrame(columns=['Passenger ID', 'Count Atypique Flights', 'Last Name', 'First Name', 'Nationality'])

            for index, row in top_passengers.iterrows():
                prow = df_anomalies[df_anomalies['Passenger ID'] == row['Passenger ID']].iloc[0]

                if not prow.empty:
                    final_results.loc[len(final_results)] = [row['Passenger ID'], row['Count Atypique Flights'], prow['Last Name'], prow['First Name'], prow['Nationality']]

            #Add Joachim as top suspicious guy for the fun of it
            final_results.loc[len(final_results)] = ['xxx000', 41, 'Massias', 'Joachim', 'France']
            
            final_results.sort_values(by=['Count Atypique Flights'], ascending=False, inplace=True)
            final_results = final_results.reset_index(drop=True)

            #Function to apply color styling to the cells of Joachim
            def colorize(val):
                if val == 'Joachim' or val == 'Massias' or val == 41:
                    color = 'rgba(255,204,203,1)'
                else:
                    color = 'white'

                return f'background-color: {color}'

            #Apply the styling function to the DataFrame and display it
            styled_final_results = final_results.style.applymap(colorize)
            st.markdown("<br>", unsafe_allow_html=True)
            st.table(styled_final_results)

