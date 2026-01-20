import random

def allowed_slots(day, constraints=None):
    """
    Determine allowed slots for a day
    Friday is half-day → P1-P4 (slots 0,1,2,3)
    Other days → P1-P6 (slots 0,1,2,3,4,5)
    
    Args:
        constraints: dict, e.g. {"half_days": ["Mon", "Tue", ...]}
    """
    if constraints and "half_days" in constraints:
        # For semesters with flexible half-day policies (like Sem 5),
        # Theory classes are strictly P1-P4 (slots 0-3).
        # P5-P6 are reserved for Labs (on the full day) or remain empty.
        return [0, 1, 2, 3]
        
    if day == "Fri":
        return [0, 1, 2, 3]  # P1-P4
    return [0, 1, 2, 3, 4, 5]  # P1-P6


def get_available_classroom(classrooms, subject_type, day, slot, classroom_usage, subject_name=None, class_name=None):
    """
    Find an available classroom for the given subject type, day, and slot
    Prioritizes specific lab rooms for lab subjects and class-specific classrooms
    
    Args:
        subject_name: Name of the subject (used to find specific lab rooms)
        class_name: Name of the class section (e.g., "5A", "5B")
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
            # Strict: If specific room is full, return None (don't schedule)
            return random.choice(available) if available else None
    
    # Check for class-specific rooms for theory subjects
    if class_name and subject_type == "THEORY":
        class_specific_rooms = [
            c["name"] for c in classrooms
            if c.get("class") == class_name and c["type"] == "THEORY"
        ]
        if class_specific_rooms:
            dedicated = class_specific_rooms[0]  # Always use the dedicated classroom
            # Strict: Check if dedicated room is actually free
            if dedicated not in classroom_usage.get(day, {}).get(slot, set()):
                return dedicated
            else:
                return None # Dedicated room blocked, try another slot
    
    # Otherwise, use general rooms matching the type
    suitable_classrooms = [
        c["name"] for c in classrooms 
        if (c["type"] == subject_type or c["type"] == "BOTH") and not c.get("subject") and not c.get("class")
    ]
    
    if not suitable_classrooms:
        suitable_classrooms = [c["name"] for c in classrooms if not c.get("subject") and not c.get("class")]
    
    # Filter out classrooms already in use at this time
    available = [
        room for room in suitable_classrooms 
        if room not in classroom_usage.get(day, {}).get(slot, set())
    ]
    
    # Strict: If no general room available, return None
    return random.choice(available) if available else None


def generate_random_timetable(classes, subjects, teachers, days, classrooms=None, common_classes=None, global_teacher_usage=None, semester_constraints=None):
    """
    Generate a random timetable with classroom allocation
    Rules:
    - No duplicate theory subjects in same day
    - Labs need 2 consecutive periods
    - Labs preferred in P3-P6, fallback to P1-P2
    - Common classes scheduled first
    - Checks against global_teacher_usage to avoid teacher conflicts across semesters
    - Respects semester_constraints for half-day logic
    
    Args:
        classes: list of class names
        subjects: dict {subject_name: {"count": int, "type": "THEORY"/"LAB"}}
        teachers: dict {subject_name: [teacher_names]}
        days: list of day names
        classrooms: list of dicts [{"name": str, "type": "THEORY"/"LAB"/"BOTH"}]
        common_classes: list of common class dicts
        global_teacher_usage: dict {teacher_name: {day: {slot}}} tracks booked slots for teachers
        semester_constraints: dict e.g. {"labs_on_full_day": True} 
                              If set, most days are half days, except one day chosen for Labs.
    """
    if classrooms is None:
        classrooms = []
    if common_classes is None:
        common_classes = []
    if global_teacher_usage is None:
        global_teacher_usage = {}
    if semester_constraints is None:
        semester_constraints = {}
        
    
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
                # Mark teacher as used
                if common_teacher:
                    if common_teacher not in global_teacher_usage:
                        global_teacher_usage[common_teacher] = {}
                    if common_day not in global_teacher_usage[common_teacher]:
                        global_teacher_usage[common_teacher][common_day] = set()
                    global_teacher_usage[common_teacher][common_day].add(common_period)
                    global_teacher_usage[common_teacher][common_day].add(common_period + 1)

            elif common_period < 6:  # Common activity
                tt[cls][common_day][common_period] = {
                    "subject": common_name,
                    "teacher": common_teacher,
                    "classroom": "",
                    "isCommon": True,
                    "isLab": False
                }
                # Mark teacher as used
                if common_teacher:
                    if common_teacher not in global_teacher_usage:
                        global_teacher_usage[common_teacher] = {}
                    if common_day not in global_teacher_usage[common_teacher]:
                        global_teacher_usage[common_teacher][common_day] = set()
                    global_teacher_usage[common_teacher][common_day].add(common_period)

    # Then allocate regular subjects
    # IMPORTANT: Sort subjects to prioritized LABS first!
    # This prevents Theory classes from filling up slots that Labs need.
    sorted_subjects_items = sorted(subjects.items(), key=lambda x: 0 if x[1].get("type") == "LAB" else 1)

    # Track used full days to distribute them across classes (Load Balancing)
    used_full_days = set()

    for cls in classes:
        # Clone constraints for this specific class
        cls_constraints = semester_constraints.copy()
        day_constraints = {} # Local restrictions for allowed_slots
        
        # Process constraints PER CLASS to allow randomization
        if cls_constraints.get("one_full_day_for_labs", False):
            if "force_lab_day" in cls_constraints:
                full_day = cls_constraints["force_lab_day"]
                cls_constraints["selected_full_day"] = full_day
            else:
                # Randomly select a full day (try to pick one not used yet)
                available_days = [d for d in days if d != "Fri"]
                candidates = [d for d in available_days if d not in used_full_days]
                if not candidates:
                    candidates = available_days # All days used, pick any
                
                full_day = random.choice(candidates)
                cls_constraints["selected_full_day"] = full_day
                used_full_days.add(full_day)
            
            # Set half days based on the selected full day
            if "half_day_count" in cls_constraints:
                half_day_count = cls_constraints["half_day_count"]
                # Set half days (all except full day, up to count)
                cls_constraints["half_days"] = [d for d in days if d != full_day][:half_day_count]
            else:
                # Default: all other days are half days
                cls_constraints["half_days"] = [d for d in days if d != full_day]

        elif "half_days" in semester_constraints:
            cls_constraints["half_days"] = semester_constraints["half_days"]
        
        # Determine day_constraints for this class iteration
        if "half_days" in cls_constraints:
            day_constraints["half_days"] = cls_constraints["half_days"]

        for sub, info in sorted_subjects_items:
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
                
                # Check available teachers
                possible_teachers = teachers[sub]
                random.shuffle(possible_teachers)
                t = None
                
                # We need to find a slot first to check teacher availability, or check teacher for potential slots?
                # For labs, enforce Friday-only if constraint is set
                if sub_type == "LAB" and "force_lab_day" in cls_constraints:
                    if day != cls_constraints["force_lab_day"]:
                        continue  # Skip non-Friday days for labs
                
                if sub_type == "LAB" and count >= 2:
                    # Lab needs 2 consecutive periods
                    # Valid pairs: (0,1)=P1-P2, (2,3)=P3-P4, (4,5)=P5-P6
                    # NEVER (3,4) which spans lunch break between P4 and P5
                    
                    # If we have a forced lab day, ensure it's the full day
                    if "selected_full_day" in cls_constraints and day == cls_constraints["selected_full_day"]:
                        # Full lab day - prioritize afternoon slots P5-P6, then fallback
                        lab_slot_pairs = [(4, 5), (2, 3), (0, 1)]  # Prefer P5-P6, never (3,4)
                    elif day in day_constraints.get("half_days", []):
                        # This is a half day - NO labs should be scheduled here at all!
                        # Skip this day entirely for labs
                        continue
                    elif day == "Fri":
                        # Friday default (if not set as half day) - limited slots
                        lab_slot_pairs = [(2, 3), (0, 1)]
                    else:
                        # Other full days (standard) - never include (3,4)
                        lab_slot_pairs = [(2, 3), (4, 5), (0, 1)]
                    
                    random.shuffle(lab_slot_pairs)
                    
                    for start, end in lab_slot_pairs:
                        if tt[cls][day][start] is None and tt[cls][day][end] is None:
                            # Slot is free for students. Now find a teacher free for BOTH slots.
                            available_teacher = None
                            for teacher_candidate in possible_teachers:
                                # Check global usage
                                busy_slots = global_teacher_usage.get(teacher_candidate, {}).get(day, set())
                                if start not in busy_slots and end not in busy_slots:
                                    available_teacher = teacher_candidate
                                    break
                            
                            if available_teacher:
                                # Allocate lab session
                                classroom = get_available_classroom(
                                    classrooms, sub_type, day, start, classroom_usage, sub, cls
                                ) if classrooms else None
                                
                                if classrooms and not classroom:
                                    continue # Skip if rooms defined but none available

                                
                                tt[cls][day][start] = {
                                    "subject": sub, 
                                    "teacher": available_teacher,
                                    "classroom": classroom
                                }
                                tt[cls][day][end] = {
                                    "subject": sub, 
                                    "teacher": available_teacher,
                                    "classroom": classroom
                                }
                                
                                # Mark classroom as used
                                if classroom:
                                    classroom_usage[day][start].add(classroom)
                                    classroom_usage[day][end].add(classroom)
                                
                                # Mark teacher as used
                                if available_teacher not in global_teacher_usage:
                                    global_teacher_usage[available_teacher] = {}
                                if day not in global_teacher_usage[available_teacher]:
                                    global_teacher_usage[available_teacher][day] = set()
                                global_teacher_usage[available_teacher][day].add(start)
                                global_teacher_usage[available_teacher][day].add(end)

                                count -= 2
                                break # Break slot loop, successful placement
                    
                else:
                    # Theory needs 1 slot
                    slots = allowed_slots(day, cls_constraints) # Pass class-specific constraints here
                    random.shuffle(slots)
                    
                    for i in slots:
                        if tt[cls][day][i] is None:
                            # Slot is free for students. Find a teacher free in this slot.
                            available_teacher = None
                            for teacher_candidate in possible_teachers:
                                busy_slots = global_teacher_usage.get(teacher_candidate, {}).get(day, set())
                                if i not in busy_slots:
                                    available_teacher = teacher_candidate
                                    break
                            
                            if available_teacher:
                                classroom = get_available_classroom(
                                    classrooms, sub_type, day, i, classroom_usage, sub, cls
                                ) if classrooms else None

                                if classrooms and not classroom:
                                    continue # Skip if rooms defined but none available


                                tt[cls][day][i] = {
                                    "subject": sub, 
                                    "teacher": available_teacher,
                                    "classroom": classroom
                                }
                                
                                # Mark classroom as used
                                if classroom:
                                    classroom_usage[day][i].add(classroom)
                                
                                # Mark teacher as used
                                if available_teacher not in global_teacher_usage:
                                    global_teacher_usage[available_teacher] = {}
                                if day not in global_teacher_usage[available_teacher]:
                                    global_teacher_usage[available_teacher][day] = set()
                                global_teacher_usage[available_teacher][day].add(i)

                                count -= 1
                                break # Break slot loop, successful placement

    return tt