from flask import Blueprint, render_template, request

from src.objects.objects_table import create_objects_table, get_object_category
from src import app


objects_bp = Blueprint('objects',  __name__, url_prefix='/objects', template_folder='templates', static_folder='static')

@objects_bp.route("/objects.html", methods=["POST", "GET"])
def objects():
    app.logger.debug('Loading objects page.')

    from src import DF

    objects = create_objects_table(DF)
    names = ["Messier Catalogue", "New General Catalogue",
             "Solar System Objects", "Other Objects"]

    dates = []
    object = ""
    if request.method == "POST":
        object = request.form["object"]
        object_type = get_object_category(object)
        dates = objects[object_type].get(object, ["Object not found."])
        object = object + ":"

    return render_template("objects/objects.html", objects=objects[:-1], names=names, dates=dates, object=object, counts=objects[-1])
