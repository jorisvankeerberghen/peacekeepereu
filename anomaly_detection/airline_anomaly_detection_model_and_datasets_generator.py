import pandas as pd
import datetime
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from joblib import dump, load

file_path = 'airline_augmented_dataset.csv'
df = pd.read_csv(file_path)

df['Departure Date'] = pd.to_datetime(df['Departure Date'], format='%d/%m/%Y')
df['Departure Date Ordinal'] = df['Departure Date'].apply(lambda x: x.toordinal())

df.sort_values(by='Departure Date', inplace=True)

#print(df.shape)

last_date = df['Departure Date'].max()
cutoff_date = last_date - pd.Timedelta(days=1)

#The first DataFrame containing records up to but not including the last two days
df_train = df[df['Departure Date'] < cutoff_date]

#The second DataFrame containing just the records of the last two days
#The last 2 days of data will represent the fresh data
df_next_two_days = df[df['Departure Date'] >= cutoff_date]

#Save next 2 days dataset for further use
df_next_two_days.to_csv('airline_next_2_days_dataset.csv', index=False)

#Remove unnecessary columns for ML
df_ml = df_train.drop(['Airport Name', 'Country Name', 'First Name', 'Last Name', 'Departure Date'], axis=1)
df_ml_next = df_next_two_days.drop(['Airport Name', 'Country Name', 'First Name', 'Last Name', 'Departure Date'], axis=1)

#print(df_ml.columns)
#print(df_ml.shape)

#print(df_ml_next.columns)
#print(df_ml_next.shape)

#-------------------------------------------------------------
#Anomalies detection model

#Encode categorical variables
label_encoders = {}
for column in ['Gender', 'Nationality', 'Arrival Airport', 'Airport Country Code']:
    le = LabelEncoder()
    df_ml[column] = le.fit_transform(df_ml[column])
    label_encoders[column] = le

#Initialize the Isolation Forest model
model = IsolationForest(n_estimators=100, contamination=0.01)

X = df_ml.drop(['Passenger ID'], axis=1) #Exclude the Passenger ID from features

#Fit the model
model.fit(X)

#Predict anomalies (-1 for anomalies, 1 for normal)
df_ml['anomaly'] = model.predict(X)

#Filter out the anomalies
anomalies_train = df_ml[df_ml['anomaly'] == -1]

#print("Anomalies detected:")
#print(anomalies_train.head())

#Save the model to disk
dump(model, 'model_airline_anomalies_detection.joblib')

#Merge the anomalies dataframe with df_train dataframe to find matching rows based on 'Passenger ID' and 'Departure Date Ordinal'
#The resulting matched_rows_train dataframe contains only anormal flights with the full readable information
df_unique_anomalies_train = anomalies_train[['Passenger ID', 'Departure Date Ordinal']].drop_duplicates()
matched_rows_train = pd.merge(df_train, df_unique_anomalies_train, on=['Passenger ID', 'Departure Date Ordinal'], how='inner')

#print("Anomalies detected in training dataset:")
#print(matched_rows_train.head())
#print(matched_rows_train.shape)

#Save the dataset containing the anomalies detected in the training dataset
matched_rows_train.to_csv('airline_anomalies_dataset.csv', index=False)
