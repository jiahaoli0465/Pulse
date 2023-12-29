import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from forms import RegisterForm, LoginForm, EditWorkLog, NewExercise, NewWorkLog,NewWorkType
from models import db, connect_db, User, Worklog, WorkoutType, Exercise, ExerciseSet

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///pulse'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#Use the database jeff so u dont have to looool

# # i dont wanna keep making a new account every time i change an html page
# def autosignup():
#     User.signup(
#                 username="a",
#                 password="a",
#                 email="a@a.com",
#     )
#     db.session.commit()
# autosignup()

# #i also cant be bothered to add workout types manually
# def autoworkoutType():
#     db.session.add(WorkoutType(id=0, type_name="new awesome workout type"))
#     db.session.commit()
# autoworkoutType()


@app.route('/')
def show_home():
    users = User.query.all()
    return render_template('home.html', users = users)

@app.route('/form')
def form_page():
    return render_template('form_page.html')

@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def show_dashboard():
    worklogs = Worklog.query.all()
    form = NewWorkLog()

    if form.validate_on_submit():
        title = form.title.data

        worklog = Worklog(title = title, user_id = current_user.id)
        db.session.add(worklog)
        db.session.commit()

        return redirect(url_for('show_dashboard'))
    else:
        return render_template('users/dashboard.html', form = form, worklogs = worklogs)
    
#============== WORKLOG ===================
    
@app.route('/edit_worklog/<int:worklog_id>', methods=['GET', 'POST'])
def edit_worklog(worklog_id):
    form = EditWorkLog()
    
    # Populate existing exercises
    exercises = Exercise.query.all() #add filter for specific workout type
    form.existing_exercise.choices = [(e.id, e.name) for e in exercises]

    if form.validate_on_submit():
        # Process the form data
        pass

    return render_template('edit_worklog.html', form=form)

@app.route('/worklogs/new', methods=['GET', 'POST'])
def new_worklog():
    form = NewWorkLog()
    
    # add logic for recommended exercises based on exercise type
    if form.validate_on_submit():
        title = form.title.data
        
        # workout_type= dict(form.workout_type.choices).get(form.workout_type.data)
        # type_id = form.workout_type.data

        workout_type_id = form.workout_type.data
        user_id = current_user.id 


        new_wl = Worklog(title = title, workout_type_id = workout_type_id, user_id = user_id)
        db.session.add(new_wl)
        db.session.commit()
        return redirect(url_for('make_worklog', wk_id = new_wl.id))

    return render_template('worklog/newlog.html', form=form)

@app.route('/worklog/<int:wk_id>')
def make_worklog(wk_id):
    worklog = Worklog.query.get_or_404(wk_id)

    return render_template('worklog/worklog.html', worklog = worklog)

@app.route('/worklog/<int:wk_id>/exercise', methods = ['POST'])
def add_excercise(wk_id):
    print("request recieved")
    return

@app.route('/worklog/<int:wk_id>/exercise', methods = ['PATCH'])
def edit_excercise(wk_id):
    return

@app.route('/worklog/<int:wk_id>/exercise', methods = ['DELETE'])
def delete_excercise(wk_id):
    return

@app.route('/worklog/<int:wk_id>/exercise/set', methods = ['POST'])
def add_set(wk_id):
    return

@app.route('/worklog/<int:wk_id>/exercise/set', methods = ['PATCH'])
def edit_set(wk_id):
    return

@app.route('/worklog/<int:wk_id>/exercise/set', methods = ['DELETE'])
def delete_set(wk_id):
    return

#####################################################
# Login/Register for users

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        login_user(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


    
@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            login_user(user)
            flash('Logged in successfully.', category='success')
            # next = request.args.get('next')
            return redirect("/")

        else:
            form.username.errors = ["Invalid input"]
            return render_template("users/login.html", form=form)

    else:
        return render_template("users/login.html", form=form)
    
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#End login/ Register Routes
#####################################################

    

