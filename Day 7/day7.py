'''
--- Day 7: Bridge Repair ---

The Historians take you to a familiar rope bridge over a river in the middle of a jungle. The Chief isn't on this side of the bridge, though; maybe he's on the other side?

When you go to cross the bridge, you notice a group of engineers trying to repair it. (Apparently, it breaks pretty frequently.) You won't be able to cross until it's fixed.

You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20

Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:

    190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
    3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators, two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
    292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.

The engineers just need the total calibration result, which is the sum of the test values from just the equations that could possibly be true. In the above example, the sum of the test values for the three equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?

Your puzzle answer was 7710205485870.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.

The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:

    156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
    7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
    192: 17 8 14 can be made true using 17 || 8 + 14.

Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?


'''
from itertools import product
from tqdm import tqdm
#------------- General constants and lists
OPERATION_LIST = ['mul', 'add', 'concat']
#------------- Functions and classes
def mul(num1:int, num2:int) -> int:
    return num1*num2

def add(num1:int, num2:int) -> int:
    return num1+num2

def concat(num1:int, num2:int) -> int:
    return int(str(num1)+str(num2))

def create_operation_lists(operator_number:int, possible_operations:list[str] = OPERATION_LIST) -> list[list[str]]:
    '''This function will generate a list of all possible combinations with x operation function calls. ,
    x is the operator_number.'''
    return list(product(possible_operations, repeat = operator_number))

def test_equation(equation:list[int,list[int]]) -> [bool, int]:
    '''This test all possible equations and checks how many are valid.'''
    result = equation[0]
    solutions = 0
    opperators_eq = equation[1]
    operation_number = len(opperators_eq) -1
    operation_possibilities = create_operation_lists(operation_number)
    for possibility in operation_possibilities:
        test_result = eval(possibility[0])(opperators_eq[0], opperators_eq[1])
        if operation_number > 1:
            for i in tqdm(range(operation_number-1)):
                test_result = eval(possibility[1+i])(test_result, opperators_eq[2+i])
        if test_result == result:
            solutions += 1
    if solutions > 0:
        return True, solutions
    return False, solutions




if __name__ == '__main__':

    #Read the data
    with open('Day 7\equations.txt', 'r') as raw_results:
        possible_equations = raw_results.readlines()
    possible_equations = [line.replace('\n','') for line in possible_equations]

    #Converting into usable lists:
    digested_equations = []
    for line in possible_equations:
        new_eq = []
        result_eq, opperators = line.split(':')
        new_eq.append(int(result_eq))
        opperators_discrete = opperators.split(' ')
        opperators_discrete = [int(num) for num in opperators_discrete[1:]]
        new_eq.append(opperators_discrete)
        digested_equations.append(new_eq)
    
    valid_index = []
    for index, equation in tqdm(enumerate(digested_equations)):
        evaluation_res, revaluation_quantity = test_equation(equation)
        if evaluation_res:
            valid_index.append(index)

    sum_valid_equations =0
    for true_equation_index in valid_index:
        sum_valid_equations += digested_equations[true_equation_index][0]

    print(sum_valid_equations)
