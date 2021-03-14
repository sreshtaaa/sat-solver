from solver import Literal, Clause

# Returns the negated literal 
def negate_literal(l : Literal): 
    return Literal(l.name, not l.sign)

# Adds literal to assigned, removes self and negated from unassigned
def commitAssigned(assigned_lits : Set[Literal], unassigned_lits : Set[Literal], lit : Literal):
    assigned_lits.add(lit)
    unassigned_lits.remove(lit)
    unassigned_lits.discard(negate_literal(lit))

# Consumes a set of clauses and returns only the clauses without the literal l 
def remove_clauses_with_literal(set_clauses : Set[Clause], l : Literal): 
    clauses_without_literal = set()
    for clause in set_clauses: 
        if l in clause: 
            continue
        else: 
            clauses_without_literal.add(clause)
    
    return clauses_without_literal