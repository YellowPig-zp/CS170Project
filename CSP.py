import itertools
from utils import argmin_random_tie, count, first

CTYPE0 = 0
CTYPE1 = 1

class Node:
    def __init__(self, variable, num_wizards, mode = 0):
        self.name = variable
        self.current_domain = None
        if mode == 0:
            self.domain = list(range(num_wizards))
            self.value  = None
        elif mode == 1:
            temp = list(range(num_wizards))
            self.domain = list(itertools.permutations(temp, 2))
            self.value = None

class CSP:
    def __init__(self, num_wizards, num_constraints, wizards, constraints):
        # self.constraints is a dictionary of "string_variable_name : [list of CONSTRAINT_EDGEs]" key, value pairs
        # where CONSTRAINT_EDGE is a tuple
        # self.variables is a dictionary of "string_variable_name : variable_node" pairs
        new_constraints = {}
        self.variables = {}
        self.variablesHaveCurrDomains = False
        self.assignedValues = set()

        for variable in wizards:
            self.variables[variable] = Node(variable, num_wizards, mode = 0)
            new_constraints[variable] = []

        for constraint in constraints:
            VAR0 = constraint[0]
            VAR1 = constraint[1]
            VAR2 = constraint[2]

            # CONSTRAINT is a (VAR0, VAR1, VAR2, #CTYPE) tuple. CTYPE0 means VAR2 < min(VAR0, VAR1) or VAR2 > max(VAR0, VAR1)
            # CTYPE1 means VAR0 < min(VAR1, VAR2) or VAR0 > max(VAR1, VAR2)
            c0 = (VAR0, VAR1, VAR2, CTYPE0)
            c1 = (VAR1, VAR0, VAR2, CTYPE0)
            c2 = (VAR2, VAR0, VAR1, CTYPE1)

            #Adding constraints to variables
            new_constraints[VAR0].append(c0)
            new_constraints[VAR1].append(c1)
            new_constraints[VAR2].append(c2)

        self.constraints = new_constraints
        self.num_variables = len(self.variables)
        """
        for constraint in constraints:
            new_variable = constraint[0] + constraint[1]
            self.variables[new_variable] = Node(new_variable, num_wizards, mode = 1)
            # CONSTRAINT_EDGE is forming as (VAR1, VAR2, #MODE) pairs
            # where (VAR0, VAR1, 0) means VAR0 = VAR1[0]
            # and (VAR0, VAR1, 1) means VAR0 = VAR1[1]
            # and (VAR0, VAR1, 2) means VAR0[0] = VAR1
            # and (VAR0, VAR1, 3) means VAR0[1] = VAR1
            # and (VAR0, VAR1, 4) means VAR0 > max(VAR1[0], VAR1[1]) or VAR0 < min(VAR1[0], VAR1[1])
            # and (VAR0, VAR1, 5) means VAR1 > max(VAR0[0], VAR0[1]) or VAR1 < min(VAR0[0], VAR0[1])
            c0 = (constraint[0], new_variable, 0)
            c1 = (constraint[1], new_variable, 1)
            c2 = (new_variable, constraint[0], 2)
            c3 = (new_variable, constraint[1], 3)
            c4 = (constraint[2], new_variable, 4)
            c5 = (new_variable, constraint[2], 5)
            if constraint[0] not in new_constraints:
                new_constraints[constraint[0]] = []
                new_constraints[constraint[0]].append(c0)
            else:
                new_constraints[constraint[0]].append(c0)
            if constraint[1] not in new_constraints:
                new_constraints[constraint[1]] = []
                new_constraints[constraint[1]].append(c1)
            else:
                new_constraints[constraint[1]].append(c1)
            if new_variable not in new_constraints:
                new_constraints[new_variable] = []
                new_constraints[new_variable].extend([c2, c3, c5])
            else:
                new_constraints[new_variable].extend([c2, c3, c5])
            if constraint[2] not in new_constraints:
                new_constraints[constraint[2]] = []
                new_constraints[constraint[2]].append(c4)
            else:
                new_constraints[constraint[2]].append(c4)
        """

        """
        for i in range(num_wizards):
            for j in range(i+1, num_wizards):
                # (VAR1, VAR2, 6) means not VAR1 == VAR2
                c0 = (wizards[i], wizards[j], 6)
                c0_prime = (wizards[j], wizards[i], 6)
                if wizards[i] not in new_constraints:
                    new_constraints[wizards[i]] = []
                    new_constraints[wizards[i]].append(c0)
                else:
                    new_constraints[wizards[i]].append(c0)
                if wizards[j] not in new_constraints:
                    new_constraints[wizards[j]] = []
                    new_constraints[wizards[j]].append(c0_prime)
                else:
                    new_constraints[wizards[j]].append(c0_prime)
        """

        """
        for variable in wizards:
            self.variables[variable] = Node(variable, num_wizards, mode = 0)
        self.constraints = new_constraints
        self.num_variables = len(self.variables)
        """

    def assign(self, var, val, assignment):
        assignment[var] = val
        self.assignedValues.add(val)

    def unassign(self, var, assignment):
        if var in assignment:
            val = assignment[var]
            del assignment[var]
            self.assignedValues.remove(val)

    def support_pruning(self):
        if not self.variablesHaveCurrDomains:
            for var_name in self.variables:
                var = self.variables[var_name]
                var.current_domain = list(var.domain)
            self.variablesHaveCurrDomains = True

    def prune(self, var, val, removals):
        """remove var = val from var's current_domain"""
        self.variables[var].current_domain.remove(val)
        if removals is not None:
            removals.append((var, val))

    def suppose(self, var, val):
        """supposing var = val"""
        self.support_pruning()
        removals = [(var, other_val) for other_val in self.variables[var].current_domain if not other_val == val]
        self.variables[var].current_domain = [val]
        return removals

    def popVariable(self):
        return self.variables.popitem()

    def addVariable(self, variable_name, variable_node):
        self.variables[variable_name] = variable_node

    def checkConsistency(self, var, val, assignment):
        if var not in self.constraints:
            return True
        if val in self.assignedValues:
            return False
        constraints = self.constraints[var]
        for c in constraints:
            if not self.checkConstraint(var, val, c, assignment):
                return False
        return True

    def checkConstraint(self, var, val, c, assignment):
        VAR0 = c[0]
        VAR1 = c[1]
        VAR2 = c[2]
        CTYPE = c[3] # constraint type
        if VAR1 not in assignment or VAR2 not in assignment:
            return True
        val0 = val
        val1 = assignment[VAR1]
        val2 = assignment[VAR2]
        if CTYPE == CTYPE0:
            return val2 < min(val0, val1) or val2 > max(val0, val1)
        if CTYPE == CTYPE1:
            return val0 < min(val1, val2) or val0 > min(val1, val2)

    def checkConstraintSatisfaction(self, X0, x0, X1, x1, X2, x2, CTYPE):
        # print(var0, val0, var1, val1, edge_type)
        if CTYPE == CTYPE0:
            return x2 < min(x0, x1) or x2 > max(x0, x1)
        if CTYPE == CTYPE1:
            return x0 < min(x1, x2) or x0 > min(x1, x2)

    def restore(self, removals):
        for var, val in removals:
            self.variables[var].current_domain.append(val)

    def choices(self, var):
        return self.variables[var].current_domain or self.variables[var].domain

