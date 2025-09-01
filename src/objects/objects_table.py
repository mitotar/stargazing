import re
from collections import defaultdict, OrderedDict, Counter

OBJECT_CATEGORIES = ["Messier Catalogue", "New General Catalogue", "Solar System Objects", "Other Objects"]
_SOLAR_SYSTEM_OBJECTS = ["Ceres", "ISS", "Jupiter", "Mars", "Mercury",
                         "Moon", "Neptune", "Pluto", "Saturn", "Sun", "Uranus", "Venus"]
_MESSIER_REGEX = r"M\d{1,3}"
_NGC_REGEX = r"NGC \d{3,4}"


def group_objects(df):
    df = df[["date", "objects"]]

    messier = defaultdict(list)
    ngc = defaultdict(list)
    sso = defaultdict(list)
    other = defaultdict(list)

    all = []

    for _, row in df.iterrows():
        objects = row["objects"].split(", ") if isinstance(row["objects"], str) else ""  # don't count NaN values
        for o in objects:
            # for messier and NGC we only keep the number to sort list in html as int instead of string
            if re.match(_MESSIER_REGEX, o):
                messier[o].append(row["date"])
            elif re.match(_NGC_REGEX, o):
                ngc[o].append(row["date"])
            elif o in _SOLAR_SYSTEM_OBJECTS:
                sso[o].append(row["date"])
            else:
                other[o].append(row["date"])

            all.append(o)

    messier = OrderedDict(sorted(messier.items(), key=lambda x: int(x[0][1:])))
    ngc = OrderedDict(sorted(ngc.items(), key=lambda x: int(x[0][4:])))
    sso = OrderedDict(sorted(sso.items()))
    other = OrderedDict(sorted(other.items()))

    return ({OBJECT_CATEGORIES[0]: messier,
             OBJECT_CATEGORIES[1]: ngc,
             OBJECT_CATEGORIES[2]: sso,
             OBJECT_CATEGORIES[3]: other}, Counter(all))


def get_object_category(object):
    if re.match(_MESSIER_REGEX, object, re.IGNORECASE):
        return OBJECT_CATEGORIES[0]
    elif re.match(_NGC_REGEX, object, re.IGNORECASE):
        return OBJECT_CATEGORIES[1]
    elif str(object).lower() in (name.lower() for name in _SOLAR_SYSTEM_OBJECTS):
        return OBJECT_CATEGORIES[2]
    else:
        return OBJECT_CATEGORIES[3]


if __name__ == "__main__":
    pass
