from flask import Blueprint, render_template, request, flash
from datetime import datetime

from src.add_session.fileio import write_entry_to_file
from src.add_session.add_session_form import AddSessionForm
from src.enum import Seeing, Transparency, MoonPhase, WindDirection
from src import app


add_session_bp = Blueprint('add_session',  __name__, url_prefix='/add_session', template_folder='templates', static_folder='static')

@add_session_bp.route("/add_session.html", methods=["POST", "GET"])
def add_session():
    app.logger.debug('Loading add session page.')

    form = AddSessionForm()

    if request.method == "POST":
        if not form.validate_on_submit():
            app.logger.debug(f'Session not saved. Invalid entries.')
        else:
            form_data = request.form.to_dict()
            write_entry_to_file(form_data, app.config['CSV_FILE'])
            app.config['RELOAD_HEATMAP'] = True
            app.logger.info(f'Created a session for {form_data["start_time"]}.')
            flash('Session created!', 'success')

    return render_template("add_session/add_session.html", form=form)