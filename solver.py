#!/bin/python3
import sys
from copy import copy, deepcopy
import random
from typing import Callable, List, Set, Tuple
from classes import Literal, Clause
from unit_elim import unit_clause_elimination, eliminate_single_unit
from general_functions import update_assignments, negate_literal, remove_clauses_with_literal
from pure_lit_elim import pure_literal_elim


def solve(assigned_lits : Set[Literal], unassigned_lits : Set[Literal], set_clauses : Set[Clause]):
    eliminated_unit_clauses = unit_clause_elimination(assigned_lits, unassigned_lits, set_clauses)
    cleaned_clauses = pure_literal_elim(eliminated_unit_clauses, assigned_lits, unassigned_lits)

    if cleaned_clauses == set():
        return assigned_lits
    elif set() in cleaned_clauses: 
        return # return None for print output
    else: 
        modified_assigned = assigned_lits.copy()
        modified_unassigned = unassigned_lits.copy()

        random_lit = modified_unassigned.pop()
        modified_unassigned.add(random_lit)

        update_assignments(modified_assigned, modified_unassigned, random_lit)
        modified_clauses = eliminate_single_unit(set_clauses.copy(), random_lit)

        result = solve(modified_assigned, modified_unassigned, modified_clauses)
        if result == None: 
            neg_modified_assigned = assigned_lits.copy()
            neg_modified_unassigned = unassigned_lits.copy()

            update_assignments(neg_modified_assigned, neg_modified_unassigned, negate_literal(random_lit))
            neg_modified_clauses = eliminate_single_unit(set_clauses.copy(), negate_literal(random_lit))

            neg_result = solve(modified_assigned, modified_unassigned, modified_clauses)
            
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
                literal_set = {}
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
        for var in assignment:
            result += " " + ("" if assignment[var] else "-") + str(var)

    print(f"s {'SATISFIABLE' if isSat else 'UNSATISFIABLE'}")
    if isSat:
        print(f"v{result} 0")

if __name__ == "__main__":
    inputFile = sys.argv[1]
    assigned, unassigned, clause_set = readInput(inputFile)

    # TODO: find a satisfying instance (or return unsat) and print it out
    printOutput({})