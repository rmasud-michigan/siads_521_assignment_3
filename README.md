# siads_521_assignment_3
SIADS 521 Data Visualization Assignment 3 

## Overview
This repo is intended to demonstrate real example of data visualizations with Python.
The various plots will analyze the City of Chicago crash data. 
The analysis will use techniques to extract, transform and load the data.

# Required Libraries:
| Module     | Install                                                       | Description                                                                                                    |
|------------|---------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| requests      | <div style="text-align: left">`pip install requests` </div>      | <div style="text-align: left">Python based HTTP client </div>             |
| pandas     | <div style="text-align: left">`pip install pandas` </div>     | <div style="text-align: left">Powerful data structures for data analysis, time series, and statistics  </div>  |
| matplotlib | <div style="text-align: left">`pip install matplotlib` </div> | <div style="text-align: left">Python plotting package </div>                                                   |
| seaborn    | <div style="text-align: left">`pip install seaborn` </div>    | <div style="text-align: left">Statistical data visualization </div>                                            |
| numpy      | <div style="text-align: left">`pip install numpy` </div>      | <div style="text-align: left">Foundational module for dealing and working with large arrays </div>             |
| scipy      | <div style="text-align: left">`pip install scipy` </div>      | <div style="text-align: left">Fundamental algorithms for scientific computing in Python </div>             |
| panel      | <div style="text-align: left">`pip install panel` </div>      | <div style="text-align: left">Powerful data exploration & web app framework for Python </div>             |
| ipython      | <div style="text-align: left">`pip install ipython` </div>      | <div style="text-align: left">IPython: Productive Interactive Computing </div>             |
| ipywidgets      | <div style="text-align: left">`pip install ipywidgets` </div>      | <div style="text-align: left">Jupyter interactive widgets </div>             |
| watermark      | <div style="text-align: left">`pip install watermark` </div>      | <div style="text-align: left">IPython magic function to print date/time stamps and various system information. </div>             |


```
pip install -r requirements.txt
```

## Source Data
### City of Chicago
* https://data.cityofchicago.org/api/views/85ca-t3if/rows.csv?fourfour=85ca-t3if&cacheBust=1742398767&date=20250319&accessType=DOWNLOAD


## Visualization Techniques
> As part of the visualization layer of the workbook, I  have examples of different plots using libraries that are incredibly powerful and can bring immense datasets together quickly. I am hoping as you look through this workbook you can see the power of these visualizations and get a sense of why a picture can be worth a thousand words. The visualizations that I will use are primarily matplotlb and seaborn as the rendering tools. With this workbook, we will see bar plots for big aggregate data. For example, a single value aggregated by year can be easily presented in a vertical bar graph. A bar graph can be good for quick aggregate however details are better suited in other plots.

> Another plot in this workbook is a jitter scattergraph. This a very powerful representation of data that has a potentially heavy density at coordinates and provides a point visual on the volume of occurrences at each (x,y). One downside to a jitter scattergraph is the zoom level of the data. That means if we are looking at a dataset that has millions of rows with hundreds of thousands of occurrences, the jitter may still resemble a continuous wide line and be difficult to read. Filtering on the data can help that to get down to a reasonable view projection.

> An additional visualization that is part of this workbook utilizes kernel density estimation (KDE) via the seaborn library. This combined with a normal distribution and a histogram can provide a useful visualization to highlight kurtosis in the data. This is good for providing users with a visual on occurrence relative to the normal distribution. One thing to account for with using a histogram is the number of bins. If the data being presented is temporal-based like weeks in a year, 52 bins might be an ideal number.

> The last visualization is a heatmap and can be useful for categorical comparison while aggregating the categories. One drawback to the heatmap is if the categories are numerous in both categories it can be difficult to read.

> Finally as part of this workbook, to emulate dashboard filtering behaviors, widgets will be introduced to allow a user of the workbook to filter the data dynamically while see that result visually. Some filtering is by year and another plot will have additional values to filter on. All code for the setup of the widgets and UI panel can be located in the reusable.py. 

## Demonstration

> In this workbook, I wanted to present different graphical representations of traffic crash information for the City of Chicago. Chicago is an incredibly large city in Illinois and one of the top 5 of the largest cities in the United States. As a result, there are a lot of visitors and residents who travel to the city. Chicago is also a well-established hub for mass transit that supports many of the residents and commuters who come to the city to visit or work. However, like many cities in the United States, accidents happen. As part of this workbook, I will use different visualization techniques and processing of the data the abilities the libraries used. Some of the graphics will be more straightforward and others will grow in the depth of complexity.

