#! /Users/varadarajanganesan/anaconda3/bin/python

# Importing libaries
import sys
import pandas as pd

# Getting the input file from command line
filename = sys.argv[-1]

# Obtaining the dataset and parsing the timestamp field to get other fields
dataset = pd.read_csv(filename, parse_dates = [1])
dataset['day_of_month'] = dataset['ts'].apply(lambda x:x.day)
dataset['day_of_week'] = dataset['ts'].apply(lambda x:x.weekday())
dataset['hour_of_visit'] = dataset['ts'].apply(lambda x:x.hour)
dataset.drop(['useragent','ts'],inplace = True, axis = 1)


# Function which checks if the user is active on weekday business hours
def is_user_active_on_weekday_business_hours(group):
    condition_check = 0
    for _,row in group.iterrows():
        if row['day_of_week'] >= 0 and row['day_of_week'] <= 4 and row['hour_of_visit'] >= 9 and row['hour_of_visit'] <= 18:
            condition_check += 1
    return condition_check > 0

# Function which checks if the user if highly mobile or not
def is_user_highly_mobile(group):
    return len(group['hashed_ip'].unique()) > 5

# Calculating the essential features
grouped_data = dataset.groupby('uuid')
df_derived_features = grouped_data.size().reset_index()
df_derived_features['highly_active'] = df_derived_features[0].apply(lambda x:x>2)
df_derived_features.drop(0,inplace = True, axis = 1)
df_derived_features['weekday_biz'] = grouped_data.apply(is_user_active_on_weekday_business_hours).reset_index()[0]
df_derived_features['highly_mobile'] = grouped_data.apply(is_user_highly_mobile).reset_index()[0]
df_derived_features.set_index('uuid',inplace=True)

# Writing the output to stdout
df_derived_features.to_csv(sys.stdout)