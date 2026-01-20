# Data Configuration for All Semesters

SEMESTER_1 = {
    "classes": ["1A", "1B"],
    "subjects": {
        "MATH1": {"count": 5, "type": "THEORY"},
        "PHY": {"count": 4, "type": "THEORY"},
        "PHY_LAB": {"count": 2, "type": "LAB"},
        "CHEM": {"count": 4, "type": "THEORY"},
        "CHEM_LAB": {"count": 2, "type": "LAB"},
        "ENG": {"count": 3, "type": "THEORY"},
        "EG": {"count": 4, "type": "THEORY"},
        "C_PROG": {"count": 3, "type": "THEORY"},
        "C_LAB": {"count": 2, "type": "LAB"}
    },
    "teachers": {
        "MATH1": ["Dr. Sharma"],
        "PHY": ["Dr. Patel"],
        "PHY_LAB": ["Dr. Patel"],
        "CHEM": ["Dr. Kumar"],
        "CHEM_LAB": ["Dr. Kumar"],
        "ENG": ["Prof. Singh"],
        "EG": ["Prof. Reddy"],
        "C_PROG": ["Prof. Gupta"],
        "C_LAB": ["Prof. Gupta"]
    },
    "classrooms": [
        {"name": "R101", "type": "THEORY", "class": "1A"},
        {"name": "R102", "type": "THEORY", "class": "1B"},
        {"name": "Drawing Hall", "type": "THEORY", "subject": "EG"},
        {"name": "Physics Lab", "type": "LAB", "subject": "PHY_LAB"},
        {"name": "Chemistry Lab", "type": "LAB", "subject": "CHEM_LAB"},
        {"name": "Computer Lab 1", "type": "LAB", "subject": "C_LAB"}
    ],
    "commonClasses": [
        {
            "name": "Orientation",
            "type": "COMMON",
            "day": "Mon",
            "period": 0,
            "periods": 1,
            "classes": "ALL",
            "teacher": "Dean"
        }
    ]
}

SEMESTER_3 = {
    "classes": ["3A", "3B"],
    "subjects": {
        "MATH3": {"count": 5, "type": "THEORY"},
        "DSA": {"count": 4, "type": "THEORY"},
        "DSA_LAB": {"count": 4, "type": "LAB"},
        "OS": {"count": 4, "type": "THEORY"},
        "OS_LAB": {"count": 2, "type": "LAB"},
        "ADLD": {"count": 4, "type": "THEORY"},
        "ADLD_LAB": {"count": 4, "type": "LAB"},
        "BC": {"count": 3, "type": "THEORY"},
        "DTL": {"count": 2, "type": "THEORY"}
    },
    "teachers": {
        "MATH3": ["SUMA", "NIRANJAN", "JAYALATHA", "KIRAN"],
        "DSA": ["SUMA_B", "DEEPAMALA", "KARANAM SUNIL"],
        "DSA_LAB": ["DEEPAMALA"],
        "OS": ["PAVITHRA", "JOTHI"],
        "OS_LAB": ["PAVITHRA"],
        "ADLD": ["MOHANA", "SUJATHA", "RAMESH"],
        "ADLD_LAB": ["BADARI"],
        "BC": ["T4", "T5", "T3"],
        "DTL": ["T4"]
    },
    "classrooms": [
        # Dedicated theory classroom for 3A
        {"name": "RVUF001", "type": "THEORY", "class": "3A"},
        # Dedicated theory classroom for 3B  
        {"name": "RVUF002", "type": "THEORY", "class": "3B"},
        # General theory rooms (backup)
        {"name": "RVUF003", "type": "THEORY"},
        {"name": "RVUF004", "type": "THEORY"},
        {"name": "RVUF101", "type": "THEORY"},
        # Specific lab rooms
        {"name": "KOTAK1", "type": "LAB", "subject": "OS_LAB"},
        {"name": "KOTAK2", "type": "LAB", "subject": "DSA_LAB"},
        {"name": "CBL1", "type": "LAB", "subject": "ADLD_LAB"}
    ],
    "commonClasses": []
}

