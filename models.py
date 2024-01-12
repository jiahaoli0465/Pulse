from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )



    password = db.Column(
        db.Text,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/defaultPic.png",
    )



    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user


    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class WorkoutType(db.Model):
    __tablename__ = 'workout_types'

    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)

class WorklogWorkoutType(db.Model):
    __tablename__ = 'worklog_workout_type'
    worklog_id = db.Column(db.Integer, db.ForeignKey('worklogs.id'), primary_key=True)
    workout_type_id = db.Column(db.Integer, db.ForeignKey('workout_types.id'), primary_key=True)


    worklog = db.relationship('Worklog', backref=db.backref("worklog_workout_types"))
    workout_type = db.relationship('WorkoutType', backref=db.backref("worklog_workout_types"))


class Worklog(db.Model):
    __tablename__ = 'worklogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='worklogs')
    workout_types = db.relationship('WorkoutType', secondary='worklog_workout_type', backref=db.backref('worklogs', lazy='dynamic'))

    @property
    def friendly_date(self):
        # Format: January 01, 2024 at 12:00 PM
        return self.created_at.strftime('%B %d, %Y at %I:%M %p') 
        
class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    worklog_id = db.Column(db.Integer, db.ForeignKey('worklogs.id'), nullable=False)
    # exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=True)

    worklog = db.relationship('Worklog', backref='workout_exercises')
    # exercise = db.relationship('Exercise', backref='workout_exercises')
    exercise_sets = db.relationship('ExerciseSet', backref='workout_exercise', cascade="all, delete-orphan")



class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique = True)
    description = db.Column(db.Text)

class ExerciseSet(db.Model):
    __tablename__ = 'exercise_sets'

    id = db.Column(db.Integer, primary_key=True)
    workout_exercise_id = db.Column(db.Integer, db.ForeignKey('workout_exercises.id'), nullable=False)
    set_number = db.Column(db.Integer, nullable=False) 
    weight = db.Column(db.Float)
    reps = db.Column(db.Integer)
    # workout_exercise = db.relationship('WorkoutExercise', backref='exercise_sets')


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
