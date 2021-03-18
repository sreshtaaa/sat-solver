import unittest
from typing import Callable, List, Set, Tuple

# Imports from our scripts
from classes import Literal, Clause
from pure_lit_elim import pure_literal_elim
from unit_elim import unit_clause_elim, eliminate_single_unit
from general_functions import negate_literal
from solver import solve
from testing_script import check_validity_clauses

############### TESTING VARIABLES ################

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

def contains_empty_clause(clauses : Set[Clause]): 
    for clause in clauses: 
        if clause.literal_set == set(): 
            return True
    
    return False

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

        self.assertTrue(unit_not_in_clauses(l1b, elim_clauses) and unit_not_in_clauses(l1, elim_clauses) \
            and contains_empty_clause(elim_clauses))

    def test_no_units(self): 
        c1 = Clause(1, {l1, l1b}) # x -x
        c2 = Clause(2, {l2, l4}) # y w
        c3 = Clause(3, {l1, l2, l3, l4}) # x y z w
        c4 = Clause(4, {l3b, l2}) # -z w

        inst = {c1, c2, c3, c4}

        self.assertTrue(unit_clause_elim(inst, assigned.copy(), unassigned.copy()) == inst)
    
    def test_unit_cascade(self): 
        c1 = Clause(1, {l3}) # z
        c2 = Clause(2, {l3b, l4}) # -z w
        c3 = Clause(3, {l1, l2, l3b, l4}) # x y -z w
        c4 = Clause(4, {l3b, l2}) # -z y

        inst = {c1, c2, c3, c4}
        elim_clauses = unit_clause_elim(inst, assigned.copy(), unassigned.copy())

        self.assertTrue(elim_clauses == set())

    def test_remove_negation(self): 
        c1 = Clause(1, {l3}) # x -x
        c2 = Clause(2, {l3b, l4, l2b}) # -z w -y
        c3 = Clause(3, {l1, l2, l3b, l4}) # x y -z w

        inst = {c1, c2, c3}
        elim_clauses = unit_clause_elim(inst, assigned.copy(), unassigned.copy())

        self.assertTrue(unit_not_in_clauses(l3, elim_clauses) and unit_not_in_clauses(l3b, elim_clauses))  

    def test_all_different_units(self): 
        c1 = Clause(1, {l1}) # x
        c2 = Clause(2, {l2}) # y
        c3 = Clause(3, {l3}) # z
        c4 = Clause(4, {l4}) # w

        inst = {c1, c2, c3, c4}

        self.assertTrue(unit_clause_elim(inst, assigned.copy(), unassigned.copy()) == set())

    def test_contains_opposing_units(self): 
        c1 = Clause(1, {l1}) # x
        c2 = Clause(2, {l1b}) # -x
        c3 = Clause(3, {l3}) # z
        c4 = Clause(4, {l4}) # w

        inst = {c1, c2, c3, c4}
        elim_clauses = unit_clause_elim(inst, assigned.copy(), unassigned.copy())

        self.assertTrue(contains_empty_clause(elim_clauses) and len(elim_clauses) == 1)


###################################################
#            TESTS FOR pure_lit_elim              #
###################################################

