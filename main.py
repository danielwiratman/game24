import random
import itertools
import operator
from typing import Any

def generate_numbers():
    return [random.randint(1, 9) for _ in range(4)]

def print_numbers_in_ascii(numbers: list[int]):
    ascii_art = {
        '0': ["  ___  ", " / _ \\ ", "| | | |", "| | | |", "| |_| |", " \\___/ "],
        '1': [" __ ", "/_ |", " | |", " | |", " | |", " |_|"],
        '2': [" ___  ", "|__ \\ ", "   ) |", "  / / ", " / /_ ", "|____|"],
        '3': [" ____  ", "|___ \\ ", "  __) |", " |__ < ", " ___) |", "|____/ "],
        '4': [" _  _   ", "| || |  ", "| || |_ ", "|__   _|", "   | |  ", "   |_|  "],
        '5': [" _____ ", "| ____|", "| |__  ", "|___ \\ ", " ___) |", "|____/ "],
        '6': ["   __  ", "  / /  ", " / /_  ", "| '_ \\ ", "| (_) |", " \\___/ "],
        '7': [" ______ ", "|____  |", "    / / ", "   / /  ", "  / /   ", " /_/    "],
        '8': ["  ___  ", " / _ \\ ", "| (_) |", " > _ < ", "| (_) |", " \\___/ "],
        '9': ["  ___  ", " / _ \\ ", "| (_) |", " \\__, |", "   / / ", "  /_/  "]
    }
    lines = [""] * 6
    for number in numbers:
        for i in range(6):
            lines[i] += ascii_art[str(number)][i] + "  "
    for line in lines:
        print(line)

def evaluate_expression(
    nums: tuple[int, ...],
    ops: list[Any], 
    op_symbols: dict[Any, str], 
    possible_answers: list[str]
):
    try:
        # Check the first possible expression: ((a op1 b) op2 c) op3 d
        if ops[2](ops[1](ops[0](nums[0], nums[1]), nums[2]), nums[3]) == 24:
            expression = f"(({nums[0]} {op_symbols[ops[0]]} {nums[1]}) {op_symbols[ops[1]]} {nums[2]}) {op_symbols[ops[2]]} {nums[3]}"
            possible_answers.append(expression)

        # Check the second possible expression: (a op1 b) op2 (c op3 d)
        if ops[1](ops[0](nums[0], nums[1]), ops[2](nums[2], nums[3])) == 24:
            expression = f"({nums[0]} {op_symbols[ops[0]]} {nums[1]}) {op_symbols[ops[1]]} ({nums[2]} {op_symbols[ops[2]]} {nums[3]})"
            possible_answers.append(expression)

        # Check the third possible expression: a op1 (b op2 (c op3 d))
        if ops[0](nums[0], ops[1](nums[1], ops[2](nums[2], nums[3]))) == 24:
            expression = f"{nums[0]} {op_symbols[ops[0]]} ({nums[1]} {op_symbols[ops[1]]} ({nums[2]} {op_symbols[ops[2]]} {nums[3]}))"
            possible_answers.append(expression)
    except ZeroDivisionError:
        # Skip any operations that result in division by zero
        pass

def find_possible_answers(numbers: list[int]):
    # Define the operations and their corresponding symbols
    operations = [operator.add, operator.sub, operator.mul, operator.truediv]
    op_symbols = {operator.add: '+', operator.sub: '-', operator.mul: '*', operator.truediv: '/'}

    possible_answers: list[str] = []

    # Iterate over all permutations of the input numbers
    for nums in itertools.permutations(numbers):
        # Iterate over all combinations of three operations
        for op1 in operations:
            for op2 in operations:
                for op3 in operations:
                    evaluate_expression(nums, [op1, op2, op3], op_symbols, possible_answers)

    return possible_answers

numbers: list[int] = []
numbers = generate_numbers()
answers = find_possible_answers(numbers)
while len(answers) == 0:
    numbers = generate_numbers()
    answers = find_possible_answers(numbers)

print("Your numbers are:")
print_numbers_in_ascii(numbers)
print()
print(f"Found {len(answers)} possible answers.")
_ = input("Press Enter to see possible answers...")

if answers:
     print("Possible answers:")
     for i in range(0, len(answers), 2):
         if i + 1 < len(answers):
             print(f"{answers[i]:<20} {answers[i+1]}")
         else:
             print(f"{answers[i]}")
else:
    print("No possible answers found.")

