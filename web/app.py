from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    classes = data.get("classes", [])
    subjects = data.get("subjects", [])
    teachers = data.get("teachers", [])
    classrooms = data.get("classrooms", [])
    common_classes = data.get("commonClasses", [])

    if not classes or not subjects or not teachers:
        return jsonify({"error": "Missing input"}), 400

    # Generate timetable with classroom allocation and common classes
    timetable = generate_timetable_with_classrooms(
        classes, subjects, teachers, classrooms, common_classes
    )

    return jsonify(timetable)


def generate_timetable_with_classrooms(classes, subjects, teachers, classrooms, common_classes=None):
    """
    Generate a timetable with classroom allocation
    Rules:
    - No duplicate theory subjects in same day
    - Labs need 2 consecutive periods
    - Labs preferred in P3-P6, fallback to P1-P2
    - Common classes scheduled at same time for specified classes
    - Specific lab rooms for specific lab subjects
    """
    if common_classes is None:
        common_classes = []
    
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    timetable = {}
    
    for cls in classes:
        # 6 slots for 6 periods
        timetable[cls] = {
            "Mon": [None] * 6,
            "Tue": [None] * 6,
            "Wed": [None] * 6,
            "Thu": [None] * 6,
            "Fri": [None] * 6
        }
    
    # First, schedule common classes
    for common in common_classes:
        common_name = common['name']
        common_type = common.get('type', 'COMMON')
        common_day = common['day']
        common_period = common['period']
        common_periods = common.get('periods', 1)  # 2 for labs, 1 for others
        common_class_list = common['classes']
        common_teacher = common.get('teacher', '')
        
        # Determine which classes this applies to
        if common_class_list == "ALL":
            applicable_classes = classes
        else:
            applicable_classes = [c for c in classes if c in common_class_list]
        
        # Schedule this common class for all applicable classes
        for cls in applicable_classes:
            if common_periods == 2 and common_period < 5:  # Common lab needs 2 periods
                timetable[cls][common_day][common_period] = {
                    "subject": common_name,
                    "teacher": common_teacher,
                    "classroom": "",
                    "isCommon": True,
                    "isLab": common_type == "LAB"
                }
                timetable[cls][common_day][common_period + 1] = {
                    "subject": common_name + " (cont.)",
                    "teacher": common_teacher,
                    "classroom": "",
                    "isCommon": True,
                    "isLab": common_type == "LAB"
                }
            elif common_period < 6:  # Common activity
                timetable[cls][common_day][common_period] = {
                    "subject": common_name,
                    "teacher": common_teacher,
                    "classroom": "",
                    "isCommon": True,
                    "isLab": False
                }

    # Then, allocate regular subjects (avoiding common class slots)
    for cls in classes:
        for subject in subjects:
            periods_to_allocate = subject['periods']
            subject_name = subject['name']
            subject_type = subject.get('type', 'THEORY')
            
            # Find teachers for this subject
            subject_teachers = [t['name'] for t in teachers if t['subject'] == subject_name]
            if not subject_teachers:
                continue
            
            # Find suitable classrooms
            # First, check for specific lab rooms for this subject
            specific_classrooms = [
                c['name'] for c in classrooms 
                if c.get('subject') == subject_name
            ]
            
            if specific_classrooms:
                suitable_classrooms = specific_classrooms
            else:
                # Otherwise, use general rooms of matching type
                suitable_classrooms = [
                    c['name'] for c in classrooms 
                    if (c['type'] == subject_type or c['type'] == 'BOTH') and not c.get('subject')
                ]
            
            if not suitable_classrooms and classrooms:
                suitable_classrooms = [c['name'] for c in classrooms if not c.get('subject')]
            
            attempts = 0
            max_attempts = 1000
            
            while periods_to_allocate > 0 and attempts < max_attempts:
                attempts += 1
                day = random.choice(days)
                
                # Check if this theory subject already exists in this day
                if subject_type == "THEORY":
                    day_subjects = [
                        slot['subject'] for slot in timetable[cls][day] 
                        if slot and slot.get('subject') and not slot.get('isCommon')
                    ]
                    if subject_name in day_subjects:
                        continue  # Skip this day, subject already scheduled
                
                teacher = random.choice(subject_teachers)
                classroom = random.choice(suitable_classrooms) if suitable_classrooms else ""
                
                if subject_type == "LAB" and periods_to_allocate >= 2:
                    # Try to place lab in P3-P6 first (slots 2-5)
                    if day == "Fri":
                        lab_slots = [(2, 3)]
                    else:
                        lab_slots = [(2, 3), (3, 4), (4, 5)]
                    
                    placed = False
                    
                    # Try preferred slots (P3-P6)
                    for start_slot, end_slot in lab_slots:
                        if (timetable[cls][day][start_slot] is None and 
                            timetable[cls][day][end_slot] is None):
                            timetable[cls][day][start_slot] = {
                                "subject": subject_name,
                                "teacher": teacher,
                                "classroom": classroom
                            }
                            timetable[cls][day][end_slot] = {
                                "subject": subject_name + " (cont.)",
                                "teacher": teacher,
                                "classroom": classroom
                            }
                            periods_to_allocate -= 2
                            placed = True
                            break
                    
                    # If not placed, try P1-P2 (slots 0-1) as fallback
                    if not placed and day != "Fri":
                        if (timetable[cls][day][0] is None and 
                            timetable[cls][day][1] is None):
                            timetable[cls][day][0] = {
                                "subject": subject_name,
                                "teacher": teacher,
                                "classroom": classroom
                            }
                            timetable[cls][day][1] = {
                                "subject": subject_name + " (cont.)",
                                "teacher": teacher,
                                "classroom": classroom
                            }
                            periods_to_allocate -= 2
                            placed = True
                    
                else:
                    # Theory subject - single period
                    if day == "Fri":
                        available_slots = [0, 1, 2, 3]  # P1-P4
                    else:
                        available_slots = [0, 1, 2, 3, 4, 5]  # P1-P6
                    
                    random.shuffle(available_slots)
                    
                    for slot in available_slots:
                        if timetable[cls][day][slot] is None:
                            timetable[cls][day][slot] = {
                                "subject": subject_name,
                                "teacher": teacher,
                                "classroom": classroom
                            }
                            periods_to_allocate -= 1
                            break

    return timetable


if __name__ == "__main__":
    app.run(debug=True)