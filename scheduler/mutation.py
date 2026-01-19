import random, copy
from config import TEACHING_SLOTS, FRIDAY_SLOTS

def mutate(tt, rate=0.05):
    child = copy.deepcopy(tt)
    for cls in child:
        for day in child[cls]:
            slots = FRIDAY_SLOTS if day == "Fri" else TEACHING_SLOTS
            for s in slots:
                if random.random() < rate:
                    child[cls][day][s] = None
    return child
