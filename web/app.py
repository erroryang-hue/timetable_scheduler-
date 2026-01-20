from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path to allow importing scheduler and config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduler.generator_random import generate_random_timetable
from config import DAYS

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    current_semester = str(data.get("currentSemester", 3))
    semesters = data.get("semesters", {})
    
    # Get current semester data to ensure we have it
    if current_semester not in semesters:
         return jsonify({"error": f"Data for semester {current_semester} not found"}), 400

    # Initialize global teacher usage
    global_teacher_usage = {}

    # 1. Pre-fill global_teacher_usage by generating/processing OTHER semesters
    # We iterate through all OTHER semesters provided in the request
    for sem_id, sem_data in semesters.items():
        if str(sem_id) == current_semester:
            continue
            
        # We need to run the generator for other semesters to populate usage
        # We don't care about their actual timetable output, just the side effect on global_teacher_usage
        if sem_data.get("classes") and sem_data.get("subjects") and sem_data.get("teachers"):
            generate_random_timetable(
                sem_data.get("classes", []),
                sem_data.get("subjects", {}), # Expecting dict based on new data structure
                sem_data.get("teachers", {}),
                DAYS,
                sem_data.get("classrooms", []),
                sem_data.get("commonClasses", []),
                global_teacher_usage=global_teacher_usage,
                semester_constraints=sem_data.get("constraints", {})
            )

    # 2. Generate timetable for the CURRENT semester
    current_sem_data = semesters[current_semester]
    
    # Check format of 'subjects' (handle list vs dict mismatch from frontend)
    subjects_input = current_sem_data.get("subjects", [])
    subjects_dict = {}
    
    if isinstance(subjects_input, list):
        for sub in subjects_input:
            name = sub["name"]
            subjects_dict[name] = {
                "count": sub["periods"],
                "type": sub.get("type", "THEORY")
            }
    else:
        subjects_dict = subjects_input

    # Check format of 'teachers'
    teachers_input = current_sem_data.get("teachers", [])
    teachers_dict = {}
    
    if isinstance(teachers_input, list):
        for t in teachers_input:
            sub = t["subject"]
            name = t["name"]
            if sub not in teachers_dict:
                teachers_dict[sub] = []
            teachers_dict[sub].append(name)
    else:
        teachers_dict = teachers_input

    try:
        timetable = generate_random_timetable(
            current_sem_data.get("classes", []),
            subjects_dict,
            teachers_dict,
            DAYS,
            current_sem_data.get("classrooms", []),
            current_sem_data.get("commonClasses", []),
            global_teacher_usage=global_teacher_usage,
            semester_constraints=current_sem_data.get("constraints", {})
        )
        
        return jsonify(timetable)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR generating Semester {current_semester}:")
        print(error_details)
        return jsonify({
            "error": f"Failed to generate timetable: {str(e)}",
            "details": error_details
        }), 500


if __name__ == "__main__":
    app.run(debug=True)