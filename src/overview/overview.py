from flask import Blueprint, render_template
import os

from src.overview.year_heatmap import create_calendar_heatmaps
from src.overview.frequency_table import create_frequency_table
from src.overview.stats_table import create_stats_table
from src import app

overview_bp = Blueprint('overview',  __name__, url_prefix='/', template_folder='templates', static_folder='static')

def _create_components():
    heatmap_html_exists = os.path.isfile('src/overview/templates/overview/_calendars.html')
    return app.config["RELOAD_HEATMAP"] or not heatmap_html_exists


@overview_bp.route("/", methods=["POST", "GET"])
def overview():
    app.logger.debug('Loading overview page.')
    
    from src import DF

    obj_res = ""
    col_res = ""

    if _create_components():
        app.logger.debug('Recreating heatmap.')
        create_calendar_heatmaps(DF)  # create bokeh html file
        app.config["RELOAD_HEATMAP"] = False

    _freq_table = create_frequency_table(DF)
    _stats_table = create_stats_table(DF)

    return render_template("overview/overview.html", search_object_results=obj_res, search_column_results=col_res, freq_table=_freq_table, stats_table=_stats_table)
