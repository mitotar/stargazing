import pandas as pd
import datetime as dt

import helpers


def load_data(filepath):
    """Transforms the CSV file into a DataFrame. Adds columnss for sessions duration and number of objects seen not included in the CSV file.

    Args:
        filepath (string): Path to CSV file.

    Returns:
        DataFrame: DataFrame of session data.
    """
    
    df = pd.read_csv(filepath, sep=';', header=0, index_col="start_time", parse_dates=["start_time", "end_time"])
    # df.index.name = "start_time" # some reason need to reset the name after setting column as index
    df["duration"] = df.end_time - df.index
    df["number_of_objects"] = df.objects.apply(lambda x: len(x.split(',')) if pd.notnull(x) else 0)

    return df


def calculate_statistics(df):
    num_sessions = df.shape[0]
    longest_date = df.duration.idxmax()
    longest_duration = df.duration.max()
    most_objects_num = df.number_of_objects.max()
    most_objects_date = df.number_of_objects.idxmax()
    coldest_temp = df.temperature.min()
    coldest_temp_date = df.temperature.idxmin()


    print("Total number of sessions: ", num_sessions)
    print("\t", df.resample("Y").count())
    print("Longest session: {0} hours {1} minutes on {2}".format(helpers.convert_timedelta(longest_duration)[1], helpers.convert_timedelta(longest_duration)[2], longest_date))
    print("Most objects seen: {0} on {1}".format(most_objects_num, most_objects_date))
    print("Coldest session: {0} deg. C on {1}".format(coldest_temp, coldest_temp_date))


if __name__ == "__main__":
    filepath = "entries.csv"
    df = load_data(filepath)
    calculate_statistics(df)