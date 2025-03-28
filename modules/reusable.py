import requests
import os

# data access and manipulation libraries
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde, norm, kurtosis

# visualization libraries
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import seaborn as sns

# visualization libraries - ui interaction
import panel as pn
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.display import display, clear_output

# capture any display output from functions
out = widgets.Output()

const_default_storage_dir = 'assets/data'
const_src_url = "https://data.cityofchicago.org/api/views/85ca-t3if/rows.csv?fourfour=85ca-t3if&cacheBust=1742398767&date=20250319&accessType=DOWNLOAD"
const_default_storage_file = "assets/data/chicago_traffic_crashes.csv"

# load the datat from the stored assets
# reusable function to load a pandas dataframe from an existing csv file


# always ensure the asste/data directory is created
if not os.path.exists(const_default_storage_dir):
    os.makedirs(const_default_storage_dir)


def download_chicago_crashdata(storein: str = const_default_storage_file, src_url: str = const_src_url,
                               force: bool = False):
    """
    Downloads the Chicago crash data from the public site and stores it in the provided filepath.
    Args:
        filepath (str): File where to store the downloaded data
    Returns:
        None
    """
    url = src_url

    # only delete the file on force and it exists
    if os.path.exists(storein) and force == True:
        try:
            os.remove(storein)
            print(f"Existing file {storein} deleted via Force being set to True.")
        except OSError as e:
            print(f"Error deleting existing file: {e}. Please delete or replace manually if needed.")

    if os.path.exists(storein) == False:
        try:
            response = requests.get(url)
            response.raise_for_status()

            with open(storein, 'wb') as f:
                f.write(response.content)
            print(f"CSV saved to {storein}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching or saving CSV: {e}")
        except IOError as e:
            print(f"Error writing to file: {e}")
    else:
        print(f"CSV present in {storein}.")


def get_chicago_crash_data(filepath: str = const_default_storage_file) -> pd.DataFrame:
    """
    Gets a CSV dataset via the url
    Args:

        filepath (str): The path to save the CSV file.
    Returns:
        A pandas DataFrame containing the CSV file content
    """

    # if the file does exist locally - we will go grab it
    if os.path.exists(filepath):
        try:
            return etl_crash_data(pd.read_csv(filepath))
        except Exception as e:
            print(f"Error loading the CSV: {e}")
            return None

    # not force and the file is already there - voila
    print(f"No file called::{filepath} found")
    return None


