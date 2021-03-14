from typing import Callable, List, Set, Tuple
from classes import Literal, Clause

# Consumes a set of clauses and returns only the clauses without the literal l 
def remove_clauses_with_literal(set_clauses : Set[Clause], l : Literal): 
    clauses_without_literal = set()
    for clause in set_clauses: 
        if l in clause: 
            continue
        else: 
            clauses_without_literal.add(clause)
    
    return clauses_without_literal

# Adds literal to assigned variable set and removes literal from unassigned variable set
def update_assignments(assigned_lits : Set[Literal], unassigned_lits : Set[Literal], l : Literal): 
    if l in unassigned_lits:
        unassigned_lits.remove(l)
        assigned_lits.add(l)
        unassigned_lits.discard(negate_literal(l))
    return

# Consumes a set of clauses not containing a literal and a literal, and removes the negated 
# literal from each clause in the set
def remove_negated_unit(set_clauses : Set[Clause], unit : Literal):
    negated_literal = negate_literal(unit)
    for clause in set_clauses: 
        clause.discard(negated_literal)
    
    return set_clauses

# Returns the negated literal 
def negate_literal(l : Literal): 
    return Literal(l.name, not l.sign)