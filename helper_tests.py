import unittest
from typing import Callable, List, Set, Tuple

# Imports from our scripts
from classes import Literal, Clause
from pure_lit_elim import pure_literal_elim
from unit_elim import unit_clause_elim, eliminate_single_unit
from general_functions import negate_literal
from solver import solve

# TESTERS

l1 = Literal(1, True)
l1b = Literal(1, False)
l2 = Literal(2, True)
l2b = Literal(2, False)
l3 = Literal(3, True)
l3b = Literal(3, False)
l4 = Literal(4, True)
l4b = Literal(4, False)

assigned = set()
unassigned = {l1, l2, l3, l4, l1b, l2b, l3b, l4b}

###################################################
#         TESTS FOR unit_clause_elim              #
###################################################

def unit_not_in_clauses(unit : Literal, clauses : Set[Clause]): 
    for clause in clauses: 
        if (unit in clause.literal_set or negate_literal(unit) in clause.literal_set): 
            return False

    return True

class UnitElimTests(unittest.TestCase):
    def test_basic(self):
        c1 = Clause(1, {l1b}) # -x
        c2 = Clause(2, {l1, l2, l3})  # x y z
        c2b = Clause(2, {l2, l3}) # y z
        c3 = Clause(3, {l1b, l3b}) # -x -z
        inst = {c1, c2, c3}

        self.assertTrue(unit_clause_elim(inst, assigned.copy(), unassigned.copy()) == {c2b})

    def test_single_clause_elim(self):
        c1 = Clause(1, {l1b}) # -x
        inst = {c1}

        self.assertTrue(unit_clause_elim(inst, assigned.copy(), unassigned.copy()) == set())

    def test_contradicting_clause_elim(self): 
        c1 = Clause(1, {l1b}) # -x
        c2 = Clause(2, {l1}) # x
        c3 = Clause(3, {l3, l4, l1b}) # z w -x

        inst = {c1, c2, c3}
        elim_clauses = unit_clause_elim(inst, assigned.copy(), unassigned.copy())

        self.assertTrue(unit_not_in_clauses(l1b, elim_clauses) and unit_not_in_clauses(l1, elim_clauses))

    def test_no_units(self): 
        c1 = Clause(1, {l1, l1b}) # x -x
        c2 = Clause(2, {l2, l4}) # y w
        c3 = Clause(3, {l1, l2, l3, l4}) # x y z w
        c4 = Clause(4, {l3b, l2}) # -z w

        inst = {c1, c2, c3, c4}

        self.assertTrue(unit_clause_elim(inst, assigned.copy(), unassigned.copy()) == inst)
    
    def test_unit_cascade(self): 
        c1 = Clause(1, {l3}) # x -x
        c2 = Clause(2, {l3b, l4}) # y w
        c3 = Clause(3, {l1, l2, l3b, l4}) # x y z w
        c4 = Clause(4, {l3b, l2}) # -z w

        inst = {c1, c2, c3, c4}
        elim_clauses = unit_clause_elim(inst, assigned.copy(), unassigned.copy())

        self.assertTrue(elim_clauses == set())

if __name__ == '__main__':
    unittest.main()