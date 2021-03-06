from typing import Callable, List, Set, Tuple
from general_functions import remove_clauses_with_literal, update_assignments, \
    remove_negated_unit, negate_literal
from classes import Literal, Clause

# Consumes a set of clauses and continues to eliminate units (and assign units to solution)
# until there are no units left
def unit_clause_elim(set_clauses : Set[Clause], assigned : Set[Literal], unassigned : Set[Literal]):
    unit_set = find_all_units(set_clauses, assigned, unassigned)
    removed_clauses = set_clauses
    for unit in unit_set: 
        removed_clauses = eliminate_single_unit(removed_clauses, unit)
    
    all_units = find_all_units(removed_clauses, assigned, unassigned)
    if all_units == set(): 
        return removed_clauses
    else: 
        return unit_clause_elim(removed_clauses, assigned, unassigned)

############# HELPER FUNCTIONS FOR unit_clause_elim #############

# Consumes a set of clauses and returns a set of unit literals
def find_all_units(set_clauses : Set[Clause], assigned : Set[Literal], unassigned : Set[Literal]):
    set_of_units = set()
    for clause in set_clauses:
        if is_unit(clause):
            val = unit_value(clause)
            set_of_units.add(val)
            update_assignments(assigned, unassigned, val)
 
    return set_of_units

# Consumes a set of clauses, elimintes all clauses with the unit, and 
# removes unit's negation from remaining clauses
def eliminate_single_unit(set_clauses : Set[Clause], unit : Literal): 
    removed_clauses = remove_clauses_with_literal(set_clauses, unit)
    return remove_negated_unit(removed_clauses, unit)

# Returns the literal contained in a unit clause 
def unit_value(c : Clause): 
    clause_literal = c.literal_set.pop()
    c.literal_set.add(clause_literal)
    return clause_literal

# If the clause only contains 1 literal, then it is a unit
def is_unit(c : Clause): 
    return len(c.literal_set) == 1