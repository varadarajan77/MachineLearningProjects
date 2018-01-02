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

# Importing all the necessary pyspark libraries
from pyspark import SparkContext
from pyspark.sql import SparkSession, types, functions
from pyspark.sql.functions import collect_list, udf, collect_set

# Initialising the spark context and the dataframe
sc = SparkContext()
spark = SparkSession(sc)
spark_df = spark.createDataFrame(dataset)


# Function which checks is user is highly active
def is_user_high_active_spark_function(count_of_records):
    return count_of_records > 2

# Function which checks if the user is active on weekday business hours
def is_user_active_on_weekday_business_hours_spark_function(list_1, list_2):
    condition_satified = 0
    for day_of_week, hour_of_day in zip(list_1,list_2):
        if day_of_week >=0 and day_of_week <= 4 and hour_of_day >=9 and hour_of_day <=18:
            condition_satified += 1
    return condition_satified > 0

# Function which checks if the user if highly mobile or not
def is_user_highly_mobile_spark_function(hashed_ip):
    return len(hashed_ip) > 5

# Initialising the different spark user defined functions
user_defined_function_1 = udf(is_user_high_active_spark_function, types.BooleanType())
user_defined_function_2 = udf(is_user_active_on_weekday_business_hours_spark_function, types.BooleanType())
user_defined_function_3 = udf(is_user_highly_mobile_spark_function, types.BooleanType())

spark_grouped_data = spark_df.groupBy('uuid')
spark_aggregated_data = spark_grouped_data.agg(functions.count(functions.lit(1)).alias('number_of_visits'),
                                         collect_list('day_of_week').alias('day_of_week'),
                                         collect_list('hour_of_visit').alias('hour_of_visit'),
                                         collect_set('hashed_ip').alias('hashed_ip'))\
                     .withColumn('highly_active', user_defined_function_1('number_of_visits'))\
                     .withColumn('weekday_biz', user_defined_function_2('day_of_week','hour_of_visit'))\
                     .withColumn('highly_mobile', user_defined_function_3('hashed_ip'))

rdd_rows = sorted(spark_aggregated_data.drop('day_of_week','hour_of_visit','hashed_ip','number_of_visits').collect())
df_derived_features_using_spark = spark.createDataFrame(rdd_rows).toPandas()
df_derived_features_using_spark.set_index('uuid',inplace=True)

# Writing the output to stdout
df_derived_features_using_spark.to_csv(sys.stdout)
