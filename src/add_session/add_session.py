from flask import Blueprint, render_template, request
from datetime import datetime

from src.add_session.fileio import write_entry_to_file
from src.enum import Seeing, Transparency, MoonPhase, WindDirection
from src import app


add_session_bp = Blueprint('add_session',  __name__, url_prefix='/add_session', template_folder='templates', static_folder='static')

@add_session_bp.route("/add_session.html", methods=["POST", "GET"])
def add_session():
    app.logger.debug('Loading add session page.')

    from src import DF

    if request.method == "POST":
        form = request.form.to_dict()
        write_entry_to_file(form)
        app.config["RELOAD_HEATMAP"] = True
        app.logger.info(f'Created a session for {form["start-time"]}.')

    return render_template("add_session/add_session.html", 
                           transparency=[t.value for t in Transparency], 
                           seeing=[s.value for s in Seeing],
                           moon_phases=[m.value for m in MoonPhase], 
                           wind_directions=[w.value for w in WindDirection], 
                           now=str(datetime.now())[:16]) # cut off seconds for datetime