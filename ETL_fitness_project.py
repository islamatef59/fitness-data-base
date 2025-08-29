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
df_fitness_final=df_fitness_resampled.ffill()
df_fitness_final.to_csv('cleaned_fitness_data2.csv',index=False)
print(f" the file {'cleaned_fitness_data2.csv'} is laodded sucessfuly")