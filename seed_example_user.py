from datetime import datetime, timedelta
import random
from app import db, app  # Adjust based on your actual app structure
from models import User, WorkoutType, Worklog, WorkoutExercise, ExerciseSet, Post, bcrypt

def create_experienced_user():
    # Ensure the user doesn't already exist
    if User.query.filter_by(username="fitenthusiast").first() is None:
        hashed_pwd = bcrypt.generate_password_hash("supersecurepassword").decode('utf-8')
        
        user = User(
            username="fitenthusiast",
            email="fitenthusiast@example.com",
            password=hashed_pwd,
            name="Alex",
            image_url="/static/images/defaultPic.png"
        )
        db.session.add(user)
        db.session.commit()
        print("Created experienced user: fitenthusiast.")
    else:
        user = User.query.filter_by(username="fitenthusiast").first()
        print("Experienced user already exists.")

    return user

def add_workouts_and_posts(user):
    workout_types = WorkoutType.query.all()
    
    # Generate 10 worklogs for the user with various workout types
    for i in range(10):
        workout_date = datetime.utcnow() - timedelta(days=i*10)  # Stagger the workout dates
        workout_type = random.choice(workout_types)
        
        worklog = Worklog(
            title=f"{workout_type.type_name} Session",
            user_id=user.id,
            created_at= workout_date
        )
        
        # Adding a generic exercise for the workout type
        exercise = WorkoutExercise(
            name=f"{workout_type.type_name} Exercise",
            worklog=worklog
        )
        
        # Adding a generic set for the exercise
        exercise_set = ExerciseSet(
            workout_exercise=exercise,
            set_number=1,
            reps=10,
            weight=50  # Assuming weight for demonstration; adjust as needed
        )
        
        # Creating a reflective post for each workout
        post = Post(
            title=f"Great {workout_type.type_name} Workout!",
            message=f"Really pushed my limits in today's {workout_type.type_name.lower()} session.",
            user_id=user.id,
            worklog=worklog,
            created_at=workout_date
        )
        
        db.session.add(worklog)
        db.session.add(exercise)
        db.session.add(exercise_set)
        db.session.add(post)
    
    db.session.commit()
    print("Added workouts and posts for experienced user.")

if __name__ == "__main__":
    with app.app_context():
        user = create_experienced_user()
        add_workouts_and_posts(user)
        print("Database seeded with an experienced user, their workouts, and posts.")
