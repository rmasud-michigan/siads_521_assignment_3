# siads_521_assignment_3
SIADS 521 Data Visualization Assignment 3 

## Overview
This repo is intended to demonstrate real example of data visualizations with Python.
The various plots will analyze the City of Chicago crash data. 
The analysis will use techniques to extract, transform and load the data.

# Required Libraris:
* [Pandas](https://pypi.org/project/pandas/)
* [MatPlotLib](https://pypi.org/project/matplotlib/)
* [Seaborn](https://pypi.org/project/seaborn/)
* [Numpy](https://pypi.org/project/numpy/)
* [SciPy](https://pypi.org/project/scipy/)



```
# run the following command in your terminal to install the required libraries into your environment
pip install pandas numpy matplotlib scipy seaborn
```

## Source Data
### City of Chicago
* https://data.cityofchicago.org/api/views/85ca-t3if/rows.csv?fourfour=85ca-t3if&cacheBust=1742398767&date=20250319&accessType=DOWNLOAD

Fields used in this repo

| Field     | Type | Description | 
|-----------|------|-------------|
| ALIGNMENT | Text |  Street alignment at crash location, as determined by reporting officer           |
| BEAT_OF_OCCURRENCE | Text |  Chicago Police Department Beat ID. Boundaries available at https://data.cityofchicago.org/d/aerh-rz74           |


