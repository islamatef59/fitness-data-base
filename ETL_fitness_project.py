import pandas as pd
#Exract data from cleaned_fitness_data file
try:
   df_fitness=pd.read_csv('cleaned_fitness_data.csv')
   df_fitness['date'] =pd.to_datetime(df_fitness['date'])
   df_fitness.set_index('date',inplace=True)
   print("data loaded sucessfuly")
   print(df_fitness.head())
except FileNotFoundError:
   print(f"Erorr the file {'cleaned_fitness_data.csv'} not loaded")

#Transform data(clean and organize it) of cleaned_fitness_data file
df_fitness.index=pd.to_datetime(df_fitness.index)
columns_to_resample=['steps','calories_burned','distance_km','active_minutes',
'sleep_hours','heart_rate_avg','calories_per_step']
df_fitness_resample=df_fitness[columns_to_resample]
dic_resample_rules={
   'steps':'sum',
   'calories_burned':'sum',
   'distance_km':'sum',
   'active_minutes':'sum',
   'sleep_hours':'mean',
   'heart_rate_avg':'mean',
   'calories_per_step':'mean',
}
df_fitness_resampled=df_fitness.resample('D').agg(dic_resample_rules)
#df_fitness_final=df_fitness_resampled.interpolate(method='linear')
#fill missing data with last  value in the colimn
df_fitness_final=df_fitness_resampled.ffill()


#Lag Features: Create new columns with values from previous days
df_fitness_final['steps_lag_1']=df_fitness_final['steps'].shift(1)
df_fitness_final['calories_burned_lag_1']=df_fitness_final['calories_burned'].shift(1)


#Rolling Statistics
# Create a 7-day rolling average for steps
df_fitness_final['steps_avregae_7days']=df_fitness_final['steps'].rolling(window=7).mean()
df_fitness_final['calories_burned_30days_sum']=df_fitness_final['calories_burned'].rolling(window=30).sum()

#get days of week
df_fitness_final['day_of_week'] = df_fitness_final.index.dayofweek

#get days of month
df_fitness_final['day_of_month'] = df_fitness_final.index.day

#know is the day is weekend or weekdays
df_fitness_final['is_weekend'] = df_fitness_final['day_of_week'].isin([5, 6]).astype(int)

#get month as number
df_fitness_final['month'] = df_fitness_final.index.month

#know the  quarter of  the day
df_fitness_final['quarter'] = df_fitness_final.index.quarter

#load new cleaned data to the file
df_fitness_final.to_csv('cleaned_fitness_data2.csv',index=False)
print(f" the file {'cleaned_fitness_data2.csv'} is laodded sucessfuly")


