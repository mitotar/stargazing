import pandas as pd
import datetime as dt

import helpers
from converters import convert_transparency_seeing_to_int


__DF = None # store dataframe at class level to avoid having to pass it as a parameter to each function

def load_data(filepath):
    """Transforms the CSV file into a DataFrame. Adds new columns for session duration and number of objects seen not included in the CSV file.

    Args:
        filepath (string): Path to CSV file.
    """
    global __DF

    __DF = pd.read_csv(filepath, sep=';', header=0)
    __DF["start_time"] = pd.to_datetime(__DF["start_time"])
    __DF["end_time"] = pd.to_datetime(__DF["end_time"])
    __DF["date"] = __DF.start_time.dt.strftime("%B %d, %Y")
    __DF["duration"] = __DF.end_time - __DF.start_time
    __DF["number_of_objects"] = __DF.objects.apply(lambda x: len(x.split(',')) if pd.notnull(x) else 0)
    __DF[["objects"]] = __DF[["objects"]].fillna(value="None")
    # if feels_like_temperature is not available, use value from temperature column
    # makes things easier later one when doing other temperature manipulations
    __DF["feels_like_temperature"] = __DF["feels_like_temperature"].fillna(__DF["temperature"])

    __DF.set_index("start_time", inplace=True, drop=False) # need to keep column for future calculations
    __DF.index.names = ["index"] # need to rename to avoid problems converting to ColumnDataSource when plotting heatmap

    return __DF


def get_resample_count_by_string(freq):
    """Resamples the DataFrame according to the provided frequency, and aggregates by count.

    Args:
        freq (string): Resampling frequency.

    Returns:
        DataFrame: Resampled DataFrame, with index year and column count.
    """

    resampled = __DF.resample(freq).count() # sets index to start_time
    resampled["Year"] = resampled.index.year
    resampled["Number of Sessions"] = resampled.number_of_objects # choose this column to get count since it should always be populated
    resampled = resampled[["Year", "Number of Sessions"]]
    resampled.set_index("Year", inplace=True)

    return resampled

def sql_search(query):
    return __DF.read_sql_query(query, parse_dates=["start_time", "end_time"])

if __name__ == "__main__":
    pass