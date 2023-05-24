from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.plotting import figure, show
import pandas as pd
import collections

from components.component import Component
from helpers import extract_timedelta_string, create_duration_string


class FrequencyTable(Component):
    """
    """

    def __init__(self, df):
        self._df = FrequencyTable._prepare_data(df)
        self.plot = self._create()


    def _create(self):
        df_count = self._df.resample("Y").count()

        years = [x.strftime("%Y") for x in df_count.index]
        counts = [df_count.loc[x].number_of_objects.values[0] for x in years]
        # start = [df_count.loc[x].start.values[0] for x in years]
        # end = [df_count.loc[x].end.values[0] for x in years]
        # duration = [create_duration_string(start[i], end[i]) for i in len(counts)]
              
        years.append("Total")
        counts.append(sum(counts))

        source = ColumnDataSource(data=dict(labels=years, data=counts))
        columns = [
            TableColumn(field="labels", title="Year"),
            TableColumn(field="data", title="Number of sessions")
        ]

        table = DataTable(source=source, columns=columns, width=250, height=280, index_position=None, header_row=True)
        
        return table
    

    if __name__ == "__main__":
        pass
