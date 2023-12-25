from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField, validators,  SelectField, FormField, IntegerField, FloatField
from wtforms.validators import InputRequired, Email, Optional, Length



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
     """Form for creating new worklog"""

     title = StringField("Type", validators=[InputRequired()])





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


