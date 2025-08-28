import numpy as np
import pandas as pd
file_path = 'fitness_tracker_dataset.csv'

try:
    ft = pd.read_csv(file_path)
    print("data loaded sucessfuly")
  #  print(ft.head())
except FileNotFoundError:
    print(f"Error the file file {file_path} is not loaded ")
    df_raw = None

#Data Type Conversion:
#Convert the date column to a proper datetime object.
print(ft['date'])
ft['date']=pd.to_datetime(ft['date'])
print(ft['date'])
# Ensure numerical columns (steps, calories_burned, etc.)
# are of the correct data type (e.g., integer or float).
ft['steps']=pd.to_numeric(ft['steps'],errors="coerce")
ft['calories_burned']=pd.to_numeric(ft['calories_burned'],errors="coerce")

#Handling Missing Values:
print(ft.isnull().any())
print(ft['workout_type'].isnull().sum())
ft['workout_type']=ft['workout_type'].replace('Walking','UnKwhon')
print(ft[ft['workout_type']=='UnKwhon']['workout_type'])

#Outlier Detection: Identify and handle unrealistic values (e.g., a heart_rate_avg of 250 bpm or a sleep_hours of 20 hours).
#You can cap these values or replace them with a more reasonable value.
Q1=ft['sleep_hours'].quantile(0.25)
Q3=ft['sleep_hours'].quantile(0.75)
IQR=Q3-Q1
lower_bound=Q1-1.5*IQR
upper_bound=Q3+1.5*IQR
print(lower_bound)
print(upper_bound)
ft['sleep_hours']=np.where(ft['sleep_hours']> upper_bound,upper_bound,ft['sleep_hours'])
ft['sleep_hours']=np.where(ft['sleep_hours']< lower_bound,lower_bound,ft['sleep_hours'])
print(ft['sleep_hours'])
ft['heart_rate_avg']=ft['heart_rate_avg'].apply(lambda x:150 if x>150 else x)
print(ft['heart_rate_avg'])

#Categorical Data: Standardize workout_type, weather_conditions,
#location, and mood to handle inconsistencies (e.g., 'running' vs. 'Runnning').
standrized_dict={
    'Walking':'walk',
    'Cycling':'cyclic',
    'Swimming':'swim'
}
ft['workout_type']=ft['workout_type'].replace(standrized_dict)
print(ft['workout_type'])
#calories_per_step: calories_burned / steps.
ft['calories_per_step']=ft['calories_burned']/ft['steps']
print(ft['calories_per_step'])

#day_of_week: Extract the day of the week from the date column.
ft['day_of_week']=ft['date'].dt.day_name()
print(ft['day_of_week'])
#month: Extract the month from the date column.
ft['month']=ft['date'].dt.month
print(ft['month'])

print("---------------------------------------------")
output_file_path = 'cleaned_fitness_data.csv'
ft.to_csv(output_file_path, index=False)
print(f"\nTransformed data loaded to '{output_file_path}' successfully!")