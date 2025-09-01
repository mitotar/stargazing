from datetime import datetime


def write_entry_to_file(form, file):
    line = _create_line(form)
    with open(file, "a") as f:
        f.write("\n" + line)


def _create_line(form):
    # need to remove seconds to avoid ValueError
    start_time = form["start_time"]
    end_time = form["end_time"]

    # convert string to datetime to make sure it's valid, then convert back to string
    start_time = datetime.strptime(
        start_time, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
    end_time = datetime.strptime(
        end_time, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")

    location = form["location"] if form["location"] else ""
    cloud_cover = str(int(form["cloud_cover"])) if form["cloud_cover"] else ""
    transparency = form["transparency"] if form["transparency"] else ""
    seeing = form["seeing"] if form["seeing"] else ""
    moon_phase = form["moon_phase"] if form["moon_phase"] else ""
    wind_speed = str(int(form["wind_speed"])) if form["wind_speed"] else ""
    wind_direction = form["wind_direction"] if form["wind_direction"] else ""
    temperature = str(int(form["temperature"])) if form["temperature"] else ""
    feels_like = str(int(form["temperature_feels_like"])) if form["temperature_feels_like"] else ""
    dew_point = str(int(form["dew_point"])) if form["dew_point"] else ""
    objects = form["objects"] if form["objects"] else ""

    return ";".join([start_time, end_time, location, cloud_cover, transparency, seeing, moon_phase, wind_speed, wind_direction, temperature, feels_like, dew_point, objects])
