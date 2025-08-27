import pandas as pd


def extract_timedelta(time):
    """Extracts the number of days, hours and seconds from a TimeDelta object.

    Args:
        time (TimeDelta): TimeDelta object.

    Returns:
        int[]: List of hours, minutes, seconds.
    """

    return [time.days, time.seconds//3600, (time.seconds//60)%60]


def extract_timedelta_string(time):
    """String of TimeDelta object broken down in days, hours, minutes.

    Args:
        time (TimeDelta): Time to turn into string.

    Returns:
        string: String of TimeDelta.
    """

    time = extract_timedelta(time)

    days = "{} days, ".format(time[0]) if time[0] > 0 else ""
    hours = "{} hours, ".format(time[1]) if time[1] > 0 else ""
    minutes = "{} minutes".format(time[2]) if time[2] > 0 else "0 minutes"

    return days + hours + minutes

def create_duration_string(start, end):
    """Creates string of start/end times, and duration.

    Args:
        start (DateTime): Start time.
        end (DateTime): End time.

    Returns:
        string: Time and duration string.
    """

    extract = True
    if pd.isnull(start):
        extract = False
        start = "???"
    if pd.isnull(end):
        extract = False
        end = "???"

    if extract:
        duration = extract_timedelta_string(end - start)
        return "{0} - {1} ({2})".format(start.strftime("%H:%M"), end.strftime("%H:%M"), duration)

    start = start if start == "???" else start.strftime("%H:%M")
    end = end if end == "???" else end.strftime("%H:%M")
    return "{0} - {1}".format(str(start), str(end))


if __name__ == "__main__":
    pass