from flask import Blueprint, render_template, request
import time
import string

from src.objects.objects_table import group_objects, get_object_category, OBJECT_CATEGORIES
from src.objects.object_form import ObjectForm
from src import app


objects_bp = Blueprint('objects',  __name__, url_prefix='/objects', template_folder='templates', static_folder='static')
_MESSIER_CATEGORY = "Messier Catalogue"
_NCG_CATEGORY = "New General Catalogue"
_SSO_CATEGORY = "Solar System Objects"
_OTHER_CATEGORY = "Other Objects"

@objects_bp.route("/objects.html", methods=["POST", "GET"])
def objects():
    app.logger.debug('Loading objects page.')

    from src import DF

    start = time.time()
    (objects, counts) = group_objects(DF) # ({messier, ngc, sso, other}, all)
    end = time.time()
    app.logger.debug(f'It took {((end - start) * 1000):.2f} ms to group objects.')

    dates = []
    object = ""
    form = ObjectForm(counts.keys())
    if request.method == "POST":
        object = form.object.data
        if not form.validate_on_submit():
            app.logger.debug(f'\'{object}\' is not a known object.')
        else:
            category = get_object_category(object)
            if category == _SSO_CATEGORY and object.lower() != 'iss' or category == _OTHER_CATEGORY:
                object = string.capwords(object)
            else:
                object = object.upper()

            app.logger.debug(f'Getting dates for object \'{object}\'.')
            dates = objects[category][object]

    return render_template("objects/objects.html", form=form, objects=objects, categories=OBJECT_CATEGORIES, dates=dates, object=object, counts=counts)
