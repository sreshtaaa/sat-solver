# CSCI 1710: SAT Solver

## Design Overview

We implemented a Satisfiability Solver in Python that operates on CNF (conjunctive normal form) files. Our implementation takes in a set of clauses where variables within a clause are separated by `OR` operators, and distinct clauses are separated by `AND`
operators. After performing a series of simplifying steps, the solver either returns a set of variable assignments or `UNSAT` if there exists no assignment that can satisfy the clauses. 

## Algorithm Overview

Our algorithm can loosely be separated into three stages: *unit clause elimination*, *pure literal elimination*, and *random assignment*. Unit clause elimination and pure literal elimination make up the "preprocessing" stage that significantly reduces the complexity of the recursion, while random assignment is part of the recursive stage.

### Unit Clause Elimination 

Consider the following set of clauses with variables `x`, `y`, and `z`. 

```
-x
x y z
-x -z
```

Here, the first clause is considered to be a unit clause with unit `-x`, since the lone variable in the clause means that the final set of variable assignments must have `x = false` in order to satisfy the `AND` operator between clauses. Knowing this, we can perform the following two simplifications, which is exactly the process of unit clause elimination for any given unit: 
* Remove all clauses with `-x` (since these will automatically be true in our assignment)
* Remove `x` (the negation of our unit) from all of its clauses, since `x` cannot equal `true` in our final assignment

This is unit clause elimination. After performing this operation, we are left with the following simplified clause: 
```
y z
```
We can now easily come up with a variable assignment that satisfies this clause. 

### Pure Literal Elimination 

Once again, consider the following set of clauses for variables `w`, `x`, `y`, and `z`. 

```
y -z
-x z
-x -w
-x -y z 
```

Notice that `x` always appears in its negated form (`-x`) in each clause containing the variable. This means that all of these clauses can easily be satisfied by setting `x = false`. Thus, we can remove every clause containing our pure literal. This is pure literal elimination. The resulting set of clauses becomes: 

```
y -z
```

As is seen, this is a far simpler set to satisfy. 

### Random Assignment

After performing unit clause elimination and pure literal elimination, the next step is to choose a variable at random and assign a value to it (either true or false). Then, the whole algorithm is repeated, including simplifying the clauses and assigning another random variable, if necessary. This is recursively continued until one of two terminating conditions: 
1. **Empty set of clauses:** This means that we have an empty `AND` condition, which is vacuously true. Hence, we return the variable assignment. 
2. **Empty clause:** This emans we have an empty `OR` condition, which is vacuously false. In this case, we recursively trace back, choosing the opposite variable assignment at each step and seeing if we reach the first terminating condition. If so, we return the variable assignment. If we continue to reach the empty clause condition for each recursive branch regardless of the variable assignment, then we know that our clause set is unsatisfiable, so we return `UNSAT`. 