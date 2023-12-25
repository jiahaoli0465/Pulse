import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from forms import RegisterForm, LoginForm
from models import db, connect_db, User

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




@app.route('/')
def show_home():
    users = User.query.all()
    return render_template('home.html', users = users)

@app.route('/form')
def form_page():
    return render_template('form_page.html')

@app.route('/dashboard')
def show_dashboard():

    return render_template('users/dashboard.html')







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

    

