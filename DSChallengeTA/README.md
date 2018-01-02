Files included:
- report.ipynb: Ipython notebook with the detailed analysis
- solution.py: Python file which uses pyspark libraries to process the dataset faster
- solution_without_pyspark.py: Python file which uses pandas alone to process the dataset
-

Files not included:
- Considering the size of the .csv files, it has not been pushed into github. Please clone this repository and copy the logs.csv file
into the same folder before running the command to generate the output file. 

Requirements:
- Pandas
- Numpy
- Cufflinks
- Plotly
- Seaborn
- Pyspark (refer to https://medium.com/@GalarnykMichael/install-spark-on-mac-pyspark-453f395f240b for installation,
           not really necessary if you decide to use solution_without_pyspark.py)

Command to generate the output file:
- ./solution.py logs.csv > output.csv (generates the output file faster as it uses pyspark)
- ./solution_without_pyspark.py logs.csv > output.csv (generates the output file slower as it only uses pandas for processing)
