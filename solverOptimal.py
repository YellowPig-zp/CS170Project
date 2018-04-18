# solverOptimal:
import argparse
from ortools.constraint_solver import pywrapcp

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
                     where constraints[0] may take the form ['A', 'B', 'C']i

    Output:
        An array of wizard names in the ordering your algorithm returns
    """
    solver = pywrapcp.Solver("sol")  # import the solver from ortool
    num_vals = num_wizards
    variables = []
    name_to_var = {}
    var_to_name = []
    for variable in wizards:
        temp = solver.IntVar(0, num_vals - 1, variable)
        variables.append(temp)
        name_to_var[variable] = temp  # send names into the variable array
        var_to_name.append((temp, variable))  # setup the variable list with tuples
    solver.Add(solver.AllDifferent(variables))

    for constraint in constraints:
    	if sameName(constraint):
    		continue
    	w0 = name_to_var[constraint[0]]
    	w1 = name_to_var[constraint[1]]
    	w2 = name_to_var[constraint[2]]
    	solver.Add(solver.Max(w2 < solver.Min(w0, w1), w2 > solver.Max(w0, w1)) == 1)

    db = solver.Phase(variables, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)  # assign new value to var
    solver.NewSearch(db)
    solver.NextSolution()  # get the solution
    result = [0] * num_vals
    for var in variables:
        result[var.Value()] = getName(var_to_name, var)  # turn tuples back to a list of names
    return result

def sameName(constraint):
	return constraint[0] == constraint[1] or \
	constraint[0] == constraint[2] or constraint[1] == constraint[2]
	
# A helper function that find the wizard name by its value
def getName(var_to_name, var):
    for x, y in var_to_name:
        if x is var:
            return y


# A helper function turn boolean to 0,1
def num(x):
    if x:
        return 1
    return 0

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
