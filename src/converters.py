import pandas as pd
import numpy as np


# values for transparency/seeing and moon phases are as given in the Astropheric app

__TRANSPARENCY_SEEING = {
    "cloudy": 1,
    "poor": 2,
    "below average": 3,
    "average": 6,
    "above average": 8,
    "excellent": 10 
}

__MOON_PHASES = {
    "new moon": 1,
    "waxing crescent": 2,
    "first quarter": 3,
    "waxing gibbous": 4,
    "full moon": 5,
    "waning crescent": 6,
    "last quarter": 7,
    "waning gibbous": 8
}

MONTH_LABELS = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}


def convert_transparency_seeing_to_int(x): 
    return __TRANSPARENCY_SEEING.get(x, np.nan)


def convert_int_to_transparency_seeing(x):
    if x == 0:
        return np.nan 

    for key, val in __TRANSPARENCY_SEEING.items():
        if val == x:
            return key


def convert_moon_phase_to_int(x):
    if pd.isnull(x):
        return 0

    return __MOON_PHASES[x]


def convert_int_to_moon_phase(x):
    if x == 0:
        return np.nan 

    for key, val in __MOON_PHASES.items():
        if val == x:
            return key


if __name__ == "__main__":
    pass