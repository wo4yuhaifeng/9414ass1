import sys
from cspConsistency import Search_with_AC_from_CSP
from searchGeneric import GreedySearcher

# Use AIpython code to Create Constraint class, in order to get right format combine all variables and conditions
class Constraint(object):
    """A Constraint consists of
    * scope: a tuple of variables
    * condition: a function that can applied to a tuple of values
    for the variables
    """
    def __init__(self, scope, condition):
        self.scope = scope
        self.condition = condition

    def __repr__(self):
        return self.condition.__name__ + str(self.scope)

    def holds(self,assignment):
        """returns the value of Constraint con evaluated in assignment.

        precondition: all variables are assigned in assignment
        """
        return self.condition(*tuple(assignment[v] for v in self.scope))

# Create Soft_CSP from cspProblem.py that add satisfy soft_Consistency and soft_cost
class Soft_CSP(object):
    """The Soft_CSP consists of
    * domains, a dictionary that maps each variable to its domain
    * constraints, a list of constraints
    * variables, a set of variables
    * var_to_const, a variable to set of constraints dictionary
    * soft_constraints, a dictionary that store soft constraints
    * soft_cost, a dictionary that store store soft cost
    """
    def __init__(self, domains, constraints, soft_constraints, soft_cost):
        """domains is a variable:domain dictionary
        constraints is a list of constriants
        """
        self.variables = set(domains)
        self.domains = domains
        self.constraints = constraints
        self.var_to_const = {var:set() for var in self.variables}
        self.soft_constraints = soft_constraints
        self.soft_cost = soft_cost

        for con in constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)

    def __str__(self):
        """string representation of CSP"""
        return str(self.domains)

    def __repr__(self):
        """more detailed string representation of CSP"""
        return "CSP("+str(self.domains)+", "+str([str(c) for c in self.constraints])+")"

    def consistent(self,assignment):
        """assignment is a variable:value dictionary
        returns True if all of the constraints that can be evaluated
                        evaluate to True given assignment.
        """
        return all(con.holds(assignment)
                    for con in self.constraints
                    if all(v in  assignment  for v in con.scope))

# Define a set of global variables and replace working days and times with numbers
# 'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5
# '9am': 1, '10am': 2, '11am': 3, '12pm': 4, '1pm': 5, '2pm': 6, '3pm': 7, '4pm': 8, '5pm': 9
day_num = {'mon': '1', 'tue': '2', 'wed': '3', 'thu': '4', 'fri': '5'}
time_num = {'9am': '1', '10am': '2', '11am': '3', '12pm': '4', '1pm': '5', '2pm': '6', '3pm': '7', '4pm': '8', '5pm': '9'}

# binary constraint
def binary_constraints_before(contrast_one,contrast_two):
    return contrast_one[1] <= contrast_two[0]

def binary_constraints_after(contrast_one,contrast_two):
    return contrast_two[1] <= contrast_one[0]

def binary_constraints_sameday(contrast_one,contrast_two):
    return contrast_one[0]//10 == contrast_two[0]//10

def binary_constraints_startsat(contrast_one,contrast_two):
    return contrast_one[0] == contrast_two[1]

# hard constraint
def hard_day(day):
    hardday = lambda x: int(x[0][0]) == int(day)
    return hardday

def hard_time(time):
    def hardtime(val):

        return val[0]%10 == int(time)
    return hardtime

def hard_starts_before_daytime(day,time):
    def startsbefore(val):
        giventime = day + time
        return int(val[0]) <= int(giventime)
    return startsbefore

def hard_starts_before_time(time):
    def startsbefore(val):
        return int(val[0][1]) <= time
    return startsbefore

def hard_starts_after_daytime(day,time):
    def startsafter(val):
        giventime = day + time
        return int(val[0]) >= int(giventime)
    return startsafter

def hard_starts_after_time(time):
    def startsafter(val):
        return int(val[0][1]) >= int(time)
    return startsafter

def hard_ends_before_daytime(day,time):
    def endsbefore(val):
        giventime = day + time
        return int(val[1]) <= int(giventime)
    return endsbefore

