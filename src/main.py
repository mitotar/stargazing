from bokeh.plotting import figure, show, curdoc, row, column
from bokeh.models import Div

import data
from components.component import Component, SmallComponent
from components.year_heatmap import YearHeatmap
from components.object_search import ObjectSearch
from components.stats_table import StatsTable
from components.column_summary import ColumnSummary
from components.frequency_table import FrequencyTable


def test():
    d = Div()
    d.text = "<p style=\"color:blue\"> testing < /p>"

    curdoc().add_root(d)


def dashboard():
    filepath = "../entries.csv"
    df = data.load_data(filepath)

    yh = YearHeatmap(df)
    os = ObjectSearch(df)
    st = StatsTable(df)
    ft = FrequencyTable(df)
    cs = ColumnSummary(df)
    hl = SmallComponent("---------------------------------------------------------------------")

    col1 = column(row(ft.plot, st.plot), yh.plot)
    col2 = column(os.plot, hl.plot, cs.plot)
    curdoc().add_root(row(col1, col2))


dashboard()