class PureLitElimTests(unittest.TestCase):
    def test_basic(self):
        c1 = Clause(1, {l1, l2, l3}) # x y z
        c2 = Clause(2, {l1, l2b})  # x -y
        c3 = Clause(3, {l2, l3}) # y z
        c4 = Clause(4, {l2b, l3b}) # -y -z

        inst = {c1, c2, c3, c4}
        unassigned2 = {l1, l2, l3, l2b, l3b}

        elim_clauses = pure_literal_elim(inst, assigned.copy(), unassigned2)

        self.assertTrue(elim_clauses == {c3, c4})

    def test_recursive_elim(self):
        c1 = Clause(1, {l1, l2, l3}) # x y z
        c2 = Clause(2, {l1, l2b})  # x -y
        c3 = Clause(3, {l2, l3}) # y z
        c4 = Clause(4, {l3, l3b}) # -z z

        inst = {c1, c2, c3, c4}
        unassigned2 = {l1, l2, l3, l2b, l3b}

        elim_clauses = pure_literal_elim(inst, assigned.copy(), unassigned2)
        
        self.assertTrue(elim_clauses == {c4})

    def test_no_pure_literals(self):
        c1 = Clause(1, {l1, l2, l3}) # x y z
        c2 = Clause(2, {l1b, l2b, l3b})  # -x -y -z

        inst = {c1, c2}
        unassigned2 = {l1, l2, l3, l2b, l3b, l1b}

        elim_clauses = pure_literal_elim(inst, assigned.copy(), unassigned2)

        self.assertTrue(elim_clauses == {c1, c2})
    
    def test_all_pure(self):
        c1 = Clause(1, {l1, l3}) # x z
        c2 = Clause(2, {l2b, l3})  # -y z
        c3 = Clause(3, {l2b, l1}) # -y x

        inst = {c1, c2, c3}
        unassigned2 = {l1, l2b, l3}

        elim_clauses = pure_literal_elim(inst, assigned.copy(), unassigned2)

        self.assertTrue(elim_clauses == set())
    
    def test_empty_clause(self):
        c1 = Clause(1, set())
        c2 = Clause(2, {l1, l2, l3}) # x y z
        c3 = Clause(3, {l1b, l2b, l3b})  # -x -y -z

        inst = {c1, c2, c3}
        unassigned2 = {l1, l2, l3, l1b, l2b, l3b}

        elim_clauses = pure_literal_elim(inst, assigned.copy(), unassigned2)

        self.assertTrue(elim_clauses == inst.copy())

    def test_assigns_leftovers(self):
        c2 = Clause(2, {l2}) # x y z
        c3 = Clause(3, {l2b, l3b})  # -x -y -z
        
        inst = {c2, c3}
        unassigned2 = {l1, l2, l2b, l3, l3b}
        assigned2 = assigned.copy()

        elim_clauses = pure_literal_elim(inst, assigned2, unassigned2)

        self.assertTrue(l1 in assigned2 and l3 not in assigned2)

class SolverEdgeCases(unittest.TestCase):
    def test_no_clauses(self): # returns subset of unassigned
        sol = solve(assigned.copy(), unassigned.copy(), set())
        self.assertTrue(sol != None and sol.issubset(unassigned))
    
    def test_no_clauses_no_literals(self): # returns sat, empty set
        sol = solve(assigned.copy(), set(), set())
        self.assertTrue(sol == set())
    
    def test_has_empty_clause_from_start(self):
        c1 = Clause(1, {l1, l2b})
        c2 = Clause(2, {l3, l3b})
        c3 = Clause(3, set())

        inst = {c1, c2, c3}
        unassigned2 = {l1, l2b, l3, l3b}

        sol = solve(assigned.copy(), unassigned2, inst)
        self.assertTrue(sol == None)
    
    def test_unsat(self):
        c1 = Clause(1, {l1, l2b})
        c2 = Clause(2, {l3, l3b})
        c3 = Clause(3, {l1b})
        c4 = Clause(4, {l2})

        inst = {c1, c2, c3, c4}
        unassigned2 = {l1, l2b, l3, l3b, l2, l2b}

        sol = solve(assigned.copy(), unassigned2, inst)
        self.assertTrue(sol == None)
    
    def test_sat(self):
        c1 = Clause(1, {l1b, l1, l2b})
        c2 = Clause(3, {l1b, l2})
        c3 = Clause(2, {l1, l2})

        inst = {c1, c2, c3}
        unassigned2 = {l1b, l1, l2b, l2}
        sol = solve(assigned.copy(), unassigned2, inst)

        self.assertTrue(check_validity_clauses(sol, inst))

if __name__ == '__main__':
    unittest.main()