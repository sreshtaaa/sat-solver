import sys
from copy import copy, deepcopy
import random 
from typing import Callable, List, Set, Tuple

# Imports from our files
from classes import Literal, Clause
from solver import read_input, solve, print_output

################# VALIDITY CHECKING #################

# SAMPLE OUTPUT : 
# Testing test_files/literals_appear_once.cnf...
# s SATISFIABLE
# v 2 3 -8 5 -6 4 -1 -7 0
# Checking Assignment For Validity... True
    
# Consumes a variable assignment and a set of clauses and returns whether the assignment 
# satisfies the clauses
def check_validity_clauses(assignment : Set[Literal], clauses : Set[Clause]): 
    for clause in clauses: 
        if assignment.intersection(clause.literal_set) == set(): 
            return False
    
    return True

def test_with_file_input(filepath : str): # use "test_files/<test_name>.cnf"
    print(f"Testing {filepath}...")
    # input_file = sys.argv[1] # for running in command line
    input_file = filepath 
    assigned, unassigned, clause_set = read_input(input_file)
    assignment = solve(assigned, unassigned, clause_set)
    
    if assignment == None: 
        print("UNSAT")
    else: 
        print_output(assignment)
        print("Checking Assignment For Validity... " + str(check_validity_clauses(assignment, clause_set)))
    return 

def main(): 
    list_tests = ["all_units.cnf", "basic_tests.cnf", "conflicting_lits.cnf", "literals_appear_once.cnf", \
        "long_sat.cnf", "pure_lit_elim_all.cnf", "single_clause.cnf", "single_pure_literal.cnf", \
            "single_unit_clause_elim.cnf", "unit_cascade_sat.cnf", "unit_cascade_unsat.cnf"]
    
    for file in list_tests: 
        filepath = "test_files/" + file
        test_with_file_input(filepath)
        print("\n")

if __name__ == "__main__":
    main()


############ PRELIMINARY CODE FOR GENERATING INPUT ##############
# Note: Not completed, added as a potential extension for testing

# def generate_literals(num_lits : int):
#     lit_set = set()
#     for i in range(1, num_lits): 
#         lit_set.add(Literal(i, True))
#         lit_set.add(Literal(i, False))
    
#     return lit_set

# def generate_clauses(set_lits : Set[Literal]): 
#     set_clauses = set()

#     num_clauses = random.randrange(2, len(set_lits) + 4)
#     for i in range(1, num_clauses): 
#         clause_size = random.randrange(1, len(set_lits))
#         lits_in_clause = set()
#         for j in range(1, clause_size): 
#             lits_copy = set_lits.copy()
#             lits_in_clause.add(lits_copy.pop())
        
#         set_clauses.add(Clause(i, lits_in_clause))
    
#     return set_clauses