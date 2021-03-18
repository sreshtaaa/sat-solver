from classes import Literal, Clause
from general_functions import update_assignments, remove_clauses_with_literal, negate_literal
from typing import Callable, List, Set, Tuple

# Eliminates pure literals until there are no remaining pure literals in the set of clauses
def pure_literal_elim(inst : Set[Clause], assigned : Set[Literal], unassigned : Set[Literal]):
    elim = find_pure(inst, unassigned)
    if elim == None:
        return inst
    else:
        update_assignments(assigned, unassigned, elim)
        new_inst = remove_clauses_with_literal(inst, elim)
        return pure_literal_elim(new_inst, assigned, unassigned)

############# HELPER FUNCTIONS FOR pure_literal_elim #############

# Consumes a set of clauses and a set of literals and returns the first pure literal found 
# (or returns None)
def find_pure(inst : Set[Clause], lits : Set[Literal]):
    for l in lits:
        pure = True
        for c in inst:
            pure = (negate_literal(l) not in c.literal_set) and pure
        if not pure:
            continue
        else:
            return l
            break