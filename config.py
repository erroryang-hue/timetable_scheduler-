DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# Total teaching periods per day (excluding breaks)
TOTAL_PERIODS = 6

# Teaching periods: P1, P2, P3, P4, P5, P6
# Array indices: 0, 1, 2, 3, 4, 5

# Friday is half-day: P1-P4 only
FRIDAY_PERIODS = 4

# Breaks are inserted during display:
# - Break between P2 and P3
# - Lunch between P4 and P5

# For display purposes only (not in data structure)
BREAK_POSITIONS = {
    "BREAK": "after P2",  # Displayed between P2 and P3
    "LUNCH": "after P4"   # Displayed between P4 and P5
}