import logging
from flask import Flask, logging as flogging
import json

from src.data import load_data


formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
flogging.default_handler.setFormatter(formatter)

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

app.logger.setLevel(level=logging.DEBUG)

app.config.from_file('../config.json', load=json.load)
app.secret_key = app.config['SECRET_KEY']

from src.overview.overview import overview_bp
from src.add_session.add_session import add_session_bp
from src.objects.objects import objects_bp
from src.search.search import search_bp
app.register_blueprint(overview_bp)
app.register_blueprint(add_session_bp)
app.register_blueprint(objects_bp)
app.register_blueprint(search_bp)

app.logger.info('Creating Stargazing app.')

DF = load_data(app.config["CSV_FILE"])