import random

def allowed_slots(day):
    """
    Friday is half-day → P1-P4 (slots 0,1,2,3)
    Other days → P1-P6 (slots 0,1,2,3,4,5)
    Note: Breaks are added in display, not in data structure
    """
    if day == "Fri":
        return [0, 1, 2, 3]  # P1-P4
    return [0, 1, 2, 3, 4, 5]  # P1-P6


def get_available_classroom(classrooms, subject_type, day, slot, classroom_usage, subject_name=None):
    """
    Find an available classroom for the given subject type, day, and slot
    Prioritizes specific lab rooms for lab subjects
    
    Args:
        subject_name: Name of the subject (used to find specific lab rooms)
    """
    # First, check for specific rooms for this subject (e.g., "Physics Lab" for "Physics")
    if subject_name:
        specific_classrooms = [
            c["name"] for c in classrooms 
            if c.get("subject") == subject_name
        ]
        if specific_classrooms:
            # Use specific room if available
            available = [
                room for room in specific_classrooms 
                if room not in classroom_usage.get(day, {}).get(slot, set())
            ]
            return random.choice(available) if available else random.choice(specific_classrooms)
    
    # Otherwise, use general rooms matching the type
    suitable_classrooms = [
        c["name"] for c in classrooms 
        if (c["type"] == subject_type or c["type"] == "BOTH") and not c.get("subject")
    ]
    
    if not suitable_classrooms:
        suitable_classrooms = [c["name"] for c in classrooms if not c.get("subject")]
    
    # Filter out classrooms already in use at this time
    available = [
        room for room in suitable_classrooms 
        if room not in classroom_usage.get(day, {}).get(slot, set())
    ]
    
    return random.choice(available) if available else (
        random.choice(suitable_classrooms) if suitable_classrooms else None
    )


def generate_random_timetable(classes, subjects, teachers, days, classrooms=None, common_classes=None):
    """
    Generate a random timetable with classroom allocation
    Rules:
    - No duplicate theory subjects in same day
    - Labs need 2 consecutive periods
    - Labs preferred in P3-P6, fallback to P1-P2
    - Common classes scheduled first
    
    Args:
        classes: list of class names
        subjects: dict {subject_name: {"count": int, "type": "THEORY"/"LAB"}}
        teachers: dict {subject_name: [teacher_names]}
        days: list of day names
        classrooms: list of dicts [{"name": str, "type": "THEORY"/"LAB"/"BOTH"}]
        common_classes: list of common class dicts
    """
    if classrooms is None:
        classrooms = []
    if common_classes is None:
        common_classes = []
    
    # 6 slots per day for 6 teaching periods
    tt = {c: {d: [None] * 6 for d in days} for c in classes}
    
    # Track classroom usage across all classes
    classroom_usage = {d: {i: set() for i in range(6)} for d in days}
    
    # First, schedule common classes
    for common in common_classes:
        common_name = common['name']
        common_type = common.get('type', 'COMMON')
        common_day = common['day']
        common_period = common['period']
        common_periods = common.get('periods', 1)
        common_class_list = common['classes']
        common_teacher = common.get('teacher', '')
        
        # Determine which classes this applies to
        if common_class_list == "ALL":
            applicable_classes = classes
        else:
            applicable_classes = [c for c in classes if c in common_class_list]
        
        # Schedule for all applicable classes
        for cls in applicable_classes:
            if common_periods == 2 and common_period < 5:  # Common lab
                tt[cls][common_day][common_period] = {
                    "subject": common_name,
                    "teacher": common_teacher,
                    "classroom": "",
                    "isCommon": True,
                    "isLab": common_type == "LAB"
                }
                tt[cls][common_day][common_period + 1] = {
                    "subject": common_name + " (cont.)",
                    "teacher": common_teacher,
                    "classroom": "",
                    "isCommon": True,
                    "isLab": common_type == "LAB"
                }
            elif common_period < 6:  # Common activity
                tt[cls][common_day][common_period] = {
                    "subject": common_name,
                    "teacher": common_teacher,
                    "classroom": "",
                    "isCommon": True,
                    "isLab": False
                }

    # Then allocate regular subjects
    for cls in classes:
        for sub, info in subjects.items():
            count = info["count"]
            sub_type = info.get("type", "THEORY")

            attempts = 0
            max_attempts = 1000

            while count > 0 and attempts < max_attempts:
                attempts += 1
                day = random.choice(days)
                
                # Check if this theory subject already exists in this day
                if sub_type == "THEORY":
                    day_subjects = [
                        slot["subject"] for slot in tt[cls][day] 
                        if slot and slot.get("subject") and not slot.get("isCommon")
                    ]
                    if sub in day_subjects:
                        continue  # Skip this day, subject already scheduled

                # Get a teacher for this subject
                if sub not in teachers or not teachers[sub]:
                    break
                t = random.choice(teachers[sub])
                
                # Get an available classroom (with subject-specific room support)
                classroom = get_available_classroom(
                    classrooms, sub_type, day, 0, classroom_usage, sub
                ) if classrooms else None

                if sub_type == "LAB" and count >= 2:
                    # Lab needs 2 consecutive periods
                    # Priority: P3-P6 (slots 2-5), fallback: P1-P2 (slots 0-1)
                    
                    if day == "Fri":
                        # Friday half-day: only P3-P4 available (slots 2-3)
                        lab_slot_pairs = [(2, 3)]
                    else:
                        # Full day: prefer P3-P6, fallback P1-P2
                        lab_slot_pairs = [(2, 3), (3, 4), (4, 5), (0, 1)]
                    
                    placed = False
                    random.shuffle(lab_slot_pairs)
                    
                    for start, end in lab_slot_pairs:
                        if tt[cls][day][start] is None and tt[cls][day][end] is None:
                            # Allocate lab session
                            tt[cls][day][start] = {
                                "subject": sub, 
                                "teacher": t,
                                "classroom": classroom
                            }
                            tt[cls][day][end] = {
                                "subject": sub, 
                                "teacher": t,
                                "classroom": classroom
                            }
                            
                            # Mark classroom as used
                            if classroom:
                                classroom_usage[day][start].add(classroom)
                                classroom_usage[day][end].add(classroom)
                            
                            count -= 2
                            placed = True
                            break
                    
                else:
                    # Theory needs 1 slot
                    slots = allowed_slots(day)
                    random.shuffle(slots)
                    
                    for i in slots:
                        if tt[cls][day][i] is None:
                            tt[cls][day][i] = {
                                "subject": sub, 
                                "teacher": t,
                                "classroom": classroom
                            }
                            
                            # Mark classroom as used
                            if classroom:
                                classroom_usage[day][i].add(classroom)
                            
                            count -= 1
                            break

    return tt