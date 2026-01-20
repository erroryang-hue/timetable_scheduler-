import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data import ALL_SEMESTERS
from scheduler.generator_random import generate_random_timetable

def verify_home_rooms():
    print("Verifying Home Room and Specific Room assignments...")
    
    # We will generate a timetable for Sem 1 and Check
    sem1 = ALL_SEMESTERS["1"]
    tt_sem1 = generate_random_timetable(
        sem1["classes"], sem1["subjects"], sem1["teachers"], 
        ["Mon", "Tue", "Wed", "Thu", "Fri"], 
        sem1["classrooms"], sem1["commonClasses"], {}
    )
    
    errors = []
    
    # Check 1A
    cls = "1A"
    for day, slots in tt_sem1[cls].items():
        for slot in slots:
            if slot and not slot.get("isCommon"):
                sub = slot["subject"]
                room = slot["classroom"]
                ctype = "LAB" if "LAB" in sub else "THEORY"
                
                if sub == "EG":
                    if room != "Drawing Hall":
                        errors.append(f"1A EG in {room} (expected Drawing Hall)")
                elif ctype == "THEORY":
                    if room != "R101":
                        errors.append(f"1A {sub} in {room} (expected R101)")

    # Check 1B
    cls = "1B"
    for day, slots in tt_sem1[cls].items():
        for slot in slots:
            if slot and not slot.get("isCommon"):
                sub = slot["subject"]
                room = slot["classroom"]
                ctype = "LAB" if "LAB" in sub else "THEORY"

                if sub == "EG":
                    if room != "Drawing Hall":
                         errors.append(f"1B EG in {room} (expected Drawing Hall)")
                elif ctype == "THEORY":
                    if room != "R102":
                        errors.append(f"1B {sub} in {room} (expected R102)")

    if errors:
        print("FAIL: Found errors:")
        for e in errors[:10]:
            print(e)
    else:
        print("PASS: All theory classes in Home Room or Specific Room as expected.")

if __name__ == "__main__":
    verify_home_rooms()
