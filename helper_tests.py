import unittest
from classes import Literal, Clause
from pure_lit_elim import pure_literal_elim
from unit_elim import unit_clause_elim, eliminate_single_unit
from solver import solve

# TESTERS

l1 = Literal(1, True)
l1b = Literal(1, False)
l2 = Literal(2, True)
l2b = Literal(2, False)
l3 = Literal(3, True)
l3b = Literal(3, False)

assigned = set()
unassigned = {l1, l2, l3, l1b, l2b, l3b}

# Tests for Unit Elim

class UnitElimTests(unittest.TestCase):
    def test_title(self):
        c1 = Clause(1, {l1b}) # -x
        c2 = Clause(2, {l1, l2, l3})  # x y z
        c2b = Clause(3, {l2, l3}) # y z
        c3 = Clause(3, {l1b, l3b}) # -x -z
        i1 = {c1, c2, c3}

        self.assertTrue(unit_clause_elim(i1, assigned.copy(), unassigned.copy()) == c2b)