from flask import Blueprint, render_template, request

from app import app
from src.data import column_search


search_bp = Blueprint('search',  __name__, url_prefix='/search', template_folder='templates', static_folder='static')

@search_bp.route("/search.html", methods=["POST", "GET"])
def search():
    app.logger.debug('Loading search page.')

    from src import DF

    cols = sorted(DF.columns.tolist())

    col = ""
    col_result = {}
    sql_result = {}
    if request.method == "POST":
        if "col-name" in request.form:
            col = request.form["col-name"]
            if col in cols:
                col_result = column_search(DF, col)
            else:
                col = "Not a valid column name"

    return render_template("search/search.html", columns=cols, col=col, col_result=col_result, sql_result=sql_result)
