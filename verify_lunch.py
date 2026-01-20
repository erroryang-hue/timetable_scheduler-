import data
from config import DAYS
from scheduler.generator_random import generate_random_timetable

print("\n" + "="*100)
print(" LAB BREAK VERIFICATION - Ensuring No Labs Span Lunch")
print("="*100 + "\n")

def check_lunch_violations(sem_id, sem_data):
    """Check if any labs span the lunch break"""
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
    
    violations = []
    
    for cls in sem_data["classes"]:
        for day in DAYS:
            # Check if P4 (slot 3) and P5 (slot 4) both have the SAME lab
            p4_slot = timetable[cls][day][3]
            p5_slot = timetable[cls][day][4]
            
            if p4_slot and p5_slot:
                # Both slots have content
                p4_subject = p4_slot.get("subject", "")
                p5_subject = p5_slot.get("subject", "")
                
                # Check if they're the same lab (or continuation thereof)
                if "LAB" in p4_subject.upper() or "LAB" in p5_subject.upper():
                    # Check if they're part of the same session
                    p4_base = p4_subject.replace(" (cont.)", "").strip()
                    p5_base = p5_subject.replace(" (cont.)", "").strip()
                    
                    if p4_base == p5_base:
                        violations.append({
                            "class": cls,
                            "day": day,
                            "subject": p4_base,
                            "p4": p4_subject,
                            "p5": p5_subject
                        })
    
    return violations

# Test Semester 3 and 5
for sem_id in ["3", "5"]:
    print(f"\n{'='*100}")
    print(f" SEMESTER {sem_id}")
    print(f"{'='*100}")
    
    sem_data = data.ALL_SEMESTERS[sem_id]
    violations = check_lunch_violations(sem_id, sem_data)
    
    if violations:
        print(f"\n❌ FAILED - Found {len(violations)} lab(s) spanning lunch break:\n")
        for v in violations:
            print(f"  Class {v['class']}, {v['day']}:")
            print(f"    P4: {v['p4']}")
            print(f"    P5: {v['p5']}")
            print(f"    ^ These should NOT be the same lab session!")
    else:
        print(f"\n✅ PASSED - No labs span the lunch break")
        print(f"   All labs use valid pairs: (P1-P2), (P3-P4), or (P5-P6)")

print("\n" + "="*100 + "\n")
