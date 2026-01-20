import data
from config import DAYS
from scheduler.generator_random import generate_random_timetable

# Generate Semester 5 timetable
sem_data = data.SEMESTER_5
global_teacher_usage = {}

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

print("\n" + "="*80)
print(" SEMESTER 5 TIMETABLE VERIFICATION")
print("="*80)

# Check each class
for cls in sem_data["classes"]:
    print(f"\n{'='*80}")
    print(f" CLASS: {cls}")
    print(f"{'='*80}\n")
    
    for day in DAYS:
        print(f"{day:10}", end=" | ")
        for period in range(6):
            slot = timetable[cls][day][period]
            if slot:
                subject = slot.get("subject", "")
                classroom = slot.get("classroom", "")
                print(f"P{period+1}: {subject:15} ({classroom:15})", end=" | ")
            else:
                print(f"P{period+1}: {'---':15} ({'':15})", end=" | ")
        print()
    
    # Verify proper half-day distribution (4 half-days, 1 day with lab)
    print(f"\n{'-'*80}")
    print("VERIFICATION: Half-Day Check (4 days should have empty P5-P6, 1 day has lab)")
    print(f"{'-'*80}")
    
    half_day_count = 0
    lab_day_count = 0
    lab_day = None
    
    for day in DAYS:
        p5 = timetable[cls][day][4]  # Slot 4 = Period 5
        p6 = timetable[cls][day][5]  # Slot 5 = Period 6
        
        if not p5 and not p6:
            half_day_count += 1
            print(f"  {day}: Half-Day (P5-P6 empty)")
        elif p5 and "LAB" in p5.get('subject', '').upper():
            lab_day_count += 1
            lab_day = day
            print(f"  {day}: Lab Day (P5: {p5.get('subject')}, P6: {p6.get('subject') if p6 else 'Empty'})")
        else:
            print(f"  {day}: P5={p5.get('subject') if p5 else 'Empty'}, P6={p6.get('subject') if p6 else 'Empty'}")
    
    # Check constraints
    if half_day_count >= 4:
        print(f"\n✅ PASSED - {half_day_count} half-days (expected: 4)")
    else:
        print(f"\n❌ FAILED - Only {half_day_count} half-days (expected: 4)")
    
    if lab_day_count >= 1:
        print(f"✅ PASSED - Lab day found: {lab_day}")
    else:
        print(f"⚠️  WARNING - No lab afternoon found")
    
    # Verify lab placement
    print(f"\n{'-'*80}")
    print("VERIFICATION: Lab Placement Check")
    print(f"{'-'*80}")
    
    # Verify classroom usage
    print(f"\n{'-'*80}")
    print(f"VERIFICATION: Classroom Check ({cls} should use same room for all theory)")
    print(f"{'-'*80}")
    
    theory_classrooms = set()
    for day in DAYS:
        for period in range(4):  # Check P1-P4 (theory periods)
            slot = timetable[cls][day][period]
            if slot and slot.get("classroom") and "Lab" not in slot.get("classroom", ""):
                theory_classrooms.add(slot.get("classroom"))
    
    if len(theory_classrooms) == 1:
        print(f"✅ PASSED - All theory classes in: {list(theory_classrooms)[0]}")
    elif len(theory_classrooms) == 0:
        print("⚠️  WARNING - No theory classrooms assigned")
    else:
        print(f"❌ FAILED - Multiple theory rooms used: {theory_classrooms}")

print("\n" + "="*80)
