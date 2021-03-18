import sys
from copy import copy, deepcopy
import random 
from typing import Callable, List, Set, Tuple

# Imports from our files
from classes import Literal, Clause
from solver import read_input, solve, print_output

############ PRELIMINARY CODE FOR GENERATING INPUT ##############
# Note: Not completed, added as a potential extension for testing

def generate_literals(num_lits : int):
    lit_set = set()
    for i in range(1, num_lits): 
        lit_set.add(Literal(i, True))
        lit_set.add(Literal(i, False))
    
    return lit_set

def generate_clauses(set_lits : Set[Literal]): 
    set_clauses = set()

    num_clauses = random.randrange(2, len(set_lits) + 4)
    for i in range(1, num_clauses): 
        clause_size = random.randrange(1, len(set_lits))
        lits_in_clause = set()
        for j in range(1, clause_size): 
            lits_copy = set_lits.copy()
            lits_in_clause.add(lits_copy.pop())
        
        set_clauses.add(Clause(i, lits_in_clause))
    
    return set_clauses

################# VALIDITY CHECKING #################
    
# Consumes a variable assignment and a set of clauses and returns whether the assignment 
# satisfies the clauses
def check_validity_clauses(assignment : Set[Literal], clauses : Set[Clause]): 
    for clause in clauses: 
        if assignment.intersection(clause.literal_set) == set(): 
            return False
    
    return True

def main(): 
    input_file = sys.argv[1] # for running in command line
    # input_file = "test_files/long_sat.cnf" # for running manually, use "test_files/<test_name>.cnf"
    assigned, unassigned, clause_set = read_input(input_file)
    assignment = solve(assigned, unassigned, clause_set)
    
    if assignment == None: 
        print("UNSAT")
    else: 
        print_output(assignment)
        print("Checking Assignment For Validity... " + str(check_validity_clauses(assignment, clause_set)))
    return 

if __name__ == "__main__":
    main()
