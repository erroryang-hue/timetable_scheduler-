import data
from config import DAYS
from scheduler.generator_random import generate_random_timetable

print("\n" + "="*100)
print(" MULTI-SEMESTER TEACHER COLLISION VERIFICATION")
print("="*100 + "\n")

# Track all teacher usage across semesters
global_teacher_usage = {}

# Generate all semesters
timetables = {}
for sem_id in ["1", "3", "5", "7"]:
    sem_data = data.ALL_SEMESTERS[sem_id]
    print(f"\nGenerating Semester {sem_id}...")
    
    timetables[sem_id] = generate_random_timetable(
        sem_data["classes"],
        sem_data["subjects"],
        sem_data["teachers"],
        DAYS,
        sem_data["classrooms"],
        sem_data["commonClasses"],
        global_teacher_usage=global_teacher_usage,
        semester_constraints=sem_data.get("constraints", {})
    )
    
    print(f"  ✅ Generated successfully")

# Now check for collisions
print(f"\n{'='*100}")
print(" COLLISION CHECK")
print(f"{'='*100}\n")

# Get all unique teachers across all semesters
all_teachers = set()
for sem_id, sem_data in data.ALL_SEMESTERS.items():
    for subject, teacher_list in sem_data["teachers"].items():
        all_teachers.update(teacher_list)

# Check each teacher's schedule
collisions_found = []
for teacher in sorted(all_teachers):
    teacher_schedule = {}
    
    # Build this teacher's complete schedule across all semesters
    for sem_id, timetable in timetables.items():
        for class_name, schedule in timetable.items():
            for day in DAYS:
                for period_idx, slot in enumerate(schedule[day]):
                    if slot and slot.get("teacher") == teacher:
                        key = (day, period_idx)
                        if key not in teacher_schedule:
                            teacher_schedule[key] = []
                        teacher_schedule[key].append({
                            "sem": sem_id,
                            "class": class_name,
                            "subject": slot.get("subject")
                        })
    
    # Check for double-booking
    for (day, period), bookings in teacher_schedule.items():
        if len(bookings) > 1:
            collisions_found.append({
                "teacher": teacher,
                "day": day,
                "period": period + 1,
                "bookings": bookings
            })

if collisions_found:
    print(f"❌ FAILED - Found {len(collisions_found)} collision(s):\n")
    for c in collisions_found:
        print(f"  Teacher: {c['teacher']}")
        print(f"  Time: {c['day']} P{c['period']}")
        for b in c['bookings']:
            print(f"    - Sem {b['sem']}, Class {b['class']}: {b['subject']}")
        print()
else:
    print(f"✅ PASSED - NO TEACHER COLLISIONS DETECTED")
    print(f"   All {len(all_teachers)} teachers have conflict-free schedules across all semesters!")

print("\n" + "="*100 + "\n")
