from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField, validators, SelectField, FormField, IntegerField, FloatField, SelectMultipleField
from wtforms.validators import InputRequired, Email, Optional, Length
from models import WorkoutType

class RegisterForm(FlaskForm):
    """Form for registering a user."""


    email = EmailField("Email", validators=[InputRequired(), Email()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])



class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class NewWorkType(FlaskForm):
     """Form for creating new type of workout"""

     type_name = StringField("Type", validators=[InputRequired()])
     description = TextAreaField('Mailing Address', [validators.optional(), validators.length(max=200)])

class NewExercise(FlaskForm):
     """Form for creating new unique exercise"""

     name = StringField("Type", validators=[InputRequired()])
     description = TextAreaField('Mailing Address', [validators.optional(), validators.length(max=200)])

class NewWorkLog(FlaskForm):
    """Form for creating a new worklog."""

    title = StringField("Title", validators=[InputRequired()])
    workout_type = SelectMultipleField("Workout Type", choices=[], coerce=int)

    def __init__(self, *args, **kwargs):
        super(NewWorkLog, self).__init__(*args, **kwargs)
        self.workout_type.choices = self.load_workout_types()

    @staticmethod
    def load_workout_types():
        """
        Load workout types from the database and add an option
        for adding a new type.
        """
        workout_types = [(wt.id, wt.type_name) for wt in WorkoutType.query.all()]
        return workout_types

class NewExerciseForm(FlaskForm):
    """Sub-form for creating a new exercise within the worklog edit form."""
    name = StringField("Exercise Name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[Optional(), Length(max=200)])

class EditWorkLog(FlaskForm):
    """Form for editing a worklog."""

    title = StringField("Title", validators=[InputRequired()])
    existing_exercise = SelectField("Existing Exercises", coerce=int, choices=[], validators=[Optional()])
    new_exercise = FormField(NewExerciseForm)

class NewSet(FlaskForm):
    weight = FloatField("Weights", validators=[InputRequired()])
    reps = IntegerField("Reps", validators=[InputRequired()])
    rest_time = IntegerField("Rest time", validators=[Optional()])


