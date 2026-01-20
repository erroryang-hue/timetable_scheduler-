import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scheduler.generator_random import generate_random_timetable

def verify_dynamic_inputs():
    print("Verifying Dynamic Inputs from simulated Web Request...")

    # Simulated Data from Frontend (Sem 3)
    # We will define a Home Room for 3A (R-HOME) and a Subject Room for 'DSA' (R-DSA)
    
    classes = ["3A", "3B"]
    subjects = {
        "MATH3": {"count": 4, "type": "THEORY"},
        "DSA": {"count": 4, "type": "THEORY"}, # Should go to R-DSA
        "OS": {"count": 4, "type": "THEORY"}   # Should go to R-HOME (for 3A) or random (for 3B)
    }
    teachers = {
        "MATH3": ["T1"],
        "DSA": ["T2"],
        "OS": ["T3"]
    }
    days = ["Mon", "Tue"]
    
    # Dynamic Classrooms Input
    classrooms = [
        {"name": "R-HOME", "type": "THEORY", "class": "3A"},     # Home room for 3A
        {"name": "R-DSA", "type": "THEORY", "subject": "DSA"},   # Specific room for DSA
        {"name": "R-GEN", "type": "THEORY"}                      # General room
    ]
    
    tt = generate_random_timetable(
        classes, subjects, teachers, days, classrooms, [], {}
    )
    
    errors = []
    
    # Check 3A
    print("\nChecking 3A:")
    for d in days:
        for slot in tt["3A"][d]:
            if slot and slot.get("subject"):
                sub = slot["subject"]
                room = slot["classroom"]
                
                if sub == "DSA":
                    if room != "R-DSA":
                        errors.append(f"3A DSA in {room} (expected R-DSA)")
                else:
                    # Other theory subjects should be in Home Room
                    if room != "R-HOME":
                         errors.append(f"3A {sub} in {room} (expected R-HOME)")

    # Check 3B (No Home Room designated, should use General or Specific)
    print("\nChecking 3B:")
    for d in days:
        for slot in tt["3B"][d]:
             if slot and slot.get("subject"):
                sub = slot["subject"]
                room = slot["classroom"]
                
                if sub == "DSA":
                    if room != "R-DSA":
                         errors.append(f"3B DSA in {room} (expected R-DSA)")
                else:
                    # Should be in General room roughly (or random) but NOT R-HOME (dedicated to 3A)
                    if room == "R-HOME":
                        errors.append(f"3B {sub} in {room} (R-HOME should be exclusive to 3A)")


    if errors:
        print("FAIL: Found errors:")
        for e in errors:
            print(e)
    else:
        print("PASS: Dynamic Home Room and Subject Room inputs working correctly.")

if __name__ == "__main__":
    verify_dynamic_inputs()
