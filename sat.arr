provide *
provide-types *

import pick as P
import either as EI

data Variable: 
  | v(value :: Number)
end

data Literal: 
  | literal(lit-var :: Variable, lit-sign :: Boolean)
end

type Clause = Set<Literal>
type SATInstance = Set<Clause>
type Assigned = Set<Literal>


fun solve(var-assign :: Set<Literal>, sat-inst :: SATInstance) -> Option<Set<Literal>>: 
  doc: "Returns whether the instance is satisfiable or not with the current set of variables"
  cleaned-inst = pure-elim(unit-clause-elimination(sat-inst), empty-list-set).{0}
  ask: 
    | cleaned-inst == empty-list-set then: some(var-assign)
    | cleaned-inst.member(empty-list-set) then: none
    | otherwise: 
      remaining-literals = find-all-literals(cleaned-inst)
      random-literal = 
        cases (P.Pick) remaining-literals.pick(): 
          | pick-none => inst
          | pick-some(lit, rest) => 
            new-clauses = eliminate-unit(inst, unit)
            eliminate-multiple-units(rest, new-clauses)
        end
  end
end

fun unit-clause-elimination(sat-inst :: SATInstance) -> Set<Clause>: 
  fun eliminate-multiple-units(units :: Set<Literal>, inst :: SATInstance) -> Set<Clause>: 
    doc: "Performs unit clause elimination on a SAT instance"
    cases (P.Pick) units.pick(): 
      | pick-none => inst
      | pick-some(unit, rest) => 
        new-clauses = eliminate-unit(inst, unit)
        eliminate-multiple-units(rest, new-clauses)
    end
  end
  
  all-units = find-all-units(sat-inst)
  removed-units-from-inst = eliminate-multiple-units(all-units, sat-inst)
  if all-units == empty-list-set: 
    removed-units-from-inst
  else: 
    unit-clause-elimination(removed-units-from-inst)
  end
end

fun pure-elim(inst :: SATInstance, a :: Assigned) -> {Set<Clause>; Assigned}:
  doc: "Eliminates pure literals"
  # all-literals
  all = find-all-literals(inst)
  
  # find pure-literal
  pure = 
    lists.fold-while({(b :: Option<Literal>, l :: Literal):
        if is-pure(inst, l):
          EI.right(some(l))
        else:
          EI.left(none)
        end
      }, none, all)
  
  # remove-pure and recurse
  cases (Option<Literal>) pure:
    | none => {inst; a}
    | some(l) => 
      pure-elim(remove-single-literal(inst, l), a.add(l))
  end
end


# HELPER FUNCTIONS FOR solve -------------------------------------------------------------------

fun find-all-literals(inst :: SATInstance) -> Set<Literal>: 
  doc: "Finds all the literals in an instance"
  inst.fold({(b :: Set<Literal>, c :: Clause): b.union(c)}, [set: ]).to-list()
end

# HELPER FUNCTIONS FOR pure-elim ---------------------------------------------------------------

fun is-pure(inst :: SATInstance, l :: Literal) -> Boolean:
  doc: "Returns true if opposite of l not in any clauses"
  not(inst.fold({(b :: Boolean, c :: Clause):
        b or c.member(literal(l.lit-var, not(l.lit-sign)))}, false))
end

# HELPER FUNCTIONS FOR unit-clause-elimination -------------------------------------------------

fun eliminate-unit(clauses :: Set<Clause>, unit :: Literal) -> Set<Clause>: 
  doc: "Consumes a set of clauses and a unit and returns a set of clauses with the unit eliminated"
  clauses-without-unit = remove-single-literal(clauses, unit)
  remove-negated-literal(clauses-without-unit, unit)
end

# ----------------------------------------------------------------------------------------------

fun find-all-units(sat-inst :: SATInstance) -> Set<Clause>: 
  doc: "Takes in a SAT Instance and returns all the unit clauses"
  sat-inst.fold(lam(base, c): if is-unit(c):base.add(unit-value(c)) else: base end end, 
    empty-list-set)
end

# Helper function for find-all-units
fun is-unit(c :: Clause) -> Boolean: 
  doc: "Returns whether a clause contains a single literal"
  c.size() == 1
end

fun unit-value(c :: Clause) -> Literal: 
  doc: "Consumes a clause with a single literal and returns the literal"
  cases (P.Pick) c.pick(): 
    | pick-none => raise("This shouldn't happen")
    | pick-some(unit, rest) => unit
  end
end

# ----------------------------------------------------------------------------------------------

fun remove-single-literal(clauses :: Set<Clause>, l :: Literal) -> Set<Clause>: 
  doc: "Consumes a SAT Instance and a unit and returns a set of clauses without that unit"
  clauses.fold({(base, c): if not(c.member(l)): base.add(c) else: base end},
    empty-list-set)
end

# -----------------------------------------------------------------------------------------------

fun remove-negated-literal(clauses :: Set<Clause>, l :: Literal) -> Set<Clause>: 
  doc: ```Consumes a set of clauses not containing a literal and a literal, and removes the negated 
       literal from each clause in the set```
  negated = negate-literal(l)
  clauses.fold({(base, c): base.add(c.remove(negated))}, empty-list-set)
end

# Helper function for remove-negated-literal
fun negate-literal(l :: Literal) -> Literal: 
  doc: "Returns the negated version of the literal"
  literal(l.lit-var, not(l.lit-sign))
end

# -----------------------------------------------------------------------------------------------
