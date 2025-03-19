import requests
import os
import pandas as pd

#const_src_url = "https://data.cityofchicago.org/api/views/hhkd-xvj4/rows.csv?accessType=DOWNLOAD"
#const_storage_file ="assets/data/chicago_red_light_cameras.csv"

def get_chicago_dataset(url:str='https://data.cityofchicago.org/api/views/hhkd-xvj4/rows.csv?accessType=DOWNLOAD',
                        filepath:str='assets/data/chicago_red_light_cameras.csv',
                        force:bool=False)->pd.DataFrame:
    """
    Gets a CSV dataset via the url

    Args:
        url (str): The URL of the CSV file.
        filepath (str): The path to save the CSV file.
        force (bool): If True, overwrite existing file. If False, skip download if file exists.
    Returns:
        A pandas DataFrame containing the CSV file content
    """

    # only delete the file on force and it exists
    if os.path.exists(filepath) and force==True:
        try:
            os.remove(filepath)
            print(f"Existing file {filepath} deleted.")
        except OSError as e:
            print(f"Error deleting existing file: {e}")

    # if the file does exist locally - we will go grab it
    if not os.path.exists(filepath):
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"CSV saved to {filepath}")
            return format_data(pd.read_csv(filepath))

        except requests.exceptions.RequestException as e:
            print(f"Error fetching or saving CSV: {e}")
            return None
        except IOError as e:
            print(f"Error writing to file: {e}")
            return None
    else:
        # not force and the file is already there - voila
        return format_data(pd.read_csv(filepath))


def format_data(df:pd.DataFrame)->pd.DataFrame:
    """
        Args:
            df: passed in dataframe to evaluate and further transform.
        Returns:
            transformed copy of the dataframe
    """
    # one column as imported in the csv is 'CAMERA ID' rename to 'CAMERA_ID'
    df_copy = df.copy()
    
    df_copy['CAMERA_ID'] = df_copy['CAMERA ID']
    df.drop('CAMERA ID', axis=1, inplace=True)
    df_copy['VIOLATION_DATE'] = pd.to_datetime(df_copy['VIOLATION DATE'])
    df.drop('VIOLATION DATE', axis=1, inplace=True)

    df_copy['VIOLATIONS_NUMERIC'] = pd.to_numeric(df_copy['VIOLATIONS'], errors='coerce')

    df_copy['YEAR'] = df_copy['VIOLATION_DATE'] .dt.year
    df_copy['DAY_NAME'] = df_copy['VIOLATION_DATE'] .dt.day_name()
    df_copy['MONTH_NAME'] = df_copy['VIOLATION_DATE'].dt.month_name()
    
    return df_copy

