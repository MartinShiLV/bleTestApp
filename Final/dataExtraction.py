import csv
from time import time
import pandas as pd 
import numpy as np
from os.path import exists

BaseInFileName = '/home/shared/LonganVision/bleTestApp/Final/HUHF-IOT-TEST_005-RAW/HUHF-IOT-TEST_005-RAW_COND'
BaseOutFileName = '/home/shared/LonganVision/bleTestApp/Final/HUHF-IOT-TEST_005-CSV_POST_PROC/HUHF-IOT-TEST_005-CSV_COND'

def main():
    for conditionNum in range(1,9):
        CondInFileName = BaseInFileName + str(conditionNum) + '/cond' + str(conditionNum) + '_loc'
        CondOutFileName = BaseOutFileName + str(conditionNum) + '/cond' + str(conditionNum) + '_loc'
        for fileNum in range (0,10):
            InFileName = CondInFileName + str(fileNum) + '.csv'
            OutFileName = CondOutFileName + str(fileNum) + '_processed.xlsx'
            fileNum = fileNum + 1
            if not exists(InFileName):
                print(InFileName)
                break
            df = pd.read_csv(InFileName,header=0)
            lap_times = np.array([])
            time_avg = np.array([])
            packetLossRate = np.array([])
            start_index = -1
            stop_index = 0
            total_packet_num = 0
            packet_loss_count = 0
            packet_loss_track = 0

            for row in df.itertuples():
                if 'Sent' in row.Info:
                    if start_index == -1:
                        start_index = row[0]
                    else:
                        if packet_loss_track == 0:
                            packet_loss_count += 1
                            packet_loss_track = 1
                        continue
                        
                if 'Complete' in row.Info and 'Disconnect' not in row.Info:
                    stop_index = row[0]
                    total_packet_num += 1
                    packet_loss_track = 0
                    if start_index>=0 :
                        time_elapsed = df.iloc[stop_index+1,1] - df.iloc[start_index+1,1]
                        lap_times=np.append(lap_times,time_elapsed)
                        start_index = -1
                
            packetLossRate = np.append(packetLossRate, packet_loss_count*1.0/total_packet_num)
            time_avg = np.append(time_avg, np.mean(lap_times))

            print('packet loss rate')
            print(packetLossRate)

            print('mean delay time from command to actual read')
            print(time_avg)

            writer = pd.ExcelWriter(OutFileName, engine='xlsxwriter')
            pd.DataFrame(lap_times).to_excel(writer, sheet_name='latency')
            pd.DataFrame(time_avg).to_excel(writer, sheet_name='latency average')
            pd.DataFrame(packetLossRate).to_excel(writer, sheet_name='packetloss')
            writer.save()


if __name__ == "__main__":
    main()