> Some of the goals of this workbook are to provide a user set of tools that can be used as a point of reference as well. Code-specific functionality as well techniques on how to implement them within Python and a Jupyter environment.

 ### Supporting Code - Modules

> To create clean seperations, the code functions mentioned in the cells can be located in:


```
./
├─ modules/
│  ├─ reusable.py
│  ├─ __init__.py
├─ assets/
│  ├─ data/
│  ├─ chicago_traffic_crashes.csv
├─ static/
│  ├─ *.png
```

> * The modules directory contains all the code referenced in this workbook. The resuable.py file contains all the functions referenced in the workbook and is imported into the workbook via this line of code:

```
from modules.reusable import *
```
> * The assets/data folder contains any referencable datasets and is also where downloaded data should be placed if done manually or via the functions.
> * The static directory is used to store static images referenced in this workbook.


**If you decide to add functions to reusable.py or modify them, depending on your python and jupyter setup, you may need to restart your kernel to get the latest changes pulled in and reloaded**

### Data - Retrieval
> This workbook contains a reusable function that will connect to a free and open source dataset available from the City of Chicago.
Via the requests module, this workbook can call and invoke a download of the file content. The CSV content is stored locally in the assets/data directory.
 
### Data - Parsing
> As part of the data presentation, pandas offers a robust set of tools, and combined with programmatic abilities in Python, we can enhance a dataset to reduce UI and code noise. As part of the dataset from the city of Chicago data coming in is in the form of CSV and times we will want to have some of the fields sub-parsed or in a more performant format like a date time. As part of the reuseable.py, those transformations and mutations will occur within a Python method called etl_crash_data.

**example code**
```
    """
    Does some transformation and extraction of additional data into our crash dataset that can be helpful for visualizations
    Args:

        df (pandas dataframe): Dataframe to modify and pass back to the caller
    Returns:
        A modified dataframe with some additional enriched data.
    """

    # pass in the format - faster to load seconds over minutes.
    df['CRASH_DATE'] = pd.to_datetime(df['CRASH_DATE'],format="%m/%d/%Y %I:%M:%S %p")
    df['CRASH_YEAR'] = df['CRASH_DATE'].dt.year
    df['CRASH_YEAR'] = df['CRASH_DATE'].dt.year
    df['CRASH_DAY_NAME'] = df['CRASH_DATE'] .dt.day_name()
    df['CRASH_MONTH_NAME'] = df['CRASH_DATE'].dt.month_name()

    # we want to ensure our numeric data is properly set to 0 if NaN is encountered
    # not doing this can impede or cause errors in heatmaps and histograms
    df['INJURIES_TOTAL'] = df['INJURIES_TOTAL'].fillna(0)
    df['INJURIES_FATAL'] = df['INJURIES_FATAL'].fillna(0)
    df['INJURIES_INCAPACITATING'] = df['INJURIES_INCAPACITATING'].fillna(0)
    df['INJURIES_NO_INDICATION'] = df['INJURIES_NO_INDICATION'].fillna(0)
    df['INJURIES_NON_INCAPACITATING'] = df['INJURIES_NON_INCAPACITATING'].fillna(0)
    df['INJURIES_UNKNOWN'] = df['INJURIES_UNKNOWN'].fillna(0)
    df['INJURIES_REPORTED_NOT_EVIDENT'] = df['INJURIES_REPORTED_NOT_EVIDENT'].fillna(0)

    return df
```

### Data - Loading
```
# load in the data into our local variable
# we will pass that to our reusable plotting functions throughout the workbook
# this dataframe will have the etl from etl_crash_data applied to it
df_chicago_data = get_chicago_crash_data()

# let's take a peek at the data
df_chicago_data.head(5)
```

### Figure 1 - Plot of Annualized Traffic Crashes All Years
> We want a better understanding of how the city of Chicago is doing with car crashes year after year. We can accomplish this by aggregating our dataset on the CRASH_YEAR column, determining overall counts, and further annotating our plot with the % of change. 
> * Questions we can look to answer?
>   * Are there holes in the data?
>   * Are outliers present or are extreme changes + or - present?
>     * Are those changes explainable?

``` 
#our primary column of aggregation is the CRASH_YEAR
# we can look at aggregate of the instance counts by year
cell_crash_counts_by_year = df_chicago_data['CRASH_YEAR'].value_counts().sort_index()

# via describe we get our high level stats.
cell_crash_counts_by_year.describe()

# use the reusable function and pass in our dataframe
plot_crash_count_by_year(df_chicago_data)
```

![figure_1_static](https://raw.githubusercontent.com/rmasud-michigan/siads_521_assignment_3/refs/heads/main/static/figure_1_static.png)