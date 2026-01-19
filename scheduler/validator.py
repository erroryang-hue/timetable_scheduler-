from config import BREAK_SLOTS

def is_break(slot):
    """Check if a slot is a break"""
    return slot in BREAK_SLOTS


def teacher_busy(timetable, teacher, day, slot):
    """Check if a teacher is already assigned at this time slot"""
    for cls in timetable:
        cell = timetable[cls][day][slot]
        if cell and cell.get("teacher") == teacher:
            return True
    return False


def classroom_busy(timetable, classroom, day, slot):
    """
    Check if a classroom is already occupied at this time slot
    
    Args:
        timetable: dict of timetable data
        classroom: name of the classroom
        day: day of the week
        slot: slot number
    
    Returns:
        bool: True if classroom is busy, False otherwise
    """
    if not classroom:
        return False
    
    for cls in timetable:
        cell = timetable[cls][day][slot]
        if cell and cell.get("classroom") == classroom:
            return True
    return False


def validate_timetable(timetable):
    """
    Validate the timetable for conflicts
    
    Returns:
        dict: {
            "valid": bool,
            "errors": list of error messages
        }
    """
    errors = []
    
    for cls in timetable:
        for day in timetable[cls]:
            for slot, cell in enumerate(timetable[cls][day]):
                if not cell or is_break(slot):
                    continue
                
                teacher = cell.get("teacher")
                classroom = cell.get("classroom")
                
                # Check teacher conflicts
                if teacher:
                    conflict_count = sum(
                        1 for other_cls in timetable
                        if timetable[other_cls][day][slot] 
                        and timetable[other_cls][day][slot].get("teacher") == teacher
                    )
                    if conflict_count > 1:
                        errors.append(
                            f"Teacher {teacher} has conflict on {day} slot {slot}"
                        )
                
                # Check classroom conflicts
                if classroom:
                    conflict_count = sum(
                        1 for other_cls in timetable
                        if timetable[other_cls][day][slot] 
                        and timetable[other_cls][day][slot].get("classroom") == classroom
                    )
                    if conflict_count > 1:
                        errors.append(
                            f"Classroom {classroom} has conflict on {day} slot {slot}"
                        )
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }