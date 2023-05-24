import re
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, curdoc
from bokeh.transform import linear_cmap
from bokeh.models import LinearColorMapper, FixedTicker, ColorBar, TextInput, Div
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.layouts import column, gridplot
from bokeh.palettes import Blues6
from functools import partial

from components.component import Component
from converters import MONTH_LABELS, convert_transparency_seeing_to_int
import helpers


class ColumnSummary(Component):
    """
    """

    def __init__(self, df):
        self._df = ColumnSummary._prepare_data(df)
        self.plot = self._create()


    def _create(self):
        self._text_input = TextInput(title="Get column summary")
        self._text_input.on_change("value", self._create_column_summary)
        self._table = DataTable()
        self._div = Div()

        return column(self._text_input, self._div)


    #region Helpers

    def _create_column_summary(self, attr, old, new):
        if new == "help":
            self._div.text = "Columns:\n" + str(self._df.columns.tolist())
        elif not new in self._df.columns:
            self._div.text = "Invalid column name. Type \"help\" for column names."
        else:
            results = self._df[new].describe().to_string().split()

            s = ""
            for i in range(len(results)): # replace every second space with newline
                if i % 2 == 0:
                    s += results[i] + " &emsp; "
                elif i % 2 != 0:
                    s += results[i] + "<br />"

            self._div.text = s

    #endregion


    if __name__ == "__main__":
        pass
