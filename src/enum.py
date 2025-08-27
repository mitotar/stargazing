from enum import Enum, EnumMeta


class NoneValueEnumMeta(EnumMeta):
    def __getitem__(cls, name):
        try:
            return super().__getitem__(name)
        except KeyError:
            return cls.NONE

    def __getattr__(cls, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            return cls.NONE


class Transparency(Enum, metaclass=NoneValueEnumMeta):
    def __str__(self):
        return self.name.lower().replace('_', ' ')

    NONE = 0
    CLOUDY = 1
    POOR = 2
    BELOW_AVERAGE = 3
    AVERAGE = 4
    ABOVE_AVERAGE = 5
    EXCELLENT = 6


class Seeing(Enum, metaclass=NoneValueEnumMeta):
    def __str__(self):
        return self.name.lower().replace('_', ' ')

    NONE = 0
    CLOUDY = 1
    POOR = 2
    BELOW_AVERAGE = 3
    AVERAGE = 4
    ABOVE_AVERAGE = 5
    EXCELLENT = 6


class MoonPhase(Enum, metaclass=NoneValueEnumMeta):
    def __str__(self):
        return self.name.lower().replace('_', ' ')

    NONE = 0
    NEW = 1
    WAXING_CRESCENT = 2
    FIRST_QUARTER = 3
    WAXING_GIBBOUS = 4
    FULL = 5
    WANING_CRESCENT = 6
    LAST_QUARTER = 7
    WANING_GIBBOUS = 8


class Month(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


class WindDirection(Enum, metaclass=NoneValueEnumMeta):
    NONE = 0
    N = 1
    NE = 2
    E = 3
    SE = 4
    S = 5
    SW = 6
    W = 7
    NW = 8


if __name__ == "__main__":
    pass
