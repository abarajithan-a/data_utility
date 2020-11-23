# Data Utility Scripts

This project consists of some of the most commonly used data utility functions within the data engineering space.

1. **InferSchema** - This script will infer the datatypes of a given data file and map them to the specified cloud platforms. You can either use the third party python library "tableschema" or the custom logic in "Datascan.py"  

	To invoke the custom library, call the function  
	`DataScan.run(<file_name>,<sample_size> , <conf_factor>)`  
	
	To use it as a standalone script,  
	`python ./inferschema/DetectSchema.py -fn <file_name> -ss <sample_size> -cf <conf_factor> -cs <cloud_service>`  
	    where   
	        -fn => source data file name  
	        -ss => sample size of the data to be used for inference  
	        -cf => confidence factor between 0 and 1. This is the level of tolerance for bad/missing/accurate data  
	        -cs => name of the supported cloud service. For now 'redshift' or 'bigquery'  

	**Performance Benchmark:**
	The below table shows the performance benchmark of "tableschema" Vs custom "DataScan". The benchmarking dataset has 12 columns.   
	All times are in *hours:minutes:seconds:microseconds*  
	| Sample Size of Data   | Confidence Factor | tableschema | DataScan   |
	|-----------------------|-------------------|-------------|------------|
	| 100                   | 0.8               | 0:00:00.41  | 0:00:00.22 |
	| 1000                  | 0.8               | 0:00:03.76  | 0:00:01.78 |
	| 10,000                | 0.8               | 0:00:37.57  | 0:00:16.99 |
	| 100,000               | 0.8               | 0:06:35.67  | 0:04:20.63 |
	| 1,000,000             | 0.8               | 1:11:45.20  | 0:31:23.23 |