def hard_ends_before_time(time):
    def endsbefore(val):
        return int(val[1][1]) <= int(time)
    return endsbefore

def hard_ends_after_daytime(day,time):
    def endsafter(val):
        giventime = day + time
        return int(val[1]) >= int(giventime)
    return endsafter

def hard_ends_after_time(time):
    def endsafter(val):
        return int(val[1][1]) >= int(time)
    return endsafter

def hard_startin_range(day1,time1,day2,time2):
    def start_range(val):
        giventime1 = day1 + time1
        giventime2 = day2 + time2
        return int(val[0]) >= int(giventime1) and int(val[0]) <= int(giventime2)
    return start_range

def hard_endin_range(day1,time1,day2,time2):
    def end_range(val):
        giventime1 = day1 + time1
        giventime2 = day2 + time2
        return int(val[1]) >= int(giventime1) and int(val[1]) <= int(giventime2)
    return end_range



# Read input.txt and change information to dict number that can easy to calculate binary_constraint、hard_constraint、soft_constraint
filename = sys.argv[1]
#filename = 'input1.txt'

domain = {'11', '12', '13', '14', '15', '16', '17', '18', '19', '21', '22', '23', '24', '25', '26', '27', '28', '29', '31', '32', '33', '34', '35', '36', '37', '38', '39', '41', '42', '43', '44', '45', '46', '47', '48', '49', '51', '52', '53', '54', '55', '56', '57', '58', '59'}

length_of_time = {}
task_domain = {}
hard_constraint = []
soft_constraint = {}
soft_cost = {}
task_list = []

def read_task_domain(line):
    if line[0] == 'task':
        #print(line)
        length_of_time[line[1]] = line[2]
        temp = set()
        duration = int(line[2])
        for str in domain:
            if int(str[1]) + duration <= 9:
                temp.add(int(str))
        task_domain[line[1]] = set((t, t + duration) for t in temp)
    else:
        pass
    return task_domain

