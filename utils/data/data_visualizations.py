import pandas as pd
import matplotlib.pyplot as plt
import folium

import numpy as np
import matplotlib.pyplot as plt
import folium
import matplotlib.dates as mdates
import matplotlib.ticker as ticker 

def plot_annual_camera_violations(df:pd.DataFrame):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14,6))

    yearly_violations = df.groupby('YEAR')['VIOLATIONS_NUMERIC'].sum().reset_index(name='TOTAL_VIOLATIONS')
    
    camera_counts = df.groupby('YEAR')['CAMERA_ID'].nunique().reset_index(name='ACTIVE_CAMERAS')
    
    axes[0].bar(yearly_violations['YEAR'],yearly_violations['TOTAL_VIOLATIONS'])
    axes[0].set_xticks(yearly_violations['YEAR']) 
    axes[1].bar(camera_counts['YEAR'],camera_counts['ACTIVE_CAMERAS'])
    axes[1].set_xticks(camera_counts['YEAR']) 
    
    def format_y_axis(value, tick_number):
                return f'{int(value):,}' # Format as integer with commas
    
    axes[0].yaxis.set_major_formatter(ticker.FuncFormatter(format_y_axis))
    
    axes[0].set_xlabel('Year',fontsize=14)
    axes[0].set_ylabel('Total Violations',fontsize=14)
    axes[0].set_title('Red Light Camera Violations')
    
    #axes[0].set_legend(loc='best')
    
    
    axes[1].set_xlabel('Year',fontsize=14)
    axes[1].set_ylabel('Camera Counts',fontsize=14)
    axes[1].set_title('Red Light Cameras')
    #axes[1].set_legend(loc='best')
    
    plt.tight_layout()
    plt.show()

    
def time_series_plot(df:pd.DataFrame):
    """
    Creates a time series plot of violations over time.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
    """
    monthly_violations = df.groupby(pd.Grouper(key='VIOLATION_DATE', freq='M'))['VIOLATIONS_NUMERIC'].sum()
    plt.plot(monthly_violations.index, monthly_violations.values)
    plt.xlabel('Date')
    plt.ylabel('Total Violations')
    plt.title('Monthly Violation Trends')
    plt.show()

    #we will return the plot to the caller if additional ui transforms are warranted
    return plt

def violations_by_day_of_week(df:pd.DataFrame):
    """
    Creates a bar chart of violations by day of the week.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
    """
    df['DAY_OF_WEEK'] = df['VIOLATION_DATE'].dt.day_name()
    df.groupby('Day of Week')['VIOLATIONS'].sum().plot(kind='bar')
    plt.xlabel('VDay of Week')
    plt.ylabel('Total Violations')
    plt.title('Violations by Day of Week')
    plt.show()

    # we will return the plot to the caller if additional ui transforms are warranted
    return plt


def scatter_plot_xy( df):
    """
    Creates a scatter plot of camera locations using X and Y coordinates.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
    """
    plt.scatter(df['X COORDINATE'], df['Y COORDINATE'], c=df['VIOLATIONS'], cmap='viridis', s=10)
    plt.colorbar(label='Violations')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Camera Locations (State Plane)')
    plt.show()

    # we will return the plot to the caller if additional ui transforms are warranted
    return plt

def scatter_plot_lat_lon(df:pd.DataFrame):
    """
    Creates a scatter plot of camera locations using latitude and longitude.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
    """
    plt.scatter(df['LONGITUDE'], df['LATITUDE'], c=df['VIOLATIONS'], cmap='viridis', s=10)
    plt.colorbar(label='Violations')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Camera Locations (WGS84)')
    plt.show()

    # we will return the plot to the caller if additional ui transforms are warranted
    return plt

def violations_by_intersection(df:pd.DataFrame, topn:int=10, displayascending=False):
    """
    Creates a bar chart of violations by intersection.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        topN (int, optional): The number of top violations to return. Defaults to 10.
        ascending (bool, optional): Defaults to False.
    """
    df.groupby('INTERSECTION')['VIOLATIONS'].sum().sort_values(ascending=displayascending).head(topn).plot(kind='bar')
    plt.xlabel('Intersection')
    plt.ylabel('Total Violations')
    plt.title('Top 10 Intersections by Violations')
    plt.show()

    # we will return the plot to the caller if additional ui transforms are warranted
    return plt

def violations_by_camera_id(df:pd.DataFrame, topn:int=10, displayascending=False):
    """
    Creates a bar chart of violations by camera ID.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        topn (int, optional): Defaults to 10.
        displayascending (bool, optional): Defaults to False.
    """
    df.groupby('CAMERA ID')['VIOLATIONS'].sum().sort_values(ascending=displayascending).head(topn).plot(kind='bar')
    plt.xlabel('Camera ID')
    plt.ylabel('Total Violations')
    plt.title('Top 10 Cameras by Violations')
    plt.show()

    # we will return the plot to the caller if additional ui transforms are warranted
    return plt

def folium_map(df, output_file='output/camera_locations_map.html',zoom_start:int=12):
    """
    Creates a Folium map of camera locations.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        output_file (str): The filename for the output HTML map. This is file name to save the generated HTML map.
        zoom_start (int, optional): Defaults to 12. Sets the zoom level
    """
    m = folium.Map(location=[df['LATITUDE'].mean(), df['LONGITUDE'].mean()], zoom_start=zoom_start)

    for index, row in df.iterrows():
        folium.CircleMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            radius=row['VIOLATIONS'] / 10,  # Adjust radius scaling as needed
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.6,
            popup=f"Intersection: {row['INTERSECTION']}, Violations: {row['VIOLATIONS']}"
        ).add_to(m)

    m.save(output_file)
