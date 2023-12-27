from models import WorkoutType, db  # Import WorkoutType model
from app import app

def seed_workout_types():
    # Define an expanded list of workout types
    workout_types = [
        {"type_name": "Chest", "description": "Exercises focusing on pectoral muscles"},
        {"type_name": "Back", "description": "Workouts targeting the back muscles"},
        {"type_name": "Arms", "description": "Biceps and triceps focused exercises"},
        {"type_name": "Shoulders", "description": "Exercises for deltoids and overall shoulder strength"},
        {"type_name": "Legs", "description": "Workouts targeting leg muscles including quads, hamstrings, and calves"},
        {"type_name": "Core", "description": "Core strengthening and abdominal workouts"},
        {"type_name": "Chest/Back", "description": "Combined workouts for chest and back muscles"},
        {"type_name": "Legs/Back", "description": "Compound exercises targeting both leg and back muscles"},
        {"type_name": "Full Body", "description": "Workouts targeting all major muscle groups"},
        {"type_name": "Glutes", "description": "Exercises focusing on glute muscles"},
        {"type_name": "Forearms", "description": "Strengthening workouts for forearm muscles"},
        {"type_name": "Calisthenics", "description": "Bodyweight exercises that focus on strength and flexibility"},
        {"type_name": "Functional Training", "description": "Workouts that enhance functional strength and coordination"},
        {"type_name": "High-Intensity Interval Training (HIIT)", "description": "High-intensity workouts with periods of rest or lower intensity"},
        {"type_name": "Powerlifting", "description": "Strength training focusing on maximal power output"},
        {"type_name": "Olympic Weightlifting", "description": "Workouts focusing on Olympic-style lifting techniques"}
        # Add more workout types as needed
    ]

    # Clear existing data
    db.session.query(WorkoutType).delete()

    # Add new workout types
    for wt in workout_types:
        workout_type = WorkoutType(type_name=wt["type_name"], description=wt["description"])
        db.session.add(workout_type)

    # Commit the changes
    db.session.commit()

if __name__ == "__main__":
    seed_workout_types()
