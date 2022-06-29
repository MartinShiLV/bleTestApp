import pandas as pd 
import numpy as np
# import matplotlib.pyplot as plt

df = pd.read_csv('test3.csv',header=0)
lap_times = np.array([])
# print(df.iloc[1,1])
for row in df.itertuples():
    if row.Protocol == 'ATT' and df.iloc[row[0]-1,4] == 'HCI_EVT':
        start_index = row[0]-4
        stop_index = row[0]
        if start_index>=0 :
            time_elapsed = df.iloc[stop_index,1] - df.iloc[start_index,1]
            lap_times=np.append(lap_times,time_elapsed)
        
# print(lap_times)
# x_axis = np.arange(len(lap_times))
# y_axis = lap_times
# plt.plot(x_axis,y_axis)
# plt.show()
df_out = pd.DataFrame(lap_times.T)
# print(df_out)
df_out.to_csv('test3_time.csv')


 


        



