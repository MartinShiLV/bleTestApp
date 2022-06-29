import csv
from time import time
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

macAddress = "78:E3:6D:0A:7E:16"

def main():
    output = open('rssi.csv', 'w')
    writer = csv.writer(output)
    df = pd.read_csv('test3.csv',header=0)
    lap_times = np.array([])
    rssiValue = np.array([])
    dataCombine = np.array([])
    rssiSum = 0
    rssiNum = 0
    time_elapsed_sum = 0
    time_elapsed_num = 0

    with open('scan4.txt') as f:
        lines = f.readlines() # list containing lines of file
        columns = [] # To store column names

        for line in lines:
            line = line.strip() # remove leading/trailing white spaces
            if (line.find('CHG') != -1 and line.find(macAddress) != -1 and line.find('RSSI') != -1):
                rssi = int(line[(line.find('RSSI')+6):])
                rssiSum = rssiSum + rssi
                rssiNum +=1
                rssiValue=np.append(rssiValue,rssi)
    rssiAvg = rssiSum/rssiNum
    rssiValue=np.append(rssiValue,rssiAvg)
    
    for row in df.itertuples():
        if row.Protocol == 'ATT' and df.iloc[row[0]-1,4] == 'HCI_EVT':
            start_index = row[0]-4
            stop_index = row[0]
            if start_index>=0 :
                time_elapsed = df.iloc[stop_index,1] - df.iloc[start_index,1]
                time_elapsed_sum = time_elapsed_sum + time_elapsed
                time_elapsed_num += 1
                lap_times=np.append(lap_times,time_elapsed)

    time_elapsed_avg = time_elapsed_sum / time_elapsed_num
    lap_times=np.append(lap_times,time_elapsed_avg) 

    #dataCombine = np.vstack((rssiValue, lap_times)).T
    dataCombine = np.concatenate((rssiValue, lap_times), axis = 0)

    print("RSSI Avg: ", rssiAvg)
    print("time elapsed avg: ", time_elapsed_avg)
    df_out = pd.DataFrame(dataCombine.T)
    df_out.to_csv('test3_time.csv')
    #writer.writerow(rssiValue)
    f.close()
    output.close()

    writer = pd.ExcelWriter('test3_outut.xlsx', engine='xlsxwriter')
    pd.DataFrame(lap_times).to_excel(writer, sheet_name='time_elapsed')
    pd.DataFrame(rssiValue).to_excel(writer, sheet_name='RSSI')
    writer.save()
    # writer.close()
    
    

if __name__ == "__main__":
    main()


'''
 for i in range(0, len(line)):
                if (line[i] == 'C' and line[i+1] == 'H' and line[i+2] == 'G'):
                    read = True'''