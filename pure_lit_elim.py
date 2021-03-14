from classes import Literal, Clause
from general import update_assignments, remove_clauses_with_literal, negate_literal
from typing import Callable, List, Set, Tuple

def find_pure(inst : Set[Clause], lits : Set[Literal]):
    for l in lits:
        pure = True
        for c in inst:
            (negate_literal(l) not in c) and pure
        if not pure:
            continue
        else:
            return l
            break

def pure_literal_elim(inst : Set[Clause], assigned : Set[Literal], unassigned : Set[Literal]):
    elim = find_pure(inst, unassigned)
    if elim == None:
        return inst
    else:
        update_assignments(assigned, unassigned, elim)
        new_inst = remove_clauses_with_literal(inst, elim)
        return pure_literal_elim(new_inst, assigned, unassigned)