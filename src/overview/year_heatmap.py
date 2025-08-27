from bokeh.plotting import figure, output_file, save
from bokeh.transform import linear_cmap
from bokeh.models import FixedTicker, ColorBar
from bokeh.layouts import gridplot
from bokeh.palettes import Blues6

from src.enum import Month


def create_calendar_heatmaps(df):
    """Creates a grid of all yearly heat maps.
    """

    years = sorted(set(df.year), reverse=True)

    plots = [_create_year_heatmap(df, str(x)) for x in years]
    grid = [[x, None] for x in plots]
    plot = gridplot(grid, toolbar_location=None)

    file = "src/overview/templates/overview/_calendars.html"

    output_file(filename=file)
    save(plot)

    return


def _create_year_heatmap(df, year):
    """Creates heat map from the given DataFrame, for the given year.

    Args:
        year (string): Year of heat map.

    Returns:
        Figure: Bokeh Figure of heat map.
    """

    tooltips = [
        ("Date", "@date"),
        ("Time", "@duration_string"),
        ("Temperature", "@{feels_like_temperature}°C"),
        ("Seeing", "@seeing"),
        ("Transparency", "@transparency"),
        # ("Moon phase", "@moon_phase"),
        # ("Wind speed", "@{wind_speed} km/h @{wind_direction}"),
        ("Objects", "@objects")
    ]

    p = figure(x_range=(0.5, 31.5), y_range=(0.5, 12.5), width=1000, height=350,
               min_border=50, active_drag=None, toolbar_location=None, tooltips=tooltips)
    p.title.text = year
    p.title.text_font_size = "20pt"
    p.title.align = "center"

    # shift grid lines by 0.5 to create grid of boxes...
    p.grid.ticker = FixedTicker(ticks=[x + 0.5 for x in range(1, 13)])
    p.grid.ticker = FixedTicker(ticks=[x + 0.5 for x in range(1, 32)])
    # ...but display tick labels in the middle
    p.yaxis.ticker = FixedTicker(ticks=[x for x in range(1, 13)])
    p.xaxis.ticker = FixedTicker(ticks=[x for x in range(1, 32)])

    p.yaxis.major_label_overrides = dict(zip([m.value for m in Month], [str(m.name).title() for m in Month]))
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None

    # p.background_fill_color = "#eaecee"
    p.border_fill_color = "#eaecee"

    # get min and max from entire data set so all years are on same color scale
    color_min = df.conditions.min()
    color_max = df.conditions.max()
    mapper = linear_cmap(field_name="conditions", palette=list(reversed(Blues6))[
                         :-1], low=color_min, high=color_max, nan_color="#abb2b9")
    p.rect(x="day", y="month", color=mapper, line_color=None,
           height=1, width=1, source=df.loc[year])

    color_bar = ColorBar(color_mapper=mapper["transform"], title="Conditions", location=(0, 0), border_line_color=None, ticker=FixedTicker(ticks=[
                         color_min, color_max]), major_tick_line_color=None, major_label_overrides={int(color_min): "Poor", int(color_max): "Excellent"})  # for some reason need to cast tick values to int
    color_bar.background_fill_color = "#eaecee"
    p.add_layout(color_bar, "right")

    return p


if __name__ == "__main__":
    pass