with open(filename,'r') as file:

    for line in file:
        line = line.strip()
        line = line.strip()
        line = line.replace(',', '')
        line = line.replace('-', '')
        line = line.split(' ')
        if '#' in line:
            continue
        if line[0] == '':
            continue
        task_domain = read_task_domain(line)

        if line[0] == 'constraint':
            contrast_one = line[1]
            contrast_two = line[-1]
            if 'before' in line:
                hard_constraint.append(Constraint((contrast_one, contrast_two), binary_constraints_before))
            if 'after' in line:
                hard_constraint.append(Constraint((contrast_one, contrast_two), binary_constraints_after))
            if 'sameday' in line:
                hard_constraint.append(Constraint((contrast_one, contrast_two), binary_constraints_sameday))
            if 'startsat' in line:
                hard_constraint.append(Constraint((contrast_one, contrast_two), binary_constraints_startsat))

        elif (line[0] == 'domain') and (line[2] =='endsby'):
            task = line[1]
            day = day_num[line[3]]
            time = time_num[line[4]]
            soft_cost[task] = int(line[-1])
            soft_constraint[task] = int(day + time)

        elif len(line)==3:
            task = line[1]
            if (line[0] == 'domain') and (line[2] in day_num):
                day = day_num[line[2]]
                hard_constraint.append(Constraint((task,), hard_day(day)))
            elif (line[0] == 'domain') and (line[2] in time_num):
                time = time_num[line[2]]
                hard_constraint.append(Constraint((task,), hard_time(time)))

        elif len(line)>3:
            task = line[1]
            if (line[0] == 'domain') and (line[2] == 'startsbefore') and (line[3] in day_num):
                day = day_num[line[-2]]
                time = time_num[line[-1]]
                hard_constraint.append(Constraint((task,), hard_starts_before_daytime(day, time)))
            elif (line[0] == 'domain') and (line[2] == 'startsafter') and (line[3] in day_num):
                day = day_num[line[-2]]
                time = time_num[line[-1]]
                hard_constraint.append(Constraint((task,), hard_starts_after_daytime(day, time)))
            elif (line[0] == 'domain') and (line[2] == 'endsbefore') and (line[3] in day_num):
                day = day_num[line[-2]]
                time = time_num[line[-1]]
                hard_constraint.append(Constraint((task,), hard_ends_before_daytime(day, time)))
            elif (line[0] == 'domain') and (line[2] == 'endsafter') and (line[3] in day_num):
                day = day_num[line[-2]]
                time = time_num[line[-1]]
                hard_constraint.append(Constraint((task,), hard_ends_after_daytime(day, time)))
            elif (line[0] == 'domain') and (line[2] == 'startsin'):
                day1 = day_num[line[3]]
                time=line[4][0:3]
                day=line[4][3:6]
                time1 = time_num[time]
                day2 = day_num[day]
                time2 = time_num[line[5]]
                #print(hard_constraint)
                hard_constraint.append(Constraint((task,), hard_startin_range(day1, time1, day2, time2)))
            elif (line[0] == 'domain') and (line[2] == 'endsin'):
                day1 = day_num[line[3]]
                time1 = time_num[line[4]]
                day2 = day_num[line[5]]
                time2 = time_num[line[5]]
                hard_constraint.append(Constraint((task,), hard_endin_range(day1, time1, day2, time2)))
            elif (line[0] == 'domain') and (line[2] == 'startsbefore') and (line[3] in time_num):
                if len(line) == 5:
                    time = time_num[line[-1]]
                    hard_constraint.append(Constraint((task,), hard_starts_before_time(time)))
            elif (line[0] == 'domain') and (line[2] == 'endsbefore') and (line[3] in time_num):
                time = time_num[line[-1]]
                hard_constraint.append(Constraint((task,), hard_ends_before_time(time)))
            elif (line[0] == 'domain') and (line[2] == 'startsafter') and (line[3] in time_num):
                time = time_num[line[-1]]
                hard_constraint.append(Constraint((task,), hard_starts_after_time(time)))
            elif (line[0] == 'domain') and (line[2] == 'endsafter') and (line[3] in time_num):
                time = time_num[line[-1]]
                hard_constraint.append(Constraint((task,), hard_ends_after_time(time)))


class Search_with_AC_from_Cost_CSP(Search_with_AC_from_CSP):
    def __init__(self,csp):
        super().__init__(csp)
        self.cost = []
        self.soft_cons = csp.soft_constraints
        self.soft_cost = soft_cost

    def heuristic(self,node):
        #print(node)
        cost = 0
        cost_list = []
        for task in node:
            if task in self.soft_cons:
                temp = []
                expect_time = self.soft_cons[task]
                for value in node[task]:
                    actual_time = value[1]
                    if actual_time > expect_time:
                        delay = (actual_time//10- expect_time//10)*24 + ((actual_time%10) - (expect_time%10))
                        temp.append(self.soft_cost[task] * delay)
                    else:
                        temp.append(0)

                if len(temp)!=0:
                    cost_list.append(min(temp))

        cost = sum(cost_list)

        return cost

# Modify the standard display format like output.txt
def output_display(min_soft_scheme,search_problem):
    if min_soft_scheme is not None:
        #returns the node at the end of the path, and transfer to output
        best_scheme=min_soft_scheme.end()
        for task in min_soft_scheme.end():
            day = str(list(best_scheme[task])[0][0])[0]
            time = str(list(best_scheme[task])[0][0])[1]
            for day_key in day_num:
                if day_num[day_key] == day:
                    day = day_key
            for time_key in time_num:
                if time_num[time_key] == time:
                    time = time_key
            print(f'{task}:{day} {time}')
        print(f'cost:{search_problem.heuristic(best_scheme)}')
    else:
        print('No solution')






soft_CSP = Soft_CSP(task_domain,hard_constraint,soft_constraint,soft_cost)
search_problem = Search_with_AC_from_Cost_CSP(soft_CSP)
min_soft_scheme = GreedySearcher(search_problem).search()
output_display(min_soft_scheme,search_problem)


