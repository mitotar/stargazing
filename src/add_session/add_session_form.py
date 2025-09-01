from wtforms import Form, IntegerField, SelectField, StringField, DateTimeField, validators, ValidationError
from flask_wtf import FlaskForm
from datetime import datetime

from src.enum import Transparency, Seeing, MoonPhase, WindDirection


def greater_than_zero_field_validator(allow_zero=False):
    error = f'Value must be greater than {'or equal to ' if allow_zero else ''}zero.'

    def _greater_than_zero_field_validator(form, field):
        if field.data < 0:
            raise ValidationError(error)
        if not allow_zero and field.data == 0:
            raise ValidationError(error)
        
    return _greater_than_zero_field_validator
    

class AddSessionForm(FlaskForm):
    location = StringField('Location', default='backyard', validators=[validators.Optional()])
    cloud_cover = IntegerField('Cloud cover', validators=[validators.NumberRange(0, 100), validators.Optional()])
    transparency = SelectField('Transparency', choices=[(x.value, x.name) for x in Transparency], default=Transparency.NONE, validators=[validators.Optional()])
    seeing = SelectField('Seeing', choices=[(x.value, x.name) for x in Seeing], default=Seeing.NONE, validators=[validators.Optional()])
    moon_phase = SelectField('Moon phase', choices=[(x.value, x.name) for x in MoonPhase], default=MoonPhase.NONE, validators=[validators.Optional()])
    moon_age = IntegerField('Moon age', validators=[validators.NumberRange(0, 29), validators.Optional()])
    start_time = DateTimeField('Start time', format='%Y-%m-%d %H:%M', default=datetime.now(), validators=[validators.InputRequired()])
    end_time = DateTimeField('End time', format='%Y-%m-%d %H:%M', default=datetime.now(), validators=[validators.InputRequired()])
    wind_speed = IntegerField('Wind speed', validators=[validators.Optional()])
    wind_direction = SelectField('Wind direction', choices=[(x.value, x.name) for x in WindDirection], default=WindDirection.NONE, validators=[validators.Optional()])
    temperature = IntegerField('Temperature', validators=[validators.Optional()])
    temperature_feels_like = IntegerField('Feels like', validators=[validators.Optional()])
    dew_point = IntegerField('Dew point', validators=[validators.Optional()])
    objects = StringField('Objects', validators=[validators.Optional()])


    def validate_wind_speed(form, field):
        """
        Validate wind speed is greater than 0.
        """
        if field.data < 0:
            raise ValidationError('Wind speed must be greater than 0.')
        
        # return True


    def validate_end_time(form, field):
        """
        Validate end time is after and not equal to start time.
        """
        # need to disregard seconds or start time will always come before
        start_time = form.start_time.data.replace(second=0).replace(microsecond=0)
        end_time = field.data.replace(second=0).replace(microsecond=0)
        if start_time >= end_time:
            raise ValidationError('End time must be after and not equal to the start time.')
