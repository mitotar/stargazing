import pandas as pd
import collections

from src.helpers import extract_timedelta_string


def create_stats_table(df):
    duration = _calculate_longest_session(df)
    objs = _calculate_most_objects_seen(df)
    obj_counts = _calculate_object_counts(df)
    coldest = _calculate_coldest_temp(df)
    warmest = _calculate_warmest_temp(df)
    windiest = _calculate_windiest_temp(df)

    labels = [
        "Longest session",
        "Coldest session",
        "Warmest session",
        "Windiest session",
        "Most objects seen",
        "Total objects seen",
        "Most viewed object"
    ]

    data = [
        duration[1] + " on " + duration[0],  # Longest session
        coldest[1] + " on " + coldest[0],  # Coldest session
        warmest[1] + " on " + warmest[0],  # Warmest session
        windiest[1] + " on " + windiest[0],  # Windiest session]
        objs[1] + " on " + objs[0],  # Most objects seen
        len(obj_counts),  # Total objects seen
        obj_counts.most_common(
            1)[0][0] + ", " + str(obj_counts.most_common(1)[0][1]) + " times"  # Most viewed object
    ]

    return dict(zip(labels, data))


def _calculate_longest_session(df):
    longest_date = df.duration.idxmax().strftime("%B %-d, %Y")
    longest_duration = extract_timedelta_string(df.duration.max())

    return [longest_date, longest_duration]


def _calculate_most_objects_seen(df):
    most_objects_date = df.number_of_objects.idxmax().strftime("%B %-d, %Y")
    most_objects_num = str(df.number_of_objects.max())

    return [most_objects_date, most_objects_num]


def _calculate_coldest_temp(df):
    """Calculates the coldest temperature in the DataFrame. A separate function is needed instead of taking the minimum value of the column, because some rows do not have a value in the feels_like_temperature column, so in those cases we take the temperature column value.
    """

    min_date = df.feels_like_temperature.idxmin().strftime("%B %-d, %Y")
    min_temp = str(int(df.feels_like_temperature.min())) + "°C"

    return [min_date, min_temp]


def _calculate_warmest_temp(df):
    """Calculates the warmest temperature in the DataFrame. A separate function is needed instead of taking the minimum value of the column, because some rows do not have a value in the feels_like_temperature column, so in those cases we take the temperature column value.
    """

    max_date = df.feels_like_temperature.idxmax().strftime("%B %-d, %Y")
    max_temp = str(int(df.feels_like_temperature.max())) + "°C"

    return [max_date, max_temp]


def _calculate_windiest_temp(df):
    max_date = df.wind_speed.idxmax().strftime("%B %-d, %Y")
    max_speed = str(int(df.wind_speed.max())) + " km/h"

    return [max_date, max_speed]


def _calculate_object_counts(df):
    """_summary_
    """

    objects = df.objects.tolist()
    objects = [x.split(", ") for x in objects if not pd.isna(x)]
    objects = [obj for sub in objects for obj in sub]

    return collections.Counter(objects)


if __name__ == "__main__":
    pass
