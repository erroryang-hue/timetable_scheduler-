def fitness(timetable, subjects):
    """
    Calculate fitness score for a timetable
    Higher score = better timetable
    
    Penalties for:
    - Duplicate theory subjects in same day
    - Labs not in consecutive periods
    - Labs in P1-P2 when P3-P6 available
    - Teacher conflicts
    - Classroom conflicts
    """
    score = 1000  # Start with perfect score
    
    for cls in timetable:
        for day in timetable[cls]:
            day_schedule = timetable[cls][day]
            
            # Check for duplicate theory subjects in same day
            theory_subjects = []
            for slot in day_schedule:
                if slot and slot.get("subject"):
                    subject_name = slot["subject"].replace(" (cont.)", "")
                    
                    # Find subject type
                    subject_type = "THEORY"
                    for subj_name, info in subjects.items():
                        if subj_name == subject_name:
                            subject_type = info.get("type", "THEORY")
                            break
                    
                    if subject_type == "THEORY":
                        if subject_name in theory_subjects:
                            score -= 50  # Heavy penalty for duplicate theory
                        else:
                            theory_subjects.append(subject_name)
            
            # Check lab placement and continuity
            for i in range(len(day_schedule) - 1):
                curr = day_schedule[i]
                next_slot = day_schedule[i + 1]
                
                if curr and curr.get("subject") and "LAB" in str(curr.get("subject", "")):
                    # Check if lab has consecutive period
                    if not next_slot or curr["subject"] != next_slot.get("subject"):
                        score -= 100  # Heavy penalty for non-consecutive lab
                    
                    # Penalize labs in P1-P2 (slots 0-1)
                    if i == 0:  # Lab starts at P1
                        score -= 20  # Moderate penalty, prefer P3-P6
    
    # Check for teacher conflicts (same teacher in multiple classes at same time)
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
        for slot in range(6):
            teachers_at_slot = []
            for cls in timetable:
                cell = timetable[cls][day][slot]
                if cell and cell.get("teacher"):
                    teacher = cell["teacher"]
                    if teacher in teachers_at_slot:
                        score -= 100  # Heavy penalty for teacher conflict
                    else:
                        teachers_at_slot.append(teacher)
    
    # Check for classroom conflicts
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
        for slot in range(6):
            classrooms_at_slot = []
            for cls in timetable:
                cell = timetable[cls][day][slot]
                if cell and cell.get("classroom"):
                    classroom = cell["classroom"]
                    if classroom in classrooms_at_slot:
                        score -= 100  # Heavy penalty for classroom conflict
                    else:
                        classrooms_at_slot.append(classroom)
    
    # Bonus for well-distributed schedule
    for cls in timetable:
        for day in timetable[cls]:
            filled_slots = sum(1 for slot in timetable[cls][day] if slot)
            if 3 <= filled_slots <= 5:  # Good balance
                score += 5
    
    return max(0, score)  # Don't go negative


def count_violations(timetable, subjects):
    """
    Count specific violations for debugging
    
    Returns:
        dict with violation counts
    """
    violations = {
        "duplicate_theory": 0,
        "non_consecutive_lab": 0,
        "lab_in_p1p2": 0,
        "teacher_conflict": 0,
        "classroom_conflict": 0
    }
    
    for cls in timetable:
        for day in timetable[cls]:
            day_schedule = timetable[cls][day]
            
            # Check duplicate theory
            theory_subjects = []
            for slot in day_schedule:
                if slot and slot.get("subject"):
                    subject_name = slot["subject"].replace(" (cont.)", "")
                    subject_type = "THEORY"
                    for subj_name, info in subjects.items():
                        if subj_name == subject_name:
                            subject_type = info.get("type", "THEORY")
                            break
                    
                    if subject_type == "THEORY":
                        if subject_name in theory_subjects:
                            violations["duplicate_theory"] += 1
                        else:
                            theory_subjects.append(subject_name)
            
            # Check lab placement
            for i in range(len(day_schedule) - 1):
                curr = day_schedule[i]
                next_slot = day_schedule[i + 1]
                
                if curr and curr.get("subject") and "LAB" in str(curr.get("subject", "")):
                    if not next_slot or curr["subject"] != next_slot.get("subject"):
                        violations["non_consecutive_lab"] += 1
                    
                    if i == 0:
                        violations["lab_in_p1p2"] += 1
    
    # Check teacher conflicts
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
        for slot in range(6):
            teachers = [
                timetable[cls][day][slot].get("teacher")
                for cls in timetable
                if timetable[cls][day][slot] and timetable[cls][day][slot].get("teacher")
            ]
            if len(teachers) != len(set(teachers)):
                violations["teacher_conflict"] += 1
    
    # Check classroom conflicts
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
        for slot in range(6):
            classrooms = [
                timetable[cls][day][slot].get("classroom")
                for cls in timetable
                if timetable[cls][day][slot] and timetable[cls][day][slot].get("classroom")
            ]
            if len(classrooms) != len(set(classrooms)):
                violations["classroom_conflict"] += 1
    
    return violations