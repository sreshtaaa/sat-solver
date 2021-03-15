from classes import Literal, Clause
import general_functions
import unit_elim
import pure_lit_elim
import solver

l1 = Literal(1, True)
l1b = Literal(1, False)
l2 = Literal(2, True)
l2b = Literal(2, False)
l3 = Literal(3, True)
l3b = Literal(3, False)

# c1 = list-to-list-set([list: l1b])
# c2 = list-to-list-set([list: l1, l2, l3])
# c2b = list-to-list-set([list: l2, l3])
# c3 = list-to-list-set([list: l1b, l3b])

# inst = list-to-list-set([list: c1, c2, c3])

c1 = Clause(1, {l1b})
c2 = Clause(2, {l1, l2, l3})
c2b = Clause(3, {l2, l3})
c3 = Clause(3, {l1b, l3b})

inst = {c1, c2, c3}

unassigned = {l1, l1b, l2, l3, l3b}
assigned = set()

print(solver.solve(assigned, unassigned, inst))

#left = unit_elim.unit_clause_elim(inst, assigned, unassigned)
#print(left, assigned)
#print(pure_lit_elim.pure_literal_elim(left, assigned, unassigned), assigned)