from solver import Literal, Clause

def commitAssigned(assigned_lits : Set[Literal], unassigned_lits : Set[Literal], lit : Literal):
    assigned_lits.add(lit)
    unassigned_lits.remove(lit)
    unassigned_lits.discard(negate_literal(lit))

