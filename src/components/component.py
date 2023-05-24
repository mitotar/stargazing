from bokeh.models import ColumnDataSource, Div
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.plotting import figure, show
import pandas as pd
import collections

from helpers import extract_timedelta_string, create_duration_string


class Component:
    """Base class for all components of the dashboard.
    """

    def __init__(self, df):
        self._df = Component._prepare_data()

    @classmethod
    def _prepare_data(cls, df_raw):
        return df_raw.copy()
    
    def _create(self):
        raise NotImplementedError("Child class method should be used instead.")
    



# small component classes
class SmallComponent:
    """_summary_
    """

    def __init__(self, text):
        self._text = SmallComponent._prepare_data(text)
        self.plot = self._create()

    @classmethod
    def _prepare_data(cls, s):
        return "<br />" + s + "<br />"

    def _create(self):
        d = Div()
        d.text = self._text

        return d