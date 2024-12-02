'''Day 2 of the advent.'''
import numpy as np

with open('Day 2\levels.txt', 'r') as file:
    lines = []
    for line in file:
        line = line.strip('\n').split(' ')
        lines.append(line)

level_evaluation = []

def check_level(report: list) -> int:
    '''This fucntion checks the report list and returns 1 if level is safe, or 0 if unsafe. Needs a report list.'''
    #Setting initial conditions and exiting if already found no change:
    skip = False
    level_steps = []
    initial_step = int(report[0])-int(report[1])
    if initial_step == 0:
        return 0
    level_steps.append(abs(initial_step))
    initial_direction = initial_step/abs(initial_step)
    for i in range(2, len(report)):
        step = int(report[i-1])-int(report[i])
        if step == 0:
            return 0
        direction = step/abs(step)
        if not direction == initial_direction:
            return 0
        level_steps.append(abs(step))
    if max(level_steps) < 4:
        return 1
    else: 
        return 0


def problem_damper(report: list ) -> int:
    '''Function simulates the damper machine discussed in the problem.'''
    for i in range(len(report)):
        new_report = report.copy()
        del new_report[i]
        result = check_level(new_report)
        if result == 1:
            return 1
    return 0

for level in lines:

    first_result = check_level(level)
    if first_result == 1:
        level_evaluation.append(1)
    else:
        level_evaluation.append(problem_damper(level))

    
        


print(sum(level_evaluation))