import os
import openai

from flask import Flask, render_template, request, flash, redirect, session, g, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from forms import RegisterForm, LoginForm, EditWorkLog, NewExercise, NewWorkLog,NewWorkType, EditProfileForm
from models import db, connect_db, User, Worklog, WorkoutType, Exercise, ExerciseSet, WorkoutExercise, Post

from assistant.assistant import assistantbot, client

app = Flask(__name__)
app.register_blueprint(assistantbot)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///pulse'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)
migrate = Migrate(app, db)

connect_db(app)


with app.app_context():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

print('app.py')

@app.route('/')
@login_required
def show_home():
    # Get list of user_ids for the current user and the users they follow
    user_ids = [current_user.id] + [user.id for user in current_user.following]
    print(user_ids)
    # Query posts from those users
    posts = Post.query.filter(Post.user_id.in_(user_ids)).order_by(Post.created_at.desc()).all()

    
    return render_template('home.html', posts=posts)


@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def show_dashboard():
    worklogs = Worklog.query.filter_by(user_id=current_user.id).all()
    return render_template('users/dashboard.html', worklogs = worklogs)

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def show_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.image_url = form.image_url.data
        current_user.username = form.username.data
        db.session.commit()
        return redirect('/dashboard')


    return render_template('users/profile.html', user = current_user , form = form)
    
@app.route('/users', methods = ['GET', 'POST'])
def show_users():
    users = User.query.all()
    return render_template('users/users.html', users = users)

@app.route('/api/users/<int:user_id>/follow', methods=['POST'])
@login_required
def follow_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'status': 'error', 'message': 'User not found.'}), 404
    if current_user.is_following(user):
        return jsonify({'status': 'error', 'message': 'Already following this user.'}), 400
    current_user.follow(user)
    db.session.commit()
    print('followed')
    return jsonify({'status': 'success', 'message': 'You are now following this user.'})




@app.route('/api/users/<int:user_id>/unfollow', methods=['POST'])
@login_required
def unfollow_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'status': 'error', 'message': 'User not found.'}), 404
    if not current_user.is_following(user):
        return jsonify({'status': 'error', 'message': 'Not following this user.'}), 400
    current_user.unfollow(user)
    db.session.commit()
    print('unfollowed')
    return jsonify({'status': 'success', 'message': 'You have unfollowed this user.'})




