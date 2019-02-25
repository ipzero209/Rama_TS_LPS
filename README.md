# Rama_TS_LPS


## About


This script will provide the following information:

1. High sample
2. Low sample
3. Simple average
4. Standard deviation
5. Number of samples with a value of zero
6. Percent of samples with a value of zero
7. Simple average of non-zero samples
8. Warning if average + 1SD is greater than the capacity of the model/mode the Panorama is running in




## Usage


To run the script ensure that it is executable then run as normal, passing the path to 
the tech support file as an argument. Example:



./rama_logs.py 20190204_1402_techsupport.tgz







## Requirements


1. Python 2.7
2. sys (part of the Python standard library)
3. math (part of the Python standard library)
4. tarfile (part of the Python standard library)