SEMESTER_5 = {
    "classes": ["5A", "5B"],
    "subjects": {
        "DBMS": {"count": 3, "type": "THEORY"},
        "TOC": {"count": 3, "type": "THEORY"},
        "POME": {"count": 3, "type": "THEORY"},
        "AIML": {"count": 3, "type": "THEORY"},
        "BASKET_COURSE": {"count": 3, "type": "THEORY"},
        "COUNSELLING": {"count": 1, "type": "THEORY"},
        # Labs - one lab per Friday afternoon (rotates weekly)
        "DBMS_LAB": {"count": 2, "type": "LAB"},
        "AIML_LAB": {"count": 2, "type": "LAB"},
        "TOC_LAB": {"count": 2, "type": "LAB"}
    },
    "teachers": {
        "DBMS": ["Prof. Meena"],
        "TOC": ["Prof. Lakshmi"],
        "POME": ["Dr. Ravi"],
        "AIML": ["Dr. Venkat"],
        "BASKET_COURSE": ["Guest Faculty"],
        "COUNSELLING": ["Counselor"],
        "DBMS_LAB": ["Prof. Meena"],
        "AIML_LAB": ["Dr. Venkat"],
        "TOC_LAB": ["Prof. Lakshmi"]
    },
    "classrooms": [
        # Dedicated theory classroom for 5A
        {"name": "RVUF104", "type": "THEORY", "class": "5A"},
        # Dedicated theory classroom for 5B
        {"name": "RVUF105", "type": "THEORY", "class": "5B"},
        # Specific lab rooms for lab subjects
        {"name": "Database Lab - A2 BATCH", "type": "LAB", "subject": "DBMS_LAB"},
        {"name": "AIML Lab - A1 BATCH", "type": "LAB", "subject": "AIML_LAB"},
        {"name": "TOC Lab", "type": "LAB", "subject": "TOC_LAB"}
    ],
    "commonClasses": [],
    "constraints": {
        "one_full_day_for_labs": True,
        # Any day can be the full day with lab after lunch (P5-P6)
        # 4 days are half-days (P1-P4 only), 1 day has lab in afternoon
        "half_day_count": 4,  # 4 days must be half-days
        "lab_afternoon_count": 1  # 1 day has lab after lunch
    }
}

SEMESTER_7 = {
    "classes": ["7A", "7B"],
    "subjects": {
        "ML": {"count": 4, "type": "THEORY"},
        "ML_LAB": {"count": 2, "type": "LAB"},
        "CLOUD": {"count": 3, "type": "THEORY"},
        "BLOCKCHAIN": {"count": 3, "type": "THEORY"},
        "IOT": {"count": 3, "type": "THEORY"},
        "IOT_LAB": {"count": 2, "type": "LAB"},
        "CYBER": {"count": 4, "type": "THEORY"},
        "PROJECT": {"count": 4, "type": "LAB"},
        "ELECTIVE": {"count": 3, "type": "THEORY"}
    },
    "teachers": {
        "ML": ["Dr. Priya"],
        "ML_LAB": ["Dr. Priya"],
        "CLOUD": ["Prof. Anand"],
        "BLOCKCHAIN": ["Prof. Suresh"],
        "IOT": ["Dr. Madhavi"],
        "IOT_LAB": ["Dr. Madhavi"],
        "CYBER": ["Prof. Krishna"],
        "PROJECT": ["Various"],
        "ELECTIVE": ["Guest Faculty"]
    },
    "classrooms": [
        {"name": "R301", "type": "THEORY", "class": "7A"},
        {"name": "R302", "type": "THEORY", "class": "7B"},
        {"name": "ML Lab", "type": "LAB", "subject": "ML_LAB"},
        {"name": "IoT Lab", "type": "LAB", "subject": "IOT_LAB"},
        {"name": "Project Lab", "type": "LAB", "subject": "PROJECT"}
    ],
    "commonClasses": [
        {
            "name": "Industry Talk",
            "type": "COMMON",
            "day": "Wed",
            "period": 5,
            "periods": 1,
            "classes": "ALL",
            "teacher": "Guest"
        },
        {
            "name": "Placement Training",
            "type": "COMMON",
            "day": "Fri",
            "period": 2,
            "periods": 2,
            "classes": "ALL",
            "teacher": "Training Team"
        }
    ]
}

ALL_SEMESTERS = {
    "1": SEMESTER_1,
    "3": SEMESTER_3,
    "5": SEMESTER_5,
    "7": SEMESTER_7
}
