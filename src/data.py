import pandas as pd
import numpy as np

from src.enum import Transparency, Seeing

def load_data(file):
    """Transforms the CSV file into a DataFrame. Adds new columns for session duration and number of objects seen not included in the CSV file.

    Args:
        filepath (string): Path to CSV file.
    """
    
    df = pd.read_csv(file, sep=';', header=0, parse_dates=['start_time', 'end_time'], date_format='%Y-%m-%d %H:%M')
    # df["start_time"] = pd.to_datetime(df["start_time"])
    # df["end_time"] = pd.to_datetime(df["end_time"])

    # create new columns
    df["date"] = df['start_time'].dt.strftime("%B %-d, %Y")
    df["duration"] = df.end_time - df.start_time
    df["number_of_objects"] = df.objects.apply(
        lambda x: len(x.split(',')) if pd.notnull(x) else 0)
    # df[["objects"]] = df[["objects"]].fillna(value="None")
    # if feels_like_temperature is not available, use value from temperature column
    # makes things easier later when doing other temperature manipulations
    # df["feels_like_temperature"] = df["feels_like_temperature"].fillna(df["temperature"])

    # need to keep column for future calculations
    # need to rename to avoid problems converting to ColumnDataSource when plotting heatmap
    # df.index.names = ["index"]
    df["year"] = df['start_time'].dt.year
    df["month"] = df['start_time'].dt.month
    df["day"] = df['start_time'].dt.day
    df["duration"] = df.apply(
        lambda x: x.start_time - x.end_time, axis=1)

    def _calculate_conditions_value(seeing, transparency):
        """
        Return NaN if no data to correctly color the heatmap
        """
        value = Seeing[seeing].value  + Transparency[transparency].value
        return value if value > 0 else np.nan
    
    df["conditions"] = df.apply(lambda x: _calculate_conditions_value(x.seeing, x.transparency), axis=1)

    df.set_index("start_time", inplace=True, drop=False)
    df.index.name = 'index' # need to rename or heatmap source will throw error

    return df


def column_search(df, column):
    """_summary_

    Args:
        df (DataFrame): DataFrame to search.
        column (string): Column name.

    Returns:
        DataFrame: Results of column describe.
    """

    description = df[column].describe().index.tolist()
    value = df[column].describe().values.tolist()
    results = zip(description, value)

    return results


if __name__ == "__main__":
    pass
