from app import db
from models import WorkoutType

def add_workout_type(name, description):
    workout_type = WorkoutType(type_name=name, description=description)
    db.session.add(workout_type)

def seed_workout_types():
    db.session.commit()  # Ensure any pending transactions are completed
    db.session.query(WorkoutType).delete()  # Clear existing data

    # Expanded list of muscle groups with descriptions
    muscle_groups = [
        ("Chest", "Exercises targeting the chest muscles"),
        ("Back", "Exercises targeting the back muscles"),
        ("Shoulders", "Exercises targeting the shoulder muscles"),
        ("Arms", "Exercises targeting the arm muscles"),
        ("Legs", "Exercises targeting the leg muscles"),
        ("Core/Abs", "Exercises targeting the abdominal muscles"),
        ("Biceps", "Exercises targeting the biceps"),
        ("Triceps", "Exercises targeting the triceps"),
        ("Quadriceps", "Exercises targeting the quadriceps"),
        ("Hamstrings", "Exercises targeting the hamstrings"),
        ("Calves", "Exercises targeting the calf muscles"),
        ("Glutes", "Exercises targeting the gluteal muscles"),
        ("Forearms", "Exercises targeting the forearm muscles"),
        ("Upper Back", "Exercises targeting the upper back muscles"),
        ("Lower Back", "Exercises targeting the lower back muscles"),
        ("Lats", "Exercises targeting the latissimus dorsi muscles"),
        ("Deltoids", "Exercises targeting the deltoid muscles"),
        ("Abdominals", "Exercises targeting the abdominal muscles"),
        ("Obliques", "Exercises targeting the oblique muscles"),
        ("Hip Flexors", "Exercises targeting the hip flexor muscles"),
        ("Adductors", "Exercises targeting the inner thigh muscles"),
        ("Abductors", "Exercises targeting the outer thigh muscles"),
    ]

    # Add each muscle group to the session
    for name, description in muscle_groups:
        add_workout_type(name, description)

    db.session.commit()  # Commit the changes

if __name__ == "__main__":
    seed_workout_types()
    print("Database seeded with workout types.")
