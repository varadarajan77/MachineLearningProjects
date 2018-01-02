Requirements:
- Pandas
- Numpy
- Cufflinks
- Plotly
- Seaborn
- Pyspark (refer to https://medium.com/@GalarnykMichael/install-spark-on-mac-pyspark-453f395f240b for installation,
           not really necessary if you decide to use solution_without_pyspark.py)
           
Files included:
- report.ipynb: ipython notebook with the detailed analysis
- solution.py: python file which uses pyspark libraries to process the dataset faster
- solution_without_pyspark.py: python file which uses pandas alone to process the dataset

Files not included:
- Considering the size of the *.csv files, they have not been pushed into github. Please clone this repository and copy the logs.csv file
into the same folder before running the command to generate the output file. 

Command to generate the output file:
- ./solution.py logs.csv > output.csv (generates the output file faster as it uses pyspark)
- ./solution_without_pyspark.py logs.csv > output.csv (generates the output file slower as it only uses pandas for processing)
