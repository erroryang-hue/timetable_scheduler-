from config import BREAK_SLOTS

def is_break(slot):
    return slot in BREAK_SLOTS


def teacher_busy(timetable, teacher, day, slot):
    for cls in timetable:
        cell = timetable[cls][day][slot]
        if cell and cell["teacher"] == teacher:
            return True
    return False
