import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, curdoc
from bokeh.transform import linear_cmap
from bokeh.models import LinearColorMapper, FixedTicker, ColorBar
from bokeh.layouts import column, gridplot
from bokeh.palettes import Blues6

from components.component import Component
from converters import MONTH_LABELS, convert_transparency_seeing_to_int
import helpers


class YearHeatmap(Component): 
    """
    """

    def __init__(self, df):
        self._df = YearHeatmap._prepare_data(df)
        self.plot = self._create()


    @classmethod
    def _prepare_data(cls, df_raw):
        """Prepares DataFrame to be turned into heat maps.

        Args:
            df (DataFrame): Raw DataFrame, as returned by data.load_data().

        Returns:
            DataFrame: DataFrame to be used for heat maps.
        """

        df = df_raw.copy()
        df["year"] = df.index.year
        df["month"] = df.index.month
        df["day"] = df.index.day
        df["conditions"] = df.apply(lambda x: convert_transparency_seeing_to_int(x.seeing) + convert_transparency_seeing_to_int(x.transparency), axis=1)
        df["duration_string"] = df.apply(lambda x: helpers.create_duration_string(x.start_time, x.end_time), axis=1)

        return df


    def _create(self):
        """Creates a grid of all yearly heat maps.
        """

        years = set(self._df.year)

        plots = [self._create_year_heatmap(str(x)) for x in years]
        grid = [[x, None] for x in plots]
        
        # curdoc().theme = 'dark_minimal'
        
        return gridplot(grid, toolbar_location=None)


    #region Helpers

    def _create_year_heatmap(self, year):
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
            ("Moon phase", "@moon_phase"),
            ("Objects", "@objects")
        ]

        p = figure(x_range=(0.5, 31.5), y_range=(0.5, 12.5), width=1000, height=350, min_border=50, active_drag=None, toolbar_location=None, tooltips=tooltips)
        p.title.text = year
        p.title.text_font_size = "20pt"
        p.title.align = "center"

        # shift grid lines by 0.5 to create grid of boxes...
        p.grid.ticker = FixedTicker(ticks=[x + 0.5 for x in range(1, 13)])
        p.grid.ticker = FixedTicker(ticks=[x + 0.5 for x in range(1, 32)])
        # ...but display tick labels in the middle
        p.yaxis.ticker = FixedTicker(ticks=[x for x in range(1, 13)])
        p.xaxis.ticker = FixedTicker(ticks=[x for x in range(1, 32)])

        p.yaxis.major_label_overrides = MONTH_LABELS
        p.grid.grid_line_color = None
        p.axis.axis_line_color = None
        p.axis.major_tick_line_color = None

        # get min and max from entire data set so all years are on same color scale
        color_min = self._df.conditions.min()
        color_max = self._df.conditions.max()
        mapper = linear_cmap(field_name="conditions", palette=list(reversed(Blues6))[:-1], low=color_min, high=color_max, nan_color="#abb2b9")
        p.rect(x="day", y="month", color=mapper, line_color=None, height=1, width=1, source=self._df.loc[year])

        color_bar = ColorBar(color_mapper=mapper["transform"], title="Conditions", location=(0,0), border_line_color=None, ticker=FixedTicker(ticks=[color_min, color_max]), major_tick_line_color=None, major_label_overrides={int(color_min): "Poor", int(color_max): "Excellent"}) # for some reason need to cast tick values to int
        p.add_layout(color_bar, "right")

        return p

    #endregion

    if __name__ == "__main__":
        pass
