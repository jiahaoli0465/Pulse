from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
bcrypt = Bcrypt()
db = SQLAlchemy()



class User(db.Model):
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

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    header_image_url = db.Column(
        db.Text,
        default="/static/images/warbler-hero.jpg"
    )

    bio = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )




    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
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


class Worklog(db.Model):
    """An individual worklog for a day."""

    __tablename__ = 'Worklogs'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

        # Relationship to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='worklogs')
    
    # Relationship to ExerciseToWorklog
    exercises = db.relationship('ExerciseToWorklog', backref='worklog', lazy='dynamic')

class ExerciseSet(db.Model):
    """A set of exercises."""
    __tablename__ = 'exerciseSets'

    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    
    # Foreign Key to ExerciseToWorklog
    exercise_to_worklog_id = db.Column(db.Integer, db.ForeignKey('exerciseToWorklog.id'), nullable=False)

class Exercise(db.Model):
    """An individual exercise."""
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)

class ExerciseToWorklog(db.Model):
    """Relationship between an exercise and a worklog."""
    __tablename__ = 'exerciseToWorklog'

    id = db.Column(db.Integer, primary_key=True)
    worklog_id = db.Column(db.Integer, db.ForeignKey('Worklogs.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    
    # Relationship to ExerciseSet
    sets = db.relationship('ExerciseSet', backref='exercise_to_worklog', lazy='dynamic')





def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
