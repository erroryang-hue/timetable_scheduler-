import data
from config import DAYS
from scheduler.generator_random import generate_random_timetable

def verify_semester(sem_id, sem_data):
    """Generate and verify a semester's timetable"""
    print(f"\n{'='*100}")
    print(f" SEMESTER {sem_id} - TIMETABLE VERIFICATION")
    print(f"{'='*100}\n")
    
    global_teacher_usage = {}
    
    try:
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
        
        print("✅ Generation SUCCESSFUL\n")
        
        # Verify classroom assignments
        for cls in sem_data["classes"]:
            theory_rooms = set()
            lab_rooms = set()
            
            for day in DAYS:
                for period in range(6):
                    slot = timetable[cls][day][period]
                    if slot and slot.get("classroom"):
                        room = slot.get("classroom")
                        if "Lab" in room or "LAB" in room:
                            lab_rooms.add(room)
                        else:
                            theory_rooms.add(room)
            
            print(f"Class {cls}:")
            print(f"  Theory Classrooms: {', '.join(theory_rooms) if theory_rooms else 'None'}")
            if len(theory_rooms) == 1:
                print(f"  ✅ All theory classes in ONE room")
            elif len(theory_rooms) > 1:
                print(f"  ⚠️  Multiple theory rooms used: {theory_rooms}")
            
            print(f"  Lab Rooms: {', '.join(lab_rooms) if lab_rooms else 'None'}")
            print()
        
        # Semester 5 specific checks
        if sem_id == "5":
            print(f"{'='*100}")
            print(f" SEMESTER 5 HALF-DAY VERIFICATION")
            print(f"{'='*100}\n")
            
            for cls in sem_data["classes"]:
                print(f"Class {cls}:")
                
                # Check proper half-day distribution
                half_day_count = 0
                lab_day_count = 0
                lab_day = None
                
                for day in DAYS:
                    p5 = timetable[cls][day][4]
                    p6 = timetable[cls][day][5]
                    
                    if not p5 and not p6:
                        half_day_count += 1
                    elif p5 and "LAB" in p5.get('subject', '').upper():
                        lab_day_count += 1
                        lab_day = day
                
                if half_day_count >= 4:
                    print(f"  ✅ PASSED - {half_day_count} half-days (P5-P6 empty)")
                else:
                    print(f"  ❌ FAILED - Only {half_day_count} half-days (expected 4)")

                if lab_day_count >= 1:
                    print(f"  ✅ PASSED - Lab day found: {lab_day}")
                    
                    # Check the specific lab slots on that day
                    l_day_p5 = timetable[cls][lab_day][4]
                    l_day_p6 = timetable[cls][lab_day][5]
                    print(f"     P5: {l_day_p5.get('subject')} | P6: {l_day_p6.get('subject')}")
                else:
                    print(f"  ⚠️  WARNING - No lab afternoon found")
                
                print()
        
        return True
        
    except Exception as e:
        print(f"❌ Generation FAILED: {e}")
        return False

# Test all semesters
print("\n" + "="*100)
print(" MULTI-SEMESTER TIMETABLE VERIFICATION")
print("="*100)

results = {}
for sem_id in ["1", "3", "5", "7"]:
    sem_data = data.ALL_SEMESTERS[sem_id]
    results[sem_id] = verify_semester(sem_id, sem_data)

print("\n" + "="*100)
print(" SUMMARY")
print("="*100)
for sem_id, success in results.items():
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"  Semester {sem_id}: {status}")
print("="*100 + "\n")
