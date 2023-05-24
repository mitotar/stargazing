from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.plotting import figure, show
import pandas as pd
import collections

from components.component import Component
from helpers import extract_timedelta_string, create_duration_string


class StatsTable(Component):
    """
    """

    def __init__(self, df):
        self._df = StatsTable._prepare_data(df)
        self.plot = self._create()


    def _create(self):
        """ 
        """

        duration = self._calculate_longest_session()
        objs = self._calculate_most_objects_seen()
        obj_counts = self._calculate_object_counts()
        coldest = self._calculate_coldest_temp()
        warmest = self._calculate_warmest_temp()
        
        labels = [
            "Longest session", 
            "Most objects seen",
            "Total objects seen",
            "Most seen object",
            "Coldest session", 
            "Warmest session"
        ]
        data = [
            duration[1] + " on " + duration[0], # Longest session
            objs[1] + " on " + objs[0], # Most objects seen
            len(obj_counts), # Total objects seen
            obj_counts.most_common(1)[0][0] + ", " + str(obj_counts.most_common(1)[0][1]) + " times", # Most seen object
            coldest[1] + " on " + coldest[0], # Coldest session
            warmest[1] + " on " + warmest[0] # Warmest session
        ]

        source = ColumnDataSource(data=dict(labels=labels, data=data))
        columns = [
            TableColumn(field="labels"),
            TableColumn(field="data")
        ]

        table = DataTable(source=source, columns=columns, width=500, height=280, index_position=None, header_row=False)

        return table


    #region Helpers

    def _calculate_longest_session(self):
        longest_date = self._df.duration.idxmax().strftime("%B %-d, %Y")
        longest_duration = extract_timedelta_string(self._df.duration.max())

        return [longest_date, longest_duration]


    def _calculate_most_objects_seen(self):
        most_objects_date = self._df.number_of_objects.idxmax().strftime("%B %-d, %Y")
        most_objects_num = str(self._df.number_of_objects.max())

        return [most_objects_date, most_objects_num]


    def _calculate_coldest_temp(self):
        """Calculates the coldest temperature in the DataFrame. A separate function is needed instead of taking the minimum value of the column, because some rows do not have a value in the feels_like_temperature column, so in those cases we take the temperature column value.
        """

        min_date = self._df.feels_like_temperature.idxmin().strftime("%B %-d, %Y")
        min_temp = str(self._df.feels_like_temperature.min()) + "°C"

        return [min_date, min_temp]


    def _calculate_warmest_temp(self):
        """Calculates the warmest temperature in the DataFrame. A separate function is needed instead of taking the minimum value of the column, because some rows do not have a value in the feels_like_temperature column, so in those cases we take the temperature column value.
        """

        max_date = self._df.feels_like_temperature.idxmax().strftime("%B %-d, %Y")
        max_temp = str(self._df.feels_like_temperature.max()) + "°C"

        return [max_date, max_temp]
    

    def _calculate_object_counts(self):
        """_summary_
        """

        objects = self._df.objects.tolist()
        objects = [x.split(", ") for x in objects if not pd.isna(x)]
        objects = [obj for sub in objects for obj in sub if not obj == "None"]

        return collections.Counter(objects)

    #endregion


    if __name__ == "__main__":
        pass