#============ Post Routes ============
@app.route('/api/posts/new', methods=['POST'])
@login_required
def create_post():
    # Extracting data from the request's JSON body
    data = request.json
    message = data.get('message')
    worklog_id = data.get('worklog_id')
    
    # Basic validation
    if not message or not worklog_id:
        return jsonify({'status': 'error', 'message': 'Message and Worklog ID are required.'}), 400

    # Ensure the worklog exists
    worklog = Worklog.query.get(worklog_id)
    if not worklog:
        return jsonify({'status': 'error', 'message': 'Worklog not found.'}), 404

    # Create new post
    new_post = Post(message=message, user_id=current_user.id, worklog_id=worklog_id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Post created successfully.', 'post_id': new_post.id}), 201

#============ End Post Routes ============


#============== WORKLOG AI ===================
@app.route('/api/user/<int:user_id>/worklogs', methods=['GET'])
def get_userLogs(user_id):
    worklogs = Worklog.query.filter_by(user_id=user_id).all()
    
    worklogs_data = []
    for log in worklogs:
        # Fetching workout types for each worklog
        workout_types_data = [{
            "id": wt.id,
            "type_name": wt.type_name,
            "description": wt.description
        } for wt in log.workout_types]

        # Fetching workout exercises for each worklog
        workout_exercises_data = []
        for exercise in log.workout_exercises:
            exercise_sets_data = [{
                "set_number": set.set_number,
                "weight": set.weight,
                "reps": set.reps
            } for set in exercise.exercise_sets]
            
            workout_exercises_data.append({
                "id": exercise.id,
                "name": exercise.name,
                "exercise_sets": exercise_sets_data
            })
        
        worklogs_data.append({
            "id": log.id,
            "title": log.title,
            "workout_types": workout_types_data,  # Include workout types here
            "created_at": log.created_at.isoformat(),
            "workout_exercises": workout_exercises_data
        })
    
    response = {
        "user_id": user_id,
        "worklogs": worklogs_data
    }

    return jsonify(response)



@app.route('/api/worklog/<int:worklog_id>', methods=['GET'])
def get_worklog(worklog_id):
    # Fetch the specific worklog
    worklog = Worklog.query.get(worklog_id)

    # Check if worklog exists
    if not worklog:
        return jsonify({"error": "Worklog not found"}), 404

    # Serialize data
    worklog_data = {
        "id": worklog.id,
        "title": worklog.title,
        "created_at": worklog.created_at.isoformat(),
        "friendly_date": worklog.friendly_date,
        "workout_type": [wk.type_name for wk in worklog.workout_types],
        "exercises": [{
            "name": exercise.name,
            "sets": [{
                "set_number": eset.set_number,
                "weight": eset.weight,
                "reps": eset.reps
            } for eset in exercise.exercise_sets]
        } for exercise in worklog.workout_exercises]
    }

    # Return the JSON response
    return jsonify(worklog_data)

#============== WORKLOG ===================

@app.route('/worklogs/new', methods=['GET', 'POST'])
def new_worklog():
    form = NewWorkLog()

    if form.validate_on_submit():
        title = form.title.data
        workout_type_ids = form.workout_type.data  # This will be a list of IDs
        user_id = current_user.id 

        # Create a new Worklog instance
        new_wl = Worklog(title=title, user_id=user_id)
        db.session.add(new_wl)
        db.session.flush()  # Flush the session to get the id for the new worklog

        # Associate selected workout types with the new worklog
        for wt_id in workout_type_ids:
            print(f'attempting to add: {wt_id}')
            # Assuming you have a relationship setup in the Worklog model for workout_types
            workout_type = WorkoutType.query.get(wt_id)
            if workout_type:
                new_wl.workout_types.append(workout_type)

        db.session.commit()
        return redirect(url_for('make_worklog', wk_id=new_wl.id))

    return render_template('worklog/newlog.html', form=form)


@app.route('/worklog/<int:wk_id>')
def make_worklog(wk_id):
    if 'thread_id' not in session:
        thread = client.beta.threads.create()
        session['thread_id'] = thread.id
        
    worklog = Worklog.query.get_or_404(wk_id)

    return render_template('worklog/worklog.html', worklog = worklog)


#CRUD FOR EXERCISE
###################################################
@app.route('/worklog/<int:wk_id>/exercise', methods=['POST'])
def add_exercise(wk_id):
    print("Exercise request received")
    
    # Check if worklog exists
    worklog = Worklog.query.get(wk_id)
    if not worklog:
        return jsonify(message="Worklog not found"), 404

    # Ensure JSON payload is present
    data = request.json
    if not data:
        return jsonify(message="No data provided"), 400

    # Extract and validate name
    name = data.get('name')
    if not name:
        return jsonify(message="Exercise name is required"), 400

    # Create and save the new exercise
    new_exercise = WorkoutExercise(worklog_id=wk_id, name=name)
    db.session.add(new_exercise)
    db.session.commit()

    return jsonify(message="Exercise created", exercise_id = new_exercise.id), 201


@app.route('/worklog/<int:wk_id>/exercise/<int:ex_id>', methods=['PATCH'])
def edit_exercise(wk_id, ex_id):
    print("Exercise edit request received")
    
    # Check if worklog and exercise exists
    worklog = Worklog.query.get(wk_id)
    workout_exercise = WorkoutExercise.query.filter_by(id=ex_id, worklog_id=wk_id).first()

    if not worklog:
        return jsonify(message="Worklog not found"), 404
    
    if not workout_exercise:
        return jsonify(message="Exercise not found"), 404

    data = request.json
    if not data:
        return jsonify(message="No data provided"), 400

    # Update the exercise if a new name is provided
    name = data.get('name')
    if name:
        workout_exercise.name = name

    db.session.commit()
    return jsonify(message="Exercise updated"), 200


@app.route('/worklog/<int:wk_id>/exercise/<int:ex_id>', methods=['DELETE'])
def delete_exercise(wk_id, ex_id):
    # Check if worklog and exercise exist
    worklog = Worklog.query.get(wk_id)
    workout_exercise = WorkoutExercise.query.filter_by(id=ex_id, worklog_id=wk_id).first()

    if not worklog:
        return jsonify(message="Worklog not found"), 404

    if not workout_exercise:
        return jsonify(message="Exercise not found"), 404

    # Delete the exercise
    db.session.delete(workout_exercise)
    db.session.commit()

    return jsonify(message="Exercise deleted"), 200

#END SECTION
####################################################################


#CRUD FOR SET
####################################################################
@app.route('/worklog/<int:wk_id>/exercise/<int:ex_id>/set', methods=['POST'])
def add_set(wk_id, ex_id):
    print("Set request received")
    worklog = Worklog.query.get(wk_id)
    workout_exercise = WorkoutExercise.query.filter_by(id=ex_id, worklog_id=wk_id).first()
    print(request.json)

    if not worklog:
        return jsonify(message="Worklog not found"), 404
    
    if not workout_exercise:
        return jsonify(message="Exercise not found"), 404

    data = request.json
    print("makes it to data")
    if not data:
        return jsonify(message="No data provided"), 400

    set_number = data.get('setNum')
    weight = data.get('setWeight')
    reps = data.get('setReps')


    if set_number is None:
        return jsonify(message="Set number is required"), 400
    if weight is None:
        return jsonify(message="Weight data is required"), 400
    if reps is None:
        return jsonify(message="Reps data is required"), 400

    # Check if the set number already exists for this exercise
    existing_set = ExerciseSet.query.filter_by(workout_exercise_id=ex_id, set_number=set_number).first()
    if existing_set:
        return jsonify(message="Set number already exists for this exercise"), 400

    new_set = ExerciseSet(workout_exercise_id=ex_id, set_number=set_number, weight=weight, reps=reps)

    db.session.add(new_set)
    db.session.commit()
    return jsonify(message="New set created", set_id = new_set.id), 201


@app.route('/worklog/<int:wk_id>/exercise/<int:ex_id>/set/<int:set_id>', methods=['PATCH'])
def edit_set(wk_id, ex_id, set_id):
    print("Set edit request received")

    # Check if worklog and exercise exist
    worklog = Worklog.query.get(wk_id)
    if not worklog:
        return jsonify(message="Worklog not found"), 404

    workout_exercise = WorkoutExercise.query.filter_by(id=ex_id, worklog_id=wk_id).first()
    if not workout_exercise:
        return jsonify(message="Exercise not found in this worklog"), 404

    # Check if the set exists and belongs to the specified exercise
    exercise_set = ExerciseSet.query.filter_by(id=set_id, workout_exercise_id=ex_id).first()
    if not exercise_set:
        return jsonify(message="Set not found in this exercise"), 404

    data = request.json
    if not data:
        return jsonify(message="No data provided"), 400

    # Update the set fields if provided
    
    sets = data.get('setNum')
    weight = data.get('setWeight')
    reps = data.get('setReps')
    print(f'set: {sets} weight: {weight}, reps: {reps}')
    if sets is not None:
        exercise_set.set_number = sets
    if weight is not None:
        exercise_set.weight = weight
    if reps is not None:
        exercise_set.reps = reps

    db.session.commit()
    return jsonify(message="Set updated"), 200


@app.route('/worklog/<int:wk_id>/exercise/<int:ex_id>/set/<int:set_id>', methods=['DELETE'])
def delete_set(wk_id, ex_id, set_id):
    print("Set delete request received")

    # Check if worklog and exercise exist
    worklog = Worklog.query.get(wk_id)
    if not worklog:
        return jsonify(message="Worklog not found"), 404

    workout_exercise = WorkoutExercise.query.filter_by(id=ex_id, worklog_id=wk_id).first()
    if not workout_exercise:
        return jsonify(message="Exercise not found in this worklog"), 404

    # Check if the set exists and belongs to the specified exercise
    exercise_set = ExerciseSet.query.filter_by(id=set_id, workout_exercise_id=ex_id).first()
    if not exercise_set:
        return jsonify(message="Set not found in this exercise"), 404

    # Delete the set
    db.session.delete(exercise_set)
    db.session.commit()

    return jsonify(message="Set deleted"), 200
#END SECTION
####################################################################



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

    

def list_files(directory):
    paths = []
    for dirname, _, files in os.walk(directory):
        for filename in files:
            paths.append(os.path.join(dirname, filename))
    return paths

if __name__ == "__main__":
    extra_dirs = ['templates', 'static']
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        extra_files.extend(list_files(extra_dir))
    app.run(debug=True, extra_files=extra_files)