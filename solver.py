#!/bin/python3
import sys
from copy import copy, deepcopy
import random
from typing import Callable, List, Set, Tuple
from classes import Literal, Clause
from unit_elim import unit_clause_elim, eliminate_single_unit
from general_functions import update_assignments, negate_literal, remove_clauses_with_literal
from pure_lit_elim import pure_literal_elim

def solve(assigned_lits : Set[Literal], unassigned_lits : Set[Literal], set_clauses : Set[Clause]):
    eliminated_unit_clauses = unit_clause_elim(set_clauses, assigned_lits, unassigned_lits)
    cleaned_clauses = pure_literal_elim(eliminated_unit_clauses, assigned_lits, unassigned_lits)

    if cleaned_clauses == set():
        return assigned_lits
    elif set() in cleaned_clauses: 
        return # return None for print output
    else: 
        mod_assigned = assigned_lits.copy()
        mod_unassigned = unassigned_lits.copy()

        random_lit = mod_unassigned.pop()
        mod_unassigned.add(random_lit)

        update_assignments(mod_assigned, mod_unassigned, random_lit)
        mod_clauses = eliminate_single_unit(set_clauses.copy(), random_lit)

        result = solve(mod_assigned, mod_unassigned, mod_clauses)
        if result == None: 
            neg_mod_assigned = assigned_lits.copy()
            neg_mod_unassigned = unassigned_lits.copy()

            update_assignments(neg_mod_assigned, neg_mod_unassigned, negate_literal(random_lit))
            neg_mod_clauses = eliminate_single_unit(set_clauses.copy(), negate_literal(random_lit))

            neg_result = solve(mod_assigned, mod_unassigned, mod_clauses)
            
            return neg_result
        else: 
            return result

# Read and parse a cnf file, returning the variable set and clause set
def readInput(cnfFile):
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
def printOutput(assignment):
    result = ""
    isSat = (assignment is not None)
    if isSat:
        for lit in assignment:
            result += " " + repr(lit)
            # result += " " + ("" if assignment[var] else "-") + str(var)

    print(f"s {'SATISFIABLE' if isSat else 'UNSATISFIABLE'}")
    if isSat:
        print(f"v{result} 0")

def main(): 
    inputFile = sys.argv[1]
    assigned, unassigned, clause_set = readInput(inputFile)
    assignment = solve(assigned, unassigned, clause_set)
    # TODO: find a satisfying instance (or return unsat) and print it out
    printOutput(assignment)
    return 

if __name__ == "__main__":
    main()