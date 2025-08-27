import re
from collections import defaultdict, OrderedDict, Counter


_SOLAR_SYSTEM_OBJECTS = ["Ceres", "ISS", "Jupiter", "Mars", "Mercury",
                         "Moon", "Neptune", "Pluto", "Saturn", "Sun", "Uranus", "Venus"]
_MESSIER_REGEX = r"M\d{1,3}"
_NGC_REGEX = r"NGC \d{3,4}"


def create_objects_table(df_raw):
    df = df_raw[["date", "objects"]]

    return _collect_all_objects(df)


def get_object_category(object):
    if re.match(_MESSIER_REGEX, object, re.IGNORECASE):
        return 0
    elif re.match(_NGC_REGEX, object, re.IGNORECASE):
        return 1
    elif str(object).lower() in (name.lower() for name in _SOLAR_SYSTEM_OBJECTS):
        return 2
    else:
        return 3


def _collect_all_objects(df):
    messier = defaultdict(list)
    ngc = defaultdict(list)
    sso = defaultdict(list)
    other = defaultdict(list)

    all = []

    for _, row in df.iterrows():
        objects = row["objects"].split(", ") if isinstance(
            row["objects"], str) else ""  # don't count NaN values
        for o in objects:
            # for messier and NGC we only keep the number to sort list in html as int instead of string
            if re.match(_MESSIER_REGEX, o):
                num = int(re.findall(r'\d+', o)[0])
                messier[num].append(row["date"])
            elif re.match(_NGC_REGEX, o):
                num = int(re.findall(r'\d+', o)[0])
                ngc[num].append(row["date"])
            elif o in _SOLAR_SYSTEM_OBJECTS:
                sso[o].append(row["date"])
            else:
                other[o].append(row["date"])

            all.append(o)

    messier = OrderedDict(sorted(messier.items()))
    ngc = OrderedDict(sorted(ngc.items()))
    sso = OrderedDict(sorted(sso.items()))
    other = OrderedDict(sorted(other.items()))

    messier = {"M" + str(k): v for k, v in messier.items()}
    ngc = {"NGC " + str(k): v for k, v in ngc.items()}

    return [messier, ngc, sso, other, Counter(all)]


if __name__ == "__main__":
    pass
