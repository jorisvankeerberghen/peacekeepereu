import pandas as pd
from datetime import datetime, timedelta
import random
random.seed(42)

file_path = 'airline_dataset.csv'
df = pd.read_csv(file_path)

#Remove rows with empty values
df = df.dropna()

#Change dates format
df['Departure Date'] = pd.to_datetime(df['Departure Date'], format='mixed').dt.strftime('%d/%m/%Y')

#Display the first few rows of the dataframe and columns
#print(df.head())
#print(df.columns)

#Keep only Schengen countries
schengen_countries_codes = ['AT', 'BE', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IS', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'NO', 'PL', 'PT', 'SK', 'SI', 'ES', 'SE', 'CH', 'LI']
df = df[df['Airport Country Code'].isin(schengen_countries_codes)]

#Remove unnecessary columns
df = df.drop(['Airport Continent', 'Continents', 'Pilot Name', 'Flight Status'], axis=1)
#print(f"Shape after transformation: {df.shape}")

df_airports = df.loc[:, ['Arrival Airport', 'Airport Name', 'Airport Country Code', 'Country Name']].copy()
df_airports = df_airports.drop_duplicates(subset='Arrival Airport')
#print(f"Shape df_airports: {df_airports.shape}")

#---------------------------------------------------------------------------
#Generate the distribution of flights for the passengers

#Normalize sequence of numbers (must add up to total)
def normalize_sequence(sequence, total):
    sum_sequence = sum(sequence)
    return [x / sum_sequence * total for x in sequence]

#Generate a sequence of probabilities for having flown from 1 to 50 times during the dataset period
def generate_random_flights_distribution():
  percentages_main_nb_flights = [0.42, 0.21, 0.08]
  num_elements = 47

  #print(total_sum)

  random_sequence = [random.random() for _ in range(num_elements)]
  normalized_sequence = normalize_sequence(random_sequence, 1 - sum(percentages_main_nb_flights))

  return percentages_main_nb_flights + normalized_sequence

import numpy as np

#Generate number of flights done by passengers based on defined distribution

probabilities_sequence = generate_random_flights_distribution()
#print(sum(probabilities_sequence))
#print(probabilities_sequence)

#Define the outcomes and their probabilities
outcomes = np.array([i for i in range(1, 51)])
probabilities = np.array(probabilities_sequence)

#Generate  random numbers of flights from this distribution
custom_distribution = np.random.choice(outcomes, size=len(df), p=probabilities)
#print(custom_distribution)

df['Flight Count'] = custom_distribution
df['Dates'] = np.nan

#print(df.columns)
#print(df.head())

#---------------------------------------------------------------------------
#Generators of random dates according to distribution

start_date = datetime(2021, 1, 1)
end_date = datetime(2023, 12, 31)

#Generate random unique dates

def generate_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date

def generate_dates(nb_dates, start_date, end_date):
  unique_dates = set()

  while len(unique_dates) < nb_dates:
    random_date = generate_random_date(start_date, end_date)
    unique_dates.add(random_date.strftime('%d/%m/%Y'))

  return list(unique_dates)

#Generate an airport code based on pre-defined distribution
def generate_airport(original_airport, airports):
  same_airport_prob = 0.6 #Harcoded choice
  airports_list = airports['Arrival Airport'].tolist()

  if random.random() > same_airport_prob:
    return random.choice(airports_list)
  else:
    return original_airport

#---------------------------------------------------------------------------
#Generate new rows in the dataframe for additional flights done by passengers
#Save final augemented dataset

df.sort_values(by='Passenger ID', ascending=True, inplace=True)
df = df.reset_index(drop=True)

df_final = df.copy()
df_final = df_final.iloc[0:0] #empty the dataframe

for index, row in df.iterrows():
  #print(f"index: {index}")
  flight_dates = generate_dates(row['Flight Count'], start_date, end_date)

  for fdate in flight_dates:
    new_row = df.iloc[index].copy()
    new_row['Departure Date'] = fdate
    new_row['Arrival Airport'] = generate_airport(new_row['Arrival Airport'], df_airports)

    df_airports_filtered = df_airports[df_airports['Arrival Airport'] == new_row['Arrival Airport']]
    new_row['Airport Name'] = df_airports_filtered['Airport Name'].iloc[0]
    new_row['Airport Country Code'] = df_airports_filtered['Airport Country Code'].iloc[0]
    new_row['Country Name'] = df_airports_filtered['Country Name'].iloc[0]

    df_final.loc[len(df_final)] = new_row
    #print(new_row)

df_final = df_final.drop(['Dates'], axis=1)
df_final.sort_values(by='Passenger ID', ascending=True, inplace=True)
df_final = df_final.reset_index(drop=True)

#print(df_final.head())

df.to_csv('filename.csv', index=False)
df_final.to_csv('airline_augmented_dataset.csv', index=False)

