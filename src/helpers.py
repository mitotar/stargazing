import pandas as pd
import datetime as dt

def convert_timedelta(time):
    """Extracts the number of days, hours and seconds from a TimeDelta object.

    Args:
        time (TimeDelta): TimeDelta object.

    Returns:
        int[]: List of hours, minutes, seconds.
    """

    return [time.days, time.seconds//3600, (time.seconds//60)%60]