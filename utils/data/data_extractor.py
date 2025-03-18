import requests
import os
import pandas as pd

def save_csv_response(url:str, filepath:str, force:bool=False)->pd.DataFrame:
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
            return pd.read_csv(filepath)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching or saving CSV: {e}")
            return None
        except IOError as e:
            print(f"Error writing to file: {e}")
            return None
    else:
        # not force and the file is already there - voila
        return pd.read_csv(filepath)




