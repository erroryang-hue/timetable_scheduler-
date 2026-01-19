from scheduler.generator_random import generate_random_timetable
from scheduler.fitness import fitness

def genetic_scheduler(classes, subjects, teachers, days, classrooms=None, common_classes=None):
    """
    Generate timetable using genetic algorithm with classroom allocation and common classes
    
    Args:
        classes: list of class names
        subjects: dict of subjects
        teachers: dict of teachers by subject
        days: list of days
        classrooms: list of classroom dicts (optional)
        common_classes: list of common class dicts (optional)
    
    Returns:
        Best timetable found
    """
    if classrooms is None:
        classrooms = []
    if common_classes is None:
        common_classes = []
    
    # Initial population
    pop = [
        generate_random_timetable(classes, subjects, teachers, days, classrooms, common_classes) 
        for _ in range(40)
    ]

    # Evolution loop
    for generation in range(60):
        # Sort by fitness (higher is better)
        pop = sorted(pop, key=lambda x: -fitness(x, subjects))[:10]
        
        # Keep top 10 and generate 30 new random ones
        pop += [
            generate_random_timetable(classes, subjects, teachers, days, classrooms, common_classes) 
            for _ in range(30)
        ]

    # Return the best timetable
    return pop[0]
