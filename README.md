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

#### Crash count analysis

> The bar plot reveals some intersting data points.
>> * As part of the plot, the % of change was added. Just in the first 4 years, the initial % of change is quite large. Data collection appears to have started in 2015 but from 2016 forward appears to be more complete.
>>    * **Using % can be misleading because looking at 2014 to 2015, the change is massive.** Did it mean that Chicago was having an immediate accident crisis? No. The data is clearly incomplete within the dataset and an indicator that the data from 2016 forward is really a better starting point for analysis.
>>    * The spike between 2016 and 2017 may have been influenced by a well-known baseball team breaking a 108-year streak of not winning a World Series and an increase in visitors to Wrigley Field from all over the country the following year.
>>    * Additional factors could be a lower gas price in 2017 that increased drivers visiting the city
>>    * https://data.theadvertiser.com/gas-price/chicago/YORD/2023-02-06/  
>> * 2020 has an interesting dip
>>   * What could cause this? The global COVID-19 pandemic resulted in a global slowdown and near stoppage of human movement. We can see that impact on the city for events and in office work and how they influenced a lower number of car crashes.
>>   * [Chicago traffic, CTA patterns dramatically affected by COVID pandemic](https://abc7chicago.com/chicago-traffic-construction-cta-bus-tracker/10451178/)
>> * Data collection for 2025 is ongoing and running this workbook at later points in 2025 or beyond may contain additional data.


### Figure 2 - Injury density by hour of the day
> With our crash data, we are getting a sense that there are a lot of crashes! Bar plots make the difficult to zoom into the data to see how often it occurs. Similar to having a single Bin size. So we want to look at our data at a smaller scale. The hour-by-day plot with a jitter can help us understand what hours have more observations of incidents with injuries.
> * Questions we can look to answer
>   * When do we see higher instances of injuries?
>   * Are times in the day that have a lot of injuries?
>   * What hours have more frequency of 4 or more injuries?

 
```
#use the reusable function will evaluate all years and filter initially on crashes with >=1 injuries

# all injuries
plot_crash_hour_of_day_vs_injuries_with_jitter(df_chicago_data)
```

![figure_2_static](https://raw.githubusercontent.com/rmasud-michigan/siads_521_assignment_3/refs/heads/main/static/figure_2_static.png)

#### Initial Jitter Scatter Analysis

> We can see that irrespective of hour the day, across all years, < 5 injuries is heavily saturated in observed incidents. One of the challenges of a jitter visualizations stems from the zoom level on the data being evaluated. In the initial jitter plot, we are looking at all years and >= 1 injuries. If we scope it down two fold by year an the minimal injury count, we should be able zoom into the data and get a better idea if patterns emerge.

```
# call the reusable function to enable the widgets to filter on year and injury counts
# this will setup an options section with panel and display in a row 2 interactive filters
# filter 1: year (bound to the unique list of all years within the dataframe
# filter 2: injury count (static range of 1 to 30)
# as the user interacts with the filters the selected year and injury count will filter the dataset and re-plot the data
setup_interactive_jitter(df_chicago_data)
```

![figure_2_with_options_static](https://raw.githubusercontent.com/rmasud-michigan/siads_521_assignment_3/refs/heads/main/static/figure_2_with_options_static.png)

#### Crash hour analysis

> When looking at the plot and the minimal injury is 1 or more, the concentration is still very heavy difficult to discern if groupings are present. Using the widgets and if we look at 2023 as an example and ask the question "In 2023, what hours had 4 or more injuries", we can see that the afternoon hours (13 - 16 or 1 pm to 4 pm) demonstrate a cluster of injuries. What can be a possible cause of this?


> * What hours should I avoid?
> * Using the year 2024 as an example, the afternoon hours of 3 pm to 5 pm have a visibly larger number of injuries.
> * Rush hour for workers leaving the city and traveling home leads to a larger number of cars on the roads at those times.

> **Image found in static/2023_minimal_4_injury.png**

> ![alt text](https://raw.githubusercontent.com/rmasud-michigan/siads_521_assignment_3/refs/heads/main/static/2023_minimal_4_injury.png)

### Figure 3 - Probability Distribution (Hour of Day)

> As we examine the jitter plot, it raises an interesting question about the hour of day and the overall probability of a car accident occurring. To assist in answering the question we can utilize a histogram in combination with a kernel density estimation and a normal distribution. Maybe this can present an additional angle on the data.

> We can look to anwer questions like:
> * Filtering by year, are there times of the day that pose more risk for a car accident? If so, how risky is it?
> * Filtering by year, what level of kurtosis is present in the data?

```
# use the reusable function to setup a widget control histogram
# filter 1: year (bound to the unique list of all years within the dataset
# plot a histogram of the crash data for the selected year
# calculate the normal distribution and kurtosis value
setup_histogram_crashes_by_year(df_chicago_data)
```
#### static example of figure 3
![figure_3_static](https://raw.githubusercontent.com/rmasud-michigan/siads_521_assignment_3/refs/heads/main//static/figure_3_static.png)

#### Probability analysis

> Where do we see the most risk traveling in the city in vehicle?
> * We can see using a kernel density with normal distribution, the time morning rush hours of 7 to 8 am pose a range of risks in the morning. We can also see the afternoon hours starting from 3 pm to 6 or  7 pm are the next risk windows. 

> When can we have travel with the lowest risk?
> * If we have to travel to the city of Chicago, and we want to minimize our risk, we should travel to and from the city between 10 am and leave before 3 pm.

### Figure 4 - Heatmap Weather Conditions to Road Conditions

> To help us understand a possible source of car crashes. We can utilize two data categories within the dataset. We can analyze weather and road conditions to see which ones stand out as possible influencers of car accidents.

> Some questions we can try to answer:
> * Is winter the worst time to drive in the city? For example, SNOW or BLOWING SNOW?
> * Do road conditions like ICE or SNOW lead to a large number of accidents?

``` 
# use the reusable function to setup a widget powered plot to allow you filter by year
# this method is specifically targeting the road conditions in comparison to the 
# filter 1: year (bound to the unique list of all years within the datasframe
# plot a heatmap for the selected year with specific categorical data: Weather and Road surface conditions.
setup_heatmap_weather_road_condition_by_year(df_chicago_data)
```
#### static example of figure 4
![figure_4_static](https://raw.githubusercontent.com/rmasud-michigan/siads_521_assignment_3/refs/heads/main/static/figure_4_static.png)

#### Heatmap Analysis

> The heatmap reveals an interesting property of the data and possible assumptions. 
> * Does the weather or road condition play role?
>   * No. Looking at various years, the large number of accidents occur in dry and clear conditions. Other factors like traffic or a drivers prior accidents could help but the dataset lacks additional data around the volume of traffic at peak windows of traffic accidents and driver behaviors.
> * 2013 and 2014 are clearly not valid data years. 

### Figure 5 - Combined Dashboard

> Throughout the workbook we saw various types of plots that analyzed data. Some were specific in their aggregation. Others introduced additional widgets to filter data like Year or Injury counts. As a final example of the ability that these various libraries can bring, a single dashboard using the same reusable functions and filter can be a cohesive way to look at all the data side by side.

``` 
# this reusable function will create a dashboard with all 4 of the visualizations presented previously and allow you modify the year
create_interactive_dashboard(df_chicago_data)
```

#### static example of figure 5
![figure_5_static](https://raw.githubusercontent.com/rmasud-michigan/siads_521_assignment_3/refs/heads/main/static/figure_5_static.png)

### Dashboard Break Down

> From left to right
> * Row 1:
>   * Crash Count by Year - no applicable filter - always show all years
>   * Jitter Plot - Filtered by Year and Injury Count
> * Row 2:
>   * Distribution Crash Years - filtered by year
>   * Heatmap of Categories (Weather to Road Condition) - filtered by year

## Rules Adherence
> As part of building a reusable and repeatable workbook, we want to adhere to rules that will help us a data scientists collect, present, and share our findings with peers. As part of this workbook, these are the key rules that helped guide the final product.

### Rule 1 (Telling a story)
> Knowing our audience and how to craft a computational narrative is key. The rule on storytelling is about knowing our audience and presenting complex layers of data in a meaningful way that conveys information. As part of this workbook, as the data is presented, I want to provide information around what is the intent of the presented model, how it was produced, and present possible questions they can answer from the data. Like a story, I aimed to explain what problems I might have encountered and the steps I needed to take. This will help establish the how, the what, and why.

### Rule 2 (Document the process)
> The documentation rule is about providing the context and flow of where I got the data, and how the data was transformed, and loaded into the environment. Similar to a term paper or other historical stories, we want to provide the footnotes on where we sourced information and how we obtained it. This is important to establish legitimacy on the outputs. As part of this workbook, context around specific processing is called out to help educate the reader and provide them with samples and sources as well that they can reference. The embedded code in cells will have a context for the functions being called and reusable.py module will have comments within the code to allow another developer to modify and enhance it as needed.

### Rule 3 (Use Cell Divisions)
> The rule of cell division helps us establish a cleaner set of areas in the workbook. Each cell can act as the boundary of information and points of focus. To help keep cells clean, functional areas that can call a function help reduce the initial UI noise. We want to keep cells from spanning multiple scrolls to provide a user with a section-by-section viewing experience. Cells can support code and markup like Markdown to add documentation and provide a section-by-section flow.

### Rule 4 (Code Modularization)
> The rule for code moderation is intended to keep complex code out of direct view as well as give us a clean separation of concerns. Creating concise, reusable, and parameterized functions allows the visual side of the workbook to stay more in presenting the data. The module code within the workbook directory helps us keep that clean. As part of this workbook, I created modules that worked in extract, transform, and loading spaces. The modules are part of the repo and also contain documentation within them to provide other users the ability to see how certain techniques are applied.

### Rule 5 (Record Dependencies)
> The rule for recording dependencies allows us to convey what is required to run our workbook end to end. By capturing the libraries and necessary system needs we ensure portability. As part of this workbook in the folder root is a requirements.txt that can deploy the required libraries via pip into an environment running Jupyter notebook. The dependencies are also part of the [README.me](README.md) in the repo so anyone can get a sense of what is required without having to install it first. Lastly, as part of the deployment, the first cell of the workbook installs the dependencies.

### Rule 6 (Version Control)

> The ability to restore and save a working set of code to demonstrate functionality is important in the development community. Version control systems like Git or SubVersion offer the ability to store backups and branches of code that can worked on by different team members. Systems like Git provides free accounts to users to upload and share their work with the global community.
As part of this workbook, all the source code is available in a publicly available repository on Git and can be accessed at [siads_521_assignment_3](https://github.com/rmasud-michigan/siads_521_assignment_3.git).