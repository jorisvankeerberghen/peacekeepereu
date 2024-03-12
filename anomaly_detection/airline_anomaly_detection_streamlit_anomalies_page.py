import streamlit as st
import pandas as pd
import plotly.express as px
import time
import sys

def show():

    #Display the results of anomalies detection in a streamlit page
    #Multiple charts are displayed

    file_path = 'airline_anomalies_dataset.csv'
    df = pd.read_csv(file_path)

    #print(df.head())
    #sys.exit("Stopping")

    #Set up the title of the page
    st.header("Détection d'anomalies dans les vols de passagers sur 3 ans")
    st.markdown("<br>", unsafe_allow_html=True)

    #When the button is clicked
    if st.button("Détecter les anomalies"):

        progress_text = "Détection en cours..."
        progbar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.03)
            progbar.progress(percent_complete + 1, text=progress_text)
        
        time.sleep(1)
        progbar.empty()

        #After the spinning wheel, display the charts

        #Display the total number of suspects flights
        #Customizing CSS
        st.markdown("""
            <style>
            .big-font {
                font-size:26px !important;
                color: #FF4B4B;
                padding: 10px 20px; /* Top and bottom padding of 10px, left and right padding of 20px */
                background-color: rgba(233,233,233,1); /* Light gray background */
                border-radius: 15px; /* Optional: rounded corners */
            }
            .medium-font {
                font-size:20px !important;
                color: black;
            }
            .plot-container {
                border-radius: 15px;
                background-color: rgba(233,233,233,1);
                overflow: hidden;
            }
            </style>
            """, unsafe_allow_html=True)

        #After detecting anomalies, calculate gender distribution
        gender_count = df['Gender'].value_counts().reset_index()
        gender_count.columns = ['Gender', 'count']

        #Mapping original values to desired labels
        gender_labels = {'Male': 'Homme', 'Female': 'Femme'}
        gender_count['Gender'] = gender_count['Gender'].map(gender_labels)

        #Generate the pie chart
        gender_fig = px.pie(gender_count, values='count', names='Gender')

        #Update the chart with custom styles
        gender_fig.update_layout(
            title_text='Répartition par genre', #Chart title
            title_font_size=20,  #Size of the chart title
            paper_bgcolor='rgba(233,233,233,1)',
            margin=dict(l=30, r=30, t=60, b=30),
            legend_title_text='Genre',  #Legend title
            legend_title_font_size=18,  #Size of the legend title
            legend_font_size=18,  #Size of the legend labels,
            legend=dict(orientation="v", x=0, xanchor="left", y=0.2, yanchor="middle"),
            title={
                'text': 'Répartition par genre',
                'y':0.96,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
                },)

        gender_fig.update_traces(insidetextfont=dict(size=18))

        #Displaying the pie char and the information on number of anomalies side-by-side
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="big-font">Trouvé 723 vols de passagers atypiques!<br/><span class="medium-font">sur un total de 72418</span></p>', unsafe_allow_html=True)

        #Display the pie chart in the Streamlit page
        #gender_fig.update_layout(width=450, height=300)
        gender_fig.update_layout(width=800)
        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(gender_fig, use_container_width=True)

        #-------------------------------------------------------------------------------
        #Calculate passenger nationality distribution

        #Calculate counts of passengers by nationality
        nationality_counts = df['Nationality'].value_counts().reset_index()
        nationality_counts.columns = ['Nationality', 'Count']

        #Select the top 10 nationalities
        top_nationalities = nationality_counts.head(10)

        #Calculate the sum of the counts for "Others"
        others_sum = nationality_counts.iloc[10:]['Count'].sum()

        #Append an "Others" row if there are any other nationalities
        if others_sum > 0:
            top_nationalities.loc[len(top_nationalities)] = {'Nationality': 'Others', 'Count': others_sum}

        #Create a bar chart
        nationality_fig = px.bar(top_nationalities, x='Nationality', y='Count', color='Nationality')

        #Adjusting bar chart appearance
        nationality_fig.update_layout(xaxis_title="Top 10 des Nationalités",
                                      yaxis_title="Nombre de passagers",
                                      title_font_size=20,
                                      paper_bgcolor='rgba(233,233,233,1)',
                                      margin=dict(l=30, r=30, t=60, b=30),
                                      coloraxis_showscale=False,
                                      showlegend=False,
                                      title={
                                        'text': 'Répartition par nationalité',
                                        'y':0.96,
                                        'x':0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top'
                                        },)

        #Display the bar chart in the Streamlit app
        nationality_fig.update_layout(width=800)
        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(nationality_fig, use_container_width=True)

        #-------------------------------------------------------------------------------
        #Calculate country of arrival distribution

        #Calculate counts of passengers by country of arrival
        country_counts = df['Country Name'].value_counts().reset_index()
        country_counts.columns = ['Country Name', 'Count']

        #Select the top 10 nationalities
        top_countries = country_counts.head(10)

        #Calculate the sum of the counts for "Others"
        others_sum_countries = country_counts.iloc[10:]['Count'].sum()

        #Append an "Others" row if there are any other nationalities
        if others_sum_countries > 0:
            top_countries.loc[len(top_countries)] = {'Country Name': 'Others', 'Count': others_sum_countries}

        #Create a bar chart
        country_fig = px.bar(top_countries, x='Country Name', y='Count', color='Country Name')

        #Adjusting bar chart appearance
        country_fig.update_layout(xaxis_title="Top 10 des Pays d'Arrivée",
                                      yaxis_title="Nombre de passagers",
                                      title_font_size=20,
                                      paper_bgcolor='rgba(233,233,233,1)',
                                      margin=dict(l=30, r=30, t=60, b=30),
                                      coloraxis_showscale=False,
                                      showlegend=False,
                                      title={
                                        'text': "Répartition par pays d'arrivée",
                                        'y':0.96,
                                        'x':0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top'
                                        },)

        #Display the bar chart in the Streamlit app
        country_fig.update_layout(width=800)
        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(country_fig, use_container_width=True)


    

