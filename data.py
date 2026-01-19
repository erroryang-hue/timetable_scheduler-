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
        {"name": "R101", "type": "THEORY"},
        {"name": "R102", "type": "THEORY"},
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
        "DTL": ["T4"] # Assuming T4 teaches DTL as implied by sample image or default
    },
    "classrooms": [
        {"name": "RVUF001", "type": "THEORY"},
        {"name": "RVUF002", "type": "THEORY"},
        {"name": "RVUF003", "type": "THEORY"},
        {"name": "RVUF004", "type": "THEORY"},
        {"name": "RVUF101", "type": "THEORY"},
        {"name": "KOTAK1", "type": "LAB", "subject": "OS_LAB"},
        {"name": "KOTAK2", "type": "LAB", "subject": "DSA_LAB"},
        {"name": "CBL1", "type": "LAB", "subject": "ADLD_LAB"}
    ],
    "commonClasses": []
}

SEMESTER_5 = {
    "classes": ["5A", "5B"],
    "subjects": {
        "CN": {"count": 4, "type": "THEORY"},
        "CN_LAB": {"count": 2, "type": "LAB"},
        "DBMS": {"count": 4, "type": "THEORY"},
        "DBMS_LAB": {"count": 2, "type": "LAB"},
        "SE": {"count": 4, "type": "THEORY"},
        "TOC": {"count": 3, "type": "THEORY"},
        "WEB": {"count": 3, "type": "THEORY"},
        "WEB_LAB": {"count": 2, "type": "LAB"},
        "AI": {"count": 4, "type": "THEORY"},
        "AI_LAB": {"count": 2, "type": "LAB"}
    },
    "teachers": {
        "CN": ["Dr. Arun"],
        "CN_LAB": ["Dr. Arun"],
        "DBMS": ["Prof. Meena"],
        "DBMS_LAB": ["Prof. Meena"],
        "SE": ["Dr. Ravi"],
        "TOC": ["Prof. Lakshmi"],
        "WEB": ["Prof. Karthik"],
        "WEB_LAB": ["Prof. Karthik"],
        "AI": ["Dr. Venkat"],
        "AI_LAB": ["Dr. Venkat"]
    },
    "classrooms": [
        {"name": "R201", "type": "THEORY"},
        {"name": "R202", "type": "THEORY"},
        {"name": "R203", "type": "THEORY"},
        {"name": "Network Lab", "type": "LAB", "subject": "CN_LAB"},
        {"name": "Database Lab", "type": "LAB", "subject": "DBMS_LAB"},
        {"name": "Web Lab", "type": "LAB", "subject": "WEB_LAB"},
        {"name": "AI Lab", "type": "LAB", "subject": "AI_LAB"}
    ],
    "commonClasses": [
        {
            "name": "Technical Seminar",
            "type": "COMMON",
            "day": "Fri",
            "period": 4,
            "periods": 1,
            "classes": "ALL",
            "teacher": "HOD"
        }
    ],
    "constraints": {
        "one_full_day_for_labs": True
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
        {"name": "R301", "type": "THEORY"},
        {"name": "R302", "type": "THEORY"},
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
