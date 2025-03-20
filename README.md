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

| Column Name                   | Data Type      |
|-------------------------------|----------------|
| CRASH_RECORD_ID               | String         |
| CRASH_DATE_EST_I              | String         |
| CRASH_DATE                    | Date Timestamp |
| POSTED_SPEED_LIMIT            | Number         |
| TRAFFIC_CONTROL_DEVICE        | String         |
| DEVICE_CONDITION              | String         |
| WEATHER_CONDITION             | String         |
| LIGHTING_CONDITION            | String         |
| FIRST_CRASH_TYPE              | String         |
| TRAFFICWAY_TYPE               | String         |
| LANE_CNT                      | Number         |
| ALIGNMENT                     | String         |
| ROADWAY_SURFACE_COND          | String         |
| ROAD_DEFECT                   | String         |
| REPORT_TYPE                   | String         |
| CRASH_TYPE                    | String         |
| INTERSECTION_RELATED_I        | String         |
| NOT_RIGHT_OF_WAY_I            | String         |
| HIT_AND_RUN_I                 | String         |
| DAMAGE                        | String         |
| DATE_POLICE_NOTIFIED          | Date Timestamp |
| PRIM_CONTRIBUTORY_CAUSE       | String         |
| SEC_CONTRIBUTORY_CAUSE        | String         |
| STREET_NO                     | Number         |
| STREET_DIRECTION              | String         |
| STREET_NAME                   | String         |
| BEAT_OF_OCCURRENCE            | Number         |
| PHOTOS_TAKEN_I                | String         |
| STATEMENTS_TAKEN_I            | String         |
| DOORING_I                     | String         |
| WORK_ZONE_I                   | String         |
| WORK_ZONE_TYPE                | String         |
| WORKERS_PRESENT_I             | String         |
| NUM_UNITS                     | Number         |
| MOST_SEVERE_INJURY            | String         |
| INJURIES_TOTAL                | Number         |
| INJURIES_FATAL                | Number         |
| INJURIES_INCAPACITATING       | Number         |
| INJURIES_NON_INCAPACITATING   | Number         |
| INJURIES_REPORTED_NOT_EVIDENT | Number         |
| INJURIES_NO_INDICATION        | Number         |
| INJURIES_UNKNOWN              | Number         |
| CRASH_HOUR                    | Number         |
| CRASH_DAY_OF_WEEK             | Number         |
| CRASH_MONTH                   | Number         |
| LATITUDE                      | Number         |
| LONGITUDE                     | Number         |
| LOCATION                      | Point          |
