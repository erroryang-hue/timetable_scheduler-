from scheduler.generator_random import generate_timetable
from config import DAYS, PERIODS

classes = ["3A", "3B"]

subjects = {
    "MATH": 4,
    "DSA": 4,
    "OS": 3
}

teachers = {
    "MATH": "T1",
    "DSA": "T2",
    "OS": "T3"
}

timetable = generate_timetable(classes, subjects, teachers, DAYS, PERIODS)

for cls in timetable:
    print("\nClass:", cls)
    for day in DAYS:
        print(day, timetable[cls][day])
