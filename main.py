from scheduler.generator_random import generate_random_timetable
from config import DAYS
import data

# Initialize global teacher usage to track busy slots across ALL semesters
global_teacher_usage = {}

# Order: 1, 3, 5, 7 (or any priority, but sequential is fine)
semesters_to_schedule = ["1", "3", "5", "7"]

for sem_id in semesters_to_schedule:
    print(f"\n{'='*50}")
    print(f"Generating Timetable for Semester {sem_id}")
    print(f"{'='*50}")
    
    sem_data = data.ALL_SEMESTERS[sem_id]
    
    # Generate timetable for this semester
    # The global_teacher_usage dictionary is updated in-place by the function
    timetable = generate_random_timetable(
        sem_data["classes"],
        sem_data["subjects"],
        sem_data["teachers"],
        DAYS,
        sem_data["classrooms"],
        sem_data["commonClasses"],
        global_teacher_usage=global_teacher_usage,
        semester_constraints=sem_data.get("constraints", {})
    )
    
    # Display results
    for cls in timetable:
        print(f"\nClass: {cls}")
        # Print header
        print(f"{'DAY':<5} | {'P1':<20} | {'P2':<20} | {'P3':<20} | {'P4':<20} | {'P5':<20} | {'P6':<20}")
        print("-" * 140)
        
        for day in DAYS:
            row_str = f"{day:<5} | "
            for i in range(6):
                slot = timetable[cls][day][i]
                if slot:
                    content = f"{slot['subject']} ({slot['teacher']})"
                    if slot.get('classroom'):
                        content += f" [{slot['classroom']}]"
                else:
                    content = "FREE"
                row_str += f"{content:<20} | "
            print(row_str)

# Debug: Show teacher usage stats
print(f"\n{'='*50}")
print("Global Teacher Usage Stats")
print(f"{'='*50}")
for teacher, days in global_teacher_usage.items():
    total_slots = sum(len(slots) for slots in days.values())
    print(f"{teacher}: {total_slots} slots booked")

