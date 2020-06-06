import pandas as pd
import os
from pathlib import Path

all_sensor_data = pd.DataFrame()
files = [file for file in os.listdir(sensor_folder) if not file.startswith('.')] # Ignore hidden files
sensor_folder = Path('~/projects/Visualizer-for-an-energy-aware-scheduler/Visualizer_Code_16321461/generated_data')
print(sensor_folder)
for file in files:
    df = pd.read_csv(sensor_folder / file)
    all_sensor_data = pd.concat([all_sensor_data, df]) 
all_sensor_data['time_of_transmission'] = all_sensor_data['time_of_transmission'].astype('float64') 
all_sensor_data['time_as_date'] = np.array(all_sensor_data["time_of_transmission"]).astype("datetime64[s]") 
all_sensor_data['time_as_date']  = all_sensor_data['time_as_date'] + timedelta(days=12476)   
all_sensor_data = all_sensor_data.sort_values(by = 'time_as_date', ascending = True)
print(all_sensor_data)