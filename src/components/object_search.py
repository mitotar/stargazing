import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, curdoc
from bokeh.transform import linear_cmap
from bokeh.models import LinearColorMapper, FixedTicker, ColorBar, TextInput, Div
from bokeh.layouts import column, gridplot
from bokeh.palettes import Blues6
from functools import partial

from components.component import Component
from converters import MONTH_LABELS, convert_transparency_seeing_to_int
import helpers


class ObjectSearch(Component):
    """
    """

    def __init__(self, df):
        self._df = ObjectSearch._prepare_data(df)
        self.plot = self._create()


    @classmethod
    def _prepare_data(cls, df_raw):
        """Prepares DataFrame to be searched.

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
        self._text_input = TextInput(title="Search for object")
        self._text_input.on_change("value", self._display_search_results)
        self._div = Div()

        return column(self._text_input, self._div)


    #region Helpers

    def _search_by_objects(self, object):
        return self._df[self._df["objects"].astype(str).str.contains(object)]


    def _display_search_results(self, attr, old, new):
        results = self._search_by_objects(new)
        self._div.text = "<br />".join(results.index.strftime("%B %-d, %Y").to_list())

    #endregion


    if __name__ == "__main__":
        pass
