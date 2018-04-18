# solverApprox

import argparse
from Numberjack import *

"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(num_wizards, num_constraints, wizards, constraints):
    """
    Write your algorithm here.
    Input:
        num_wizards: Number of wizards
        num_constraints: Number of constraints
        wizards: An array of wizard names, in no particular order
        constraints: A 2D-array of constraints, 
                     where constraints[0] may take the form ['A', 'B', 'C']

    Output:
        An array of wizard names in the ordering your algorithm returns
    """
    """
    Testing the basic functionality of the solver:
    v1 = Variable(1,5)
    v2 = Variable(1,5)
    v3 = Variable(1,5)
    v4 = Variable(1,5)
    v5 = Variable(1,5)
    model = Model([
        (v2 <= v1 & v2 <= v5) | (v2 >= v1 & v2 >= v5),
        (v3 <= v4 & v3 <= v5) | (v3 >= v4 & v3 >= v5),
        (v5 <= v3 & v5 <= v4) | (v5 >= v3 & v5 >= v4),
        (v4 <= v1 & v4 <= v2) | (v4 >= v1 & v4 >= v2),
        AllDiff((v1,v2,v3,v4,v5))
        ])
    solver = model.load("Mistral")
    solver.solve()
    print(v1,v2,v3,v4,v5)"""

    # create the variables that represent the wizards
    vs = [Variable(1, num_wizards) for i in range(num_wizards)]
    # match wizards to variables
    wiz_to_var = {}
    for i in range(num_wizards):
        wiz_to_var[wizards[i]] = vs[i] 
    # initiate a model
    model = Model([
         ])
    # add constraints
    for c in constraints:
        t0 = wiz_to_var[c[0]]
        t1 = wiz_to_var[c[1]]
        t2 = wiz_to_var[c[2]]
        model.add((t2 <= t0 & t2 <= t1) | (t2 >= t0 & t2 >= t1))
    # make sure all variables have different values
    model.add(AllDiff(vs))
    # solve
    solver = model.load("Mistral")
    solver.solve()
    # store results
    result = [0]*num_wizards
    for w in wizards:
        result[wiz_to_var[w].get_value() - 1] = w
    return result


"""
======================================================================
   No need to change any code below this line
======================================================================
"""

def read_input(filename):
    with open(filename) as f:
        num_wizards = int(f.readline())
        num_constraints = int(f.readline())
        constraints = []
        wizards = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            for w in c:
                wizards.add(w)
                
    wizards = list(wizards)
    return num_wizards, num_constraints, wizards, constraints

def write_output(filename, solution):
    with open(filename, "w") as f:
        for wizard in solution:
            f.write("{0} ".format(wizard))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Constraint Solver.")
    parser.add_argument("input_file", type=str, help = "___.in")
    parser.add_argument("output_file", type=str, help = "___.out")
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    write_output(args.output_file, solution)