def etl_crash_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Does some transformation and extraction of additional data into our crash dataset that can be helpful calculating visualization
    Args:

        df (pandas dataframe): Dataframe to modify and pass back to the caller
    Returns:
        A modified dataframe with some additional enriched data.
    """

    # call out why this is important - pass in the format - faster to load seconds over minutes.
    df['CRASH_DATE'] = pd.to_datetime(df['CRASH_DATE'], format="%m/%d/%Y %I:%M:%S %p")
    df['CRASH_YEAR'] = df['CRASH_DATE'].dt.year
    df['CRASH_YEAR'] = df['CRASH_DATE'].dt.year
    df['CRASH_DAY_NAME'] = df['CRASH_DATE'].dt.day_name()
    df['CRASH_MONTH_NAME'] = df['CRASH_DATE'].dt.month_name()

    # we want to insure our numeric data is properly set to 0 where NaN is encountered
    df['INJURIES_TOTAL'] = df['INJURIES_TOTAL'].fillna(0)
    df['INJURIES_FATAL'] = df['INJURIES_FATAL'].fillna(0)
    df['INJURIES_INCAPACITATING'] = df['INJURIES_INCAPACITATING'].fillna(0)
    df['INJURIES_NO_INDICATION'] = df['INJURIES_NO_INDICATION'].fillna(0)
    df['INJURIES_NON_INCAPACITATING'] = df['INJURIES_NON_INCAPACITATING'].fillna(0)
    df['INJURIES_UNKNOWN'] = df['INJURIES_UNKNOWN'].fillna(0)
    df['INJURIES_REPORTED_NOT_EVIDENT'] = df['INJURIES_REPORTED_NOT_EVIDENT'].fillna(0)

    return df


# ****************************************************************
# visualization functions 
# ****************************************************************


# ****************************************************************
# Plot the crash count by year in a bar graph
# ****************************************************************
def plot_crash_count_by_year(df: pd.DataFrame):
    """
    Displays the crash count by year from the given dataset.

    Args:
        df (pd.DataFrame): The crash dataset as a Pandas DataFrame.
                           It should contain a 'CRASH_YEAR' column with datetime information.
    """
    # Count the number of crashes for each year
    crash_counts_by_year = df['CRASH_YEAR'].value_counts().sort_index()
    years = sorted(df['CRASH_YEAR'].unique())
    year_counts = crash_counts_by_year.index.tolist()
    counts = crash_counts_by_year.values.tolist()

    # Create the bar plot
    plt.figure(figsize=(10, 6))

    # use the bars variable to later add annotation
    bars = plt.bar(year_counts, counts, color='skyblue')

    # Add labels and title
    plt.xlabel("Year")
    plt.ylabel("Crash Count")
    plt.title("Crash Count by Year")

    # in this case, our x axis ticks are the same as the year label - 
    plt.xticks(labels=years, ticks=years, rotation=45, ha='right')

    # Annotate the percentage of change between the bars
    for i in range(1, len(counts)):
        old_count = counts[i - 1]
        new_count = counts[i]
        if old_count == 0:
            percentage_change = float('inf') if new_count > 0 else 0
        else:
            percentage_change = ((new_count - old_count) / old_count) * 100

        height = bars[i].get_height()
        plt.annotate(f'{percentage_change:.2f}%',
                     xy=(bars[i].get_x() + bars[i].get_width() / 2, height),
                     xytext=(0, 3),  # Offset in points
                     textcoords='offset points',
                     ha='center', va='bottom')

    # plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.show()


# ***************************************
# let's understand via the violin plot
# include or not include : tbd
# ***************************************
def plot_violinplot_injuries_by_lighting(df: pd.DataFrame, year: int = 2025, applylogtransform: bool = True):
    """
    Generates a violin plot of 'INJURIES_TOTAL' for different
    'LIGHTING_CONDITION' categories from the input DataFrame.

    Args:
        df (pd.DataFrame): The pandas DataFrame containing crash data with
            'INJURIES_TOTAL' and 'LIGHTING_CONDITION' columns.
        year (int): The year we want to filter on, we will default to 2025
        applylogtranform (bool): The year we want to filter on, we will default to 2025
    """
    if 'INJURIES_TOTAL' not in df.columns or 'LIGHTING_CONDITION' not in df.columns:
        print("Error: DataFrame must contain 'INJURIES_TOTAL' and 'LIGHTING_CONDITION' columns.")
        return

    plt.figure(figsize=(12, 8))
    df_copy = df.copy()
    df_copy = df_copy[df_copy['CRASH_YEAR'] == year]

    if applylogtransform == True:
        # due to a large number of lower number of total injuries, the data is heavily skewed
        # applying a log transform to stretch out the data
        df_copy['LOG_INJURIES_TOTAL'] = np.log(df_copy['INJURIES_TOTAL'] + 1)
        sns.violinplot(x='LIGHTING_CONDITION', y='LOG_INJURIES_TOTAL', data=df_copy)
        plt.ylabel('Total Injuries - (LOG Transformed)')
    else:
        sns.violinplot(x='LIGHTING_CONDITION', y='INJURIES_TOTAL', data=df_copy)
        plt.ylabel('Total Injuries')

    plt.xlabel('Lighting Condition')
    plt.title(f'Violin Plot of Total Injuries by Lighting Condition -{year}')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()


# ****************************************************************
# function for setting up a widget for the jitter to apply a filter on the year
# ****************************************************************
def setup_interactive_jitter(df: pd.DataFrame):
    """
    Setup for the 
    """

    # we need to activate the widgets
    pn.extension('ipywidgets')

    # unique set of years reverse sorted
    years = sorted(df['CRASH_YEAR'].unique(), reverse=True)

    # *********************************************
    # setup a dropdown widget bound to the unique
    # default to the most current year
    # *********************************************
    yearselector = widgets.Dropdown(
        options=years,
        value=years[0],
        description='Year:',
        disabled=False,
    )

    # **************************************************************************************
    # injury selector - max 30 ouch!
    # **************************************************************************************
    minimalinjuryselector = widgets.IntSlider(
        value=1,
        min=0,
        max=30,
        step=1,
        description='Injury Count:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d'
    )

    # our callback function as the widget set is being interacted with
    def crash_year_plot(year, minimalinjury):
        display(plot_crash_hour_of_day_vs_injuries_with_jitter(df, minimalinjury, year))

    # here we will create a panel row and apply Markdown # to create a title and our widgets
    row = pn.Row('# Options', yearselector, minimalinjuryselector, styles=dict(background='WhiteSmoke'))

    # create the initial iteractive plot
    filteredplot = widgets.interactive_output(crash_year_plot,
                                              {'year': yearselector, 'minimalinjury': minimalinjuryselector})

    display(row)

    display(filteredplot)


# ****************************************************************
# Plot the crash hour in the day with injuries and jitter it up
# ****************************************************************
def plot_crash_hour_of_day_vs_injuries_with_jitter(df: pd.DataFrame, minimalinjury: int = 1, year: int = None):
    """
    Generates a scatter plot of 'LANE_CNT' against 'INJURIES_TOTAL'
    from the input pandas DataFrame, with added jitter.

    Args:
        df: The pandas DataFrame containing crash data with
            'CRASH_HOUR' and 'INJURIES_TOTAL' columns.
    """
    if 'CRASH_HOUR' not in df.columns or 'INJURIES_TOTAL' not in df.columns:
        print("Error: DataFrame must contain 'CRASH_HOUR' and 'INJURIES_TOTAL' columns.")
        return

    # Define the amount of jitter
    jitter = 0.2

    df_copy = df.copy()
    df_copy = df_copy[df_copy['INJURIES_TOTAL'] >= minimalinjury]

    # filter further by year
    if year is not None:
        df_copy = df_copy[df_copy['CRASH_YEAR'] == year]

    # Apply jitter to the 'LANE_CNT' and 'INJURIES_TOTAL' columns - we align the size of the filtered dataset
    jittered_x = df_copy['INJURIES_TOTAL'] + np.random.normal(loc=0, scale=jitter, size=len(df_copy))
    jittered_y = df_copy['CRASH_HOUR'] + np.random.normal(loc=0, scale=jitter, size=len(df_copy))

    # Adjust this value to control the amount of jitter
    plt.figure(figsize=(16, 6))
    sns.scatterplot(x=jittered_x, y=jittered_y, data=df_copy, alpha=0.6)

    # use the original so we get all hours
    plt.yticks(np.arange(0, 24), sorted(df['CRASH_HOUR'].unique()))  # Label y-axis with day names

    plt.ylabel('Hour of the Day')
    plt.xlabel('Total Injuries')

    title = f'Jitter Scatter Plot of Hour of the Day vs. Minimal Injury ({minimalinjury})'
    if year is not None:
        title = f'Jitter Scatter Plot of Hour of the Day vs. Minimal Injury ({minimalinjury}) - {year}'
    plt.title(title)
    plt.grid(True, which="major", axis="y", linestyle='--', alpha=0.7)  # Add a horizontal grid for days
    plt.show()


# ****************************************************************
# function for setting up a widget for the jitter to apply a filter on the year
# ****************************************************************
def setup_histogram_crashes_by_year(df: pd.DataFrame):
    """
    Setup for the 
    """

    # we need to activate the widgets
    pn.extension('ipywidgets')

    # unique set of years reverse sorted
    years = sorted(df['CRASH_YEAR'].unique(), reverse=True)

    # *********************************************
    # setup a dropdown widget bound to the unique
    # default to the most current year
    # *********************************************
    yearselector = widgets.Dropdown(
        options=years,
        value=years[0],
        description='Year:',
        disabled=False,
    )

    # our callback function as the widget set is being interacted with
    def crash_year_plot(year):
        display(plot_histogram_crashes_by_year(df, year))

    # here we will create a panel row and apply Markdown # to create a title and our widgets
    row = pn.Row('# Options', yearselector, styles=dict(background='WhiteSmoke'))

    # create the initial iteractive plot
    filteredplot = widgets.interactive_output(crash_year_plot, {'year': yearselector})

    # display the row
    display(row)
    # display the filtered interactive
    display(filteredplot)


# ****************************************************************
#
# ****************************************************************
def plot_histogram_crashes_by_year(df: pd.DataFrame, year: int):
    df_copy = df.copy()
    df_copy = df_copy[df_copy['CRASH_YEAR'] == year]
    plt.figure(figsize=(10, 5))
    crash_hours = df_copy['CRASH_HOUR']
    plt.hist(crash_hours, bins=range(25), density=True, alpha=0.4, color='green', edgecolor='black', label='Histogram')

    # like week 2
    kde = gaussian_kde(crash_hours)
    x_kde = np.linspace(min(crash_hours), max(crash_hours), 100)
    density_kde = kde(x_kde)
    plt.plot(x_kde, density_kde, color='red', linewidth=2, label='KDE')

    # like week 2 -calculate the mean and standard deviation of the data
    mean = np.mean(crash_hours)
    std = np.std(crash_hours)

    # norm dist
    xmin, xmax = plt.xlim()
    x_norm = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x_norm, mean, std)

    # calculate the kurtosis value
    kurtosisval = kurtosis(crash_hours)

    plt.plot(x_norm, p, 'k--', linewidth=2, label=f'Normal Distribution\n(μ={mean:.2f}, σ={std:.2f})')

    # empty to add value purely to the legend - easier than a textbox!!
    plt.plot([], [], ' ', label=f'Kurtosis Value\n{kurtosisval:.2f}')

    # Customize the plot
    plt.title('Distribution of Crash Hours with Normal Distribution')
    plt.xlabel('Hour of the day (0-23) from midnight to 11pm')
    plt.ylabel('Probability Density')

    # we want ours 0 (midnight to 11 pm) in that order
    plt.xticks(range(24))
    plt.legend(loc='best')
    # digging the grid -- 
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()


# ****************************************************************
# function for setting up a widget for the heat map year filter
# ****************************************************************
def setup_heatmap_weather_road_condition_by_year(df: pd.DataFrame):
    """
    Setup for the 
    """

    # we need to activate the widgets
    pn.extension('ipywidgets')

    # unique set of years reverse sorted
    years = sorted(df['CRASH_YEAR'].unique(), reverse=True)

    # *********************************************
    # setup a dropdown widget bound to the unique
    # default to the most current year
    # *********************************************
    yearselector = widgets.Dropdown(
        options=years,
        value=years[0],
        description='Year:',
        disabled=False,
    )

    # our callback function as the widget set is being interacted with
    def crash_year_plot(year):
        display(plot_frequency_heatmap_weather_road_condition(df, year))

    # here we will create a panel row and apply Markdown # to create a title and our widgets
    row = pn.Row('# Options', yearselector, styles=dict(background='WhiteSmoke'))

    # create the initial iteractive plot
    filteredplot = widgets.interactive_output(crash_year_plot, {'year': yearselector})

    # display the row
    display(row)
    # display the filtered interactive
    display(filteredplot)


def plot_frequency_heatmap_weather_road_condition(df: pd.DataFrame, year: int = None):
    """
    Generates a frequency heatmap of 'WEATHER_CONDITION' vs.
    'ROADWAY_SURFACE_COND' from the input DataFrame.

    Args:
        df: The pandas DataFrame containing crash data with
            'WEATHER_CONDITION' and 'ROADWAY_SURFACE_COND' columns.
    """
    if 'WEATHER_CONDITION' not in df.columns or 'ROADWAY_SURFACE_COND' not in df.columns:
        print("Error: DataFrame must contain 'WEATHER_CONDITION' and 'ROADWAY_SURFACE_COND' columns.")
        return

    df_copy = df.copy();
    default_title = 'Heatmap: Weather vs. Road Condition'

    if year is not None:
        df_copy = df_copy[df_copy['CRASH_YEAR'] == year]
        default_title = default_title + f' {year}'

    # Create a contingency table (frequency count) of the two columns
    cross_tab = pd.crosstab(df_copy['WEATHER_CONDITION'], df_copy['ROADWAY_SURFACE_COND'])

    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(cross_tab, annot=True, fmt="d", cmap="viridis", cbar_kws={'label': 'Frequency'})
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    plt.xlabel('Road Condition')
    plt.ylabel('Weather Condition')
    plt.title(default_title)
    plt.tight_layout()
    plt.show()


def create_dashboard(df: pd.DataFrame, year: int = 2024, minimalinjury: int = 1):
    df_copy = df.copy();

    if year is not None:
        df_copy = df_copy[df_copy['CRASH_YEAR'] == year]

    fig = plt.figure(figsize=(18, 16))
    gs = fig.add_gridspec(2, 2)

    # ****************************************************
    # Summarized bar by year - Not filtered - intentional
    # ****************************************************
    ax1 = fig.add_subplot(gs[0, 0])
    crash_counts_by_year = df['CRASH_YEAR'].value_counts().sort_index()
    years = sorted(df['CRASH_YEAR'].unique())
    year_counts = crash_counts_by_year.index.tolist()
    counts = crash_counts_by_year.values.tolist()
    bars = plt.bar(year_counts, counts, color='skyblue')
    ax1.set_xticks(labels=years, ticks=years, rotation=45, ha='right')

    # Annotate the percentage of change between the bars
    for i in range(1, len(counts)):
        old_count = counts[i - 1]
        new_count = counts[i]
        if old_count == 0:
            percentage_change = float('inf') if new_count > 0 else 0
        else:
            percentage_change = ((new_count - old_count) / old_count) * 100

        height = bars[i].get_height()
        plt.annotate(f'{percentage_change:.2f}%',
                     xy=(bars[i].get_x() + bars[i].get_width() / 2, height),
                     xytext=(0, 3),  # Offset in points
                     textcoords='offset points',
                     fontsize=7,
                     ha='center', va='bottom')

    ax1.set_title(f'Crash Count by Year')
    # ****************************************************

    # ****************************************************
    # Jitter Scatter plot
    # ****************************************************
    ax2 = fig.add_subplot(gs[0, 1])
    # Define the amount of jitter
    jitter = 0.2

    df_copy2 = df_copy[df_copy['INJURIES_TOTAL'] >= minimalinjury]

    # Apply jitter to the 'LANE_CNT' and 'INJURIES_TOTAL' columns - we align the size of the filtered dataset (df_copy2) 
    jittered_x = df_copy2['INJURIES_TOTAL'] + np.random.normal(loc=0, scale=jitter, size=len(df_copy2))
    jittered_y = df_copy2['CRASH_HOUR'] + np.random.normal(loc=0, scale=jitter, size=len(df_copy2))

    # Adjust this value to control the amount of jitter
    sns.scatterplot(x=jittered_x, y=jittered_y, data=df_copy2, alpha=0.6)

    # use the original so we get all hours
    ax2.set_yticks(np.arange(0, 24), sorted(df['CRASH_HOUR'].unique()))  # Label y-axis with day names

    ax2.set_ylabel('Hour of the Day')
    ax2.set_xlabel('Total # of Injuries')
    ax2.set_title(f'Jitter Scatter - {year} for injury count {minimalinjury}')
    # ****************************************************

    # Box plot
    ax3 = fig.add_subplot(gs[1, 0])
    crash_hours = df_copy['CRASH_HOUR']
    ax3.hist(crash_hours, bins=range(25), density=True, alpha=0.4, color='green', edgecolor='black', label='Histogram')

    # like week 2
    kde = gaussian_kde(crash_hours)
    x_kde = np.linspace(min(crash_hours), max(crash_hours), 100)
    density_kde = kde(x_kde)
    ax3.plot(x_kde, density_kde, color='red', linewidth=2, label='KDE')

    # like week 2 -calculate the mean and standard deviation of the data
    mean = np.mean(crash_hours)
    std = np.std(crash_hours)

    # norm dist
    xmin, xmax = plt.xlim()
    x_norm = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x_norm, mean, std)

    # calculate the kurtosis value
    kurtosisval = kurtosis(crash_hours)

    ax3.plot(x_norm, p, 'k--', linewidth=2, label=f'Normal Distribution\n(μ={mean:.2f}, σ={std:.2f})')

    # empty to add value purely to the legend - easier than a textbox!!
    ax3.plot([], [], ' ', label=f'Kurtosis Value\n{kurtosisval:.2f}')

    # Customize the plot
    ax3.set_title(f'Distribution of Crash Hours with Normal Distribution {year}')
    ax3.set_xlabel('Hour of the day (0-23) from midnight to 11pm')
    ax3.set_ylabel('Probability Density')
    ax3.set_xticks(range(24))
    ax3.legend(loc='best')
    # ****************************************************

    # ****************************************************
    # heatmap of the 2 category (Weather and Road)
    # ****************************************************
    heatmap_default_title = 'Heatmap: Weather vs. Road Condition'
    if year is not None:
        heatmap_default_title = heatmap_default_title + f' {year}'

    # Create a contingency table (frequency count) of the two columns
    cross_tab = pd.crosstab(df_copy['WEATHER_CONDITION'], df_copy['ROADWAY_SURFACE_COND'])
    ax4 = fig.add_subplot(gs[1, 1])
    ax = sns.heatmap(cross_tab, annot=True, fmt="d", cmap="viridis", cbar_kws={'label': 'Frequency'})
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=6, rotation=45, ha='right')
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=6, rotation=45, ha='right')
    ax4.set_xlabel('Road Condition', fontsize=6.5)
    ax4.set_ylabel('Weather Condition', fontsize=6.5)
    ax4.set_title(heatmap_default_title)

    return fig


def create_interactive_dashboard(df: pd.DataFrame):
    """Creates an interactive dashboard with widgets for controlling the display."""
    pn.extension('ipywidgets')
    years = sorted(df['CRASH_YEAR'].unique(), reverse=True)
    yearselector = widgets.Dropdown(
        options=years,
        value=years[0],
        description='Year:',
        disabled=False,
    )

    minimalinjuryselector = widgets.IntSlider(
        value=1,
        min=0,
        max=30,
        step=1,
        description='Injury Count:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d'
    )

    def update(year, minimumjury):
        # Clear previous output to avoid memory issues
        clear_output(wait=True)

        # Create and display the dashboard with current widget values
        fig = create_dashboard(df=df, year=year, minimalinjury=minimumjury)
        plt.show()

    # here we will create a panel row and apply Markdown # to create a title and our widgets
    row = pn.Row('# Filter Options', yearselector, minimalinjuryselector, styles=dict(background='WhiteSmoke'))

    # create the initial iteractive plot
    filteredplot = widgets.interactive_output(update, {'year': yearselector, 'minimumjury': minimalinjuryselector})

    # display the row
    display(row)
    # display the filtered interactive
    display(filteredplot)

    #return (row, filteredplot)
