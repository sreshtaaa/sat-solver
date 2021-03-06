#!/bin/python3
import sys
from copy import copy, deepcopy
import random
from typing import Callable, List, Set, Tuple

# Imports from our scripts
from classes import Literal, Clause
from unit_elim import unit_clause_elim, eliminate_single_unit
from general_functions import update_assignments, negate_literal, remove_clauses_with_literal
from pure_lit_elim import pure_literal_elim

def solve(assigned_lits : Set[Literal], unassigned_lits : Set[Literal], set_clauses : Set[Clause]):\
    # Optimizations
    eliminated_unit_clauses = unit_clause_elim(set_clauses, assigned_lits, unassigned_lits)
    cleaned_clauses = pure_literal_elim(eliminated_unit_clauses, assigned_lits, unassigned_lits)

    # Check conditions for SAT and UNSAT
    if cleaned_clauses == set():
        return assigned_lits
    else: 
        for clause in cleaned_clauses: 
            if clause.literal_set == set(): 
                return 
            else: 
                continue
        
        # Ch0ose random literal and try and find a solution
        mod_assigned = deepcopy(assigned_lits)
        mod_unassigned = deepcopy(unassigned_lits)

        random_lit = mod_unassigned.pop()
        mod_unassigned.add(random_lit)

        update_assignments(mod_assigned, mod_unassigned, random_lit)
        mod_clauses = eliminate_single_unit(deepcopy(cleaned_clauses), random_lit)

        result = solve(mod_assigned, mod_unassigned, mod_clauses)

        # If UNSAT, choose negated literal and try again
        if result == None: 
            neg_mod_assigned = deepcopy(assigned_lits)
            neg_mod_unassigned = deepcopy(unassigned_lits)

            update_assignments(neg_mod_assigned, neg_mod_unassigned, negate_literal(random_lit))
            neg_mod_clauses = eliminate_single_unit(deepcopy(cleaned_clauses), negate_literal(random_lit))

            neg_result = solve(neg_mod_assigned, neg_mod_unassigned, neg_mod_clauses)
            
            return neg_result
        else: 
            return result

# Read and parse a cnf file, returning the variable set and clause set
def read_input(cnfFile):
    unassigned_set = set()
    assigned_set = set()
    clause_set = set()
    next_CID = 0
    with open(cnfFile, "r") as f:
        for line in f.readlines():
            tokens = line.strip().split()
            if tokens and tokens[0] != "p" and tokens[0] != "c":
                literal_set = set()
                for lit in tokens[:-1]:
                    sign = lit[0] != "-"
                    variable = lit.strip("-")
                    constructed_lit = Literal(variable, sign)

                    literal_set.add(constructed_lit)
                    unassigned_set.add(constructed_lit)

                clause_set.add(Clause(next_CID, literal_set))
                next_CID += 1
    
    return assigned_set, unassigned_set, clause_set


# Print the result in DIMACS format
def print_output(assignment):
    result = ""
    is_sat = (assignment is not None)
    if is_sat:
        for lit in assignment:
            result += " " + repr(lit)

    print(f"s {'SATISFIABLE' if is_sat else 'UNSATISFIABLE'}")
    if is_sat:
        print(f"v{result} 0")

def main(): 
    # Read in file, assign initial clause sets and variable sets
    input_file = sys.argv[1]
    assigned, unassigned, clause_set = read_input(input_file)

    # Solve and print solution
    assignment = solve(assigned, unassigned, clause_set)
    print_output(assignment)
    return 

if __name__ == "__main__":
    main()