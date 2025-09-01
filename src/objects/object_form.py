from wtforms import StringField, ValidationError
from flask_wtf import FlaskForm


class ObjectForm(FlaskForm):
    def __init__(self, objects, **kwargs):
        self.objects = [o.lower() for o in objects]
        super().__init__(**kwargs)

    object = StringField('Objects')

    def validate_object(form, field):
        if field.data.lower() not in form.objects:
            raise ValidationError('Object not found.')
