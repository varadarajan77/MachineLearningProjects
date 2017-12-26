#! /Users/varadarajanganesan/anaconda3/bin/python

import sys
import pandas as pd
import numpy as np
import time

filename = sys.argv[-1]
start_time = time.time()
dataset = pd.read_csv(filename, parse_dates = [1])
dataset['day_of_month'] = dataset['ts'].apply(lambda x:x.day)
dataset['day_of_week'] = dataset['ts'].apply(lambda x:x.weekday())
dataset['hour_of_visit'] = dataset['ts'].apply(lambda x:x.hour)
dataset.drop(['useragent','ts'],inplace = True, axis = 1)


def number_of_unique_hashed_ips(group):
    return len(group['hashed_ip'].unique()) >= 5

def is_weekday_active(group):
    condition_check = 0
    for _,row in group.iterrows():
        if row['day_of_week'] >= 0 and row['day_of_week'] <= 4 and row['hour_of_visit'] >= 9 and row['hour_of_visit'] <= 18:
            condition_check += 1
    return condition_check > 0

grouped_data= dataset.groupby('uuid')
df_new = grouped_data.size().reset_index()
df_new.rename(columns = {0:'highly_active'},inplace = True)
df_new['weekday_biz'] = grouped_data.apply(is_weekday_active).reset_index()[0]
df_new['globally_active'] = grouped_data.apply(number_of_unique_hashed_ips).reset_index()[0]
df_new.set_index('uuid',inplace=True)

print("Time Elapsed: ", time.time() - start_time)

df_new.to_csv(sys.stdout)