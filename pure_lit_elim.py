from classes import Literal, Clause
from general_functions import update_assignments, remove_clauses_with_literal, negate_literal
from typing import Callable, List, Set, Tuple

def find_pure(inst : Set[Clause], lits : Set[Literal]):
    remove = set()
    for l in lits:
        exists = False
        for c in inst:
            exists = exists or l in c.literal_set
        if not exists:
            remove.add(l)
            continue
        else:
            pure = True
            for c in inst:
                # DO: must check there is atleast one 
                pure = (negate_literal(l) not in c.literal_set) and pure
            if not pure:
                continue
            else:
                return l
                break
    lits.difference_update(remove)

def pure_literal_elim(inst : Set[Clause], assigned : Set[Literal], unassigned : Set[Literal]):
    elim = find_pure(inst, unassigned)
    if elim == None:
        return inst
    else:
        update_assignments(assigned, unassigned, elim)
        new_inst = remove_clauses_with_literal(inst, elim)
        return pure_literal_elim(new_inst, assigned, unassigned)

# l1 = Literal(1, False)
# l2 = Literal(1, True)
# l3 = Literal(2, False)
# l4 = Literal(2, True)
# l5 = Literal(3, False)
# l6 = Literal(3, True)
# l7 = Literal(4, False)
# l8 = Literal(4, True)

# c1 = Clause(1, {l1, l3})
# c2 = Clause(2, {l2, l4})
# c3 = Clause(3, {l5, l7})
# c4 = Clause(4, {l8})

# exI = {c1, c2, c3, c4}

# assgnd = set()
# unassgnd = {l1, l2, l3, l4, l5, l7, l8}

# print(find_pure(exI, unassgnd))
# print(pure_literal_elim(exI, assgnd, unassgnd), assgnd)
