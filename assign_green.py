import time as t
import trial
import json
import numpy as np
import csv
import pandas as pd
cnts=1
flags=[0,0,0,0]
times=0
def get_s(time, cnt):
    print(time)
    trial.run_main(time, cnt)
    s = []
    f = open("buffer.json", "r")
    obj = json.load(f)
    for i in range(4):
        s.append(obj[str(i)])
    f.close()
    print(s)
    return s


def get_time(vc):
    if vc >= 0 and vc < 5:
        return 5
    elif vc >= 5 and vc < 15:
        return 6
    elif vc >= 15 and vc < 30:
        return 8
    else:
        return 9


def assign_green(flag, cnt, time):
    global flags,cnts,times
    s = get_s(time, cnt)
    df = pd.read_csv("details.csv")
    for i in range(4):
        imagePath="{cnts}_capture_side_{pids}.jpg".format(cnts=str(cnt),pids=str(i))
        df.loc[i,"cnt"]=cnt
        df.loc[i,"vehicles"]=s[i]
        df.loc[i,"image"]=imagePath
        
    for i in range(0, 4):
        if flag[i] != 0:
            s[i] = 0
    max_temp = s[0]
    for i in range(0, 4):
        if s[i] >= max_temp:
            max_temp = s[i]
    for i in range(0, 4):
        if s[i] == max_temp:
            flag[i] = 1
            max_s = i
            max_s_value = s[i]
            break

    w_time = get_time(max_s_value)
    for i in range(4):
        df.loc[i,"flag"]=flag[i]
        if i==max_s:
            df.loc[i,"greentime"]=w_time
        else:
            df.loc[i,"greentime"]=0
    df.to_csv("details.csv", index=False)
    
    print('s'+str(max_s))
    print('vehicle count '+str(max_s_value))
    print('green time ' + str(w_time))
    print('********')

    sleep_time = w_time-5

    t.sleep(sleep_time)

    time = time+w_time
    # trial.run_main(time)
    # s = get_s()
    if (cnt % 4) == 0:
        flag = [0, 0, 0, 0]
        print("\n\n")
        print("DONE")
        print("\n\n")
    cnt = cnt + 1
    cnts=cnt
    flags=flag
    times=time
    


if __name__ == "__main__":
    while True:
        print(cnts)
        assign_green(flags, cnts, times)

    # flag = [0, 0, 0, 0]
    # s = [12, 15, 20, 5]
    # cnt = 0
    # assign_green(s, flag, cnt)
    # flag = [0, 0, 0, 0]
    # s = [3, 8, 12, 2]
    # cnt = 0
    # assign_green(s, flag, cnt)
