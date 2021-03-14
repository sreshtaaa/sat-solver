#!/bin/python3
import sys
from copy import copy, deepcopy
import random

# Feel free to change the provided types and parsing code to match
# your preferred representation of formulas, clauses, and literals.

class Literal:
    def __init__(self, name, sign):
        self.name = name  # integer
        self.sign = sign  # boolean

    def __repr__(self):
        return ("-" if not self.sign else "") + self.name

    def __eq__(self, other):
        if type(other) != Literal:
            return False
        return self.name == other.name and self.sign == other.sign

    def __hash__(self):
      return hash((self.name, self.sign))


class Clause:
    def __init__(self, id, literal_set):
        self.id = id
        self.literal_set = literal_set

    def __repr__(self):
        return f"{self.id}: {str(self.literal_set)}"

    def __eq__(self, other):
        if type(other) != Clause:
            return False
        return self.id == other.id

# CAN YOU SEE THIS

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