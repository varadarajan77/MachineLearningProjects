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

from pyspark import SparkContext
from pyspark.sql import SparkSession, types
from pyspark.sql.functions import collect_list, udf, collect_set

sc = SparkContext()
spark = SparkSession(sc)
spark_DF = spark.createDataFrame(dataset)

def custom_spark_function(list_1, list_2):
    condition_satified = 0
    for day_of_week, hour_of_day in zip(list_1,list_2):
        if day_of_week >=0 and day_of_week <= 4 and hour_of_day >=9 and hour_of_day <=18:
            condition_satified += 1
    return condition_satified > 0

def custom_spark_function_2(hashed_ip):
    return len(hashed_ip) >= 5

sparkF = udf(custom_spark_function, types.BooleanType())
sparkF2 = udf(custom_spark_function_2, types.BooleanType())

sp_grouped_data = spark_DF.groupBy('uuid')
sp_aggregated_data = sp_grouped_data.agg(collect_list('day_of_week').alias('day_of_week'),
                                         collect_list('hour_of_visit').alias('hour_of_visit'),
                                         collect_set('hashed_ip').alias('hashed_ip'))\
                     .withColumn('weekday_biz', sparkF('day_of_week','hour_of_visit'))\
                     .withColumn('gloabally_active', sparkF2('hashed_ip'))

rdd_rows = sorted(sp_aggregated_data.drop('day_of_week','hour_of_visit','hashed_ip').collect())
df_new = spark.createDataFrame(rdd_rows).toPandas()

df_new.set_index('uuid',inplace=True)
print("Time Elapsed: ", time.time() - start_time)
df_new.to_csv(sys.stdout)