# AC3
def AC3(csp, queue=None, removals=None):
    if queue is None:
        queue = [constraint for Xi in csp.variables for constraint in csp.constraints[Xi]]
    csp.support_pruning()
    while queue:
        (X0, X1, X2, CTYPE) = queue.pop()
        # print(Xi, Xj, edge_type)
        if revise(csp, X0, X1, X2, CTYPE, removals):
            if not csp.variables[X0].current_domain:
                return False
            for constraint in csp.constraints[X0]:
                queue.append((constraint[1], constraint[0], constraint[2], CTYPE0))
                queue.append((constraint[2], constraint[0], constraint[1], CTYPE1))
    return True

def revise(csp, X0, X1, X2,CTYPE, removals):
    revised = False
    for x0 in csp.variables[X0].current_domain[:]:
        if all(not csp.checkConstraintSatisfaction(X0, x0, X1, x1, X2, x2, CTYPE) for x1 in
               csp.variables[X1].current_domain for x2 in csp.variables[X2].current_domain):
            csp.prune(X0, x0, removals)
            revised = True
    return revised

# Inference
def MAC(csp, var, val, assignment, removals):
    """Maintain arc consistency"""
    queue = [constraint
             for constraint in csp.constraints[var]]
    return AC3(csp, queue, removals)

# Actual Search
def BT_Search(csp):
    return Recursive_BT({}, csp)

def Recursive_BT(assignment, csp):
    if checkAssignmentComplete(assignment, csp):
        return assignment
    printOriginal(assignment)
    var_name = MRV(assignment, csp)
    for val in LCV(csp, var_name):
        if csp.checkConsistency(var_name, val, assignment):
            csp.assign(var_name, val, assignment)
            removals = csp.suppose(var_name, val)
            if MAC(csp, var_name, val, assignment, removals):
                result = Recursive_BT(assignment, csp)
                if result is not None:
                    return result
            csp.restore(removals)
            csp.unassign(var_name, assignment)
    return None

def checkAssignmentComplete(assignment, csp):
    return len(assignment) == csp.num_variables

# Variable ordering
def MRV(assignment, csp):
    """Minimum remaining value"""
    return argmin_random_tie(
        [var for var in csp.variables if var not in assignment],
        key = lambda var: remainingValues(csp, var, assignment)
    )

def remainingValues(csp, var, assignment):
    if csp.variables[var].current_domain:
        return len(csp.variables[var].current_domain)
    else:
        return count(csp.checkConsistency(var, val, assignment) for val in csp.variables[var].domain)

# Variable ordering
def numPairsConflict(csp, var, val):
    """check how many pairs of values would be conflicted if we set var = val"""
    csp.support_pruning()
    queue = [constraint
             for constraint in csp.constraints[var]]
    count = 0
    while queue:
        (X0, X1, X2, CTYPE) = queue.pop()
        # print(Xi, Xj, edge_type)
        for x1 in csp.variables[X1].current_domain:
            for x2 in csp.variables[X2].current_domain:
                if not csp.checkConstraintSatisfaction(X0, val, X1, x1, X2, x2, CTYPE):
                    count += 1
    return count

def LCV(csp, var):
    return sorted(csp.choices(var),
                  key=lambda val : numPairsConflict(csp, var, val))

# Extra helper methods
def getEdgeCorrespondency(x):
    """helper method for MAC. This turns an edge A->B into B->A"""
    if x == 0:
        return 2
    if x == 1:
        return 3
    if x == 2:
        return 0
    if x == 3:
        return 1
    if x == 4:
        return 5
    if x == 5:
        return 4
    if x == 6:
        return x

def printOriginal(assignment):
    toPrint = "{"
    for key in assignment:
        toPrint += key + " : " + str(assignment[key]) + ", "
    toPrint += "}"
    print(toPrint)