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
    def __init__(self, id, literalSet):
        self.id = id
        self.literalSet = literalSet

    def __repr__(self):
        return f"{self.id}: {str(self.literalSet)}"

    def __eq__(self, other):
        if type(other) != Clause:
            return False
        return self.id == other.id




# Consumes a set of clauses not containing a literal and a literal, and removes the negated 
# literal from each clause in the set
def remove_negated_unit(set_clauses : Set[Clause], unit : Literal):
    negated_literal = negate_literal(unit)
    for clause in set_clauses: 
        clause.discard(negate_literal)
    
    return set_clauses

# Consumes a set of clauses and returns a set of unit literals
def find_all_units(set_clauses : Set[Clause]):
    set_of_units = set()
    for clause in set_clauses:
        if is_unit(clause):
            set_of_units.add(unit_value(clause))
    
    return set_of_units

# Returns the literal contained in a unit clause 
def unit_value(c : Clause): 
    clause_literal = c.literalSet.pop()
    c.literalSet.add(clause_literal)
    return clause_literal

# If the clause only contains 1 literal, then it is a unit
def is_unit(c : Clause): 
    return len(c.literalSet) == 1

# Returns the negated literal 
def negate_literal(l : Literal): 
    return Literal(l.name, not l.sign)