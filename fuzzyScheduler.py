"""
#Author: Yao Lu z5190639
#Date: 2020/06/20

"""
"""
This module provides a fuzzy scheduling problem in this scenario is specified by ignoring orders 
and giving a number of tasks, each with a fixed duration in hours. Each task must start and finish 
on the same day, within working hours (9am to 5pm). In addition, there can be constraints both on 
single tasks and between two tasks.

Object Class:

Constraint -- Store all constraints i.e. binary_constraints, hard_constraints, soft_constraints
Soft_CSP -- Use CSP but add soft_constraints and soft_constraints_cost
Search_with_AC_from_Cost_CSP -- inherit class Search_with_AC_from_CSP from cspConsistency.py which 
    add heuristic() function to calculation the Minimum soft constraints cost

Dynamic objects:

length_of_time -- a dict include tasks duration hours
task_basic_value -- a dict tasks include start time and end time, and end time brfore 5pm 
hard_constraints  -- a list include all hard constraints
soft_constraints -- a dict include all tasks soft constraints
soft_constraints_cost -- a dict include all tasks soft constraints cost

Static Objects: 

day_num -- Store the number of the week
time_num -- Store the number of the time
domain -- Store all the possibility domain，

Functions:

# binary constraint function
binary_constraints_before() -- task1 ends when or before task2 starts
binary_constraints_after() -- task1 starts after or when task2 ends
binary_constraints_sameday() -- task1 and task2 are scheduled on the same day
binary_constraints_startsat() -- task1 starts exactly when task2 ends

# hard constraint function
hard_constraints_day() -- task starts on given day at any time
hard_constraints_time() -- task starts at given time on any day
hard_constraints_startsbefore_daytime() -- task starts at or before given time
hard_constraints_startsafter_daytime() -- task starts at or after given time
hard_constraints_endsbefore_daytime() -- task ends at or before given time
hard_constraints_endsafter_daytime() -- task ends at or after given time
hard_constraints_startin() -- task starts in day-time range
hard_constraints_endin() -- task ends in day-time range
hard_constraints_startsbefore_time() -- task starts at or before time on any day
hard_constraints_endsbefore_time() -- task ends at or before time on any day
hard_constraints_startsafter_time() -- task stats at or after time on any day
hard_constraints_endsafter_time() -- task ends at or after time on any day

output_display() -- Modify the standard display format like assignment requirement output
"""
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

# Create Soft_CSP from cspProblem.py that add satisfy soft_Consistency and soft_constraints_cost
class Soft_CSP(object):
    """The Soft_CSP consists of
    * domains, a dictionary that maps each variable to its domain
    * constraints, a list of constraints
    * variables, a set of variables
    * var_to_const, a variable to set of constraints dictionary
    * soft_constraints, a dictionary that store soft constraints
    * soft_constraints_cost, a dictionary that store store soft cost
    """
    def __init__(self, domains, constraints, soft_constraints, soft_constraints_cost):
        """domains is a variable:domain dictionary
        constraints is a list of constriants
        """
        self.variables = set(domains)
        self.domains = domains
        self.constraints = constraints
        self.var_to_const = {var:set() for var in self.variables}
        self.soft_constraints = soft_constraints
        self.soft_constraints_cost = soft_constraints_cost

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

# rewrite Search_with_AC_from_CSP in cspConsistency.py and add soft_constraints and soft_constraints_cost
class Search_with_AC_from_Cost_CSP(Search_with_AC_from_CSP):
    def __init__(self, csp):
        super().__init__(csp)
        self.cost = []
        self.soft_constraints = csp.soft_constraints
        self.soft_constraints_cost = soft_constraints_cost

"""
Define a set of Static objects and replace working days and times with numbers
* 'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5
* '9am': 1, '10am': 2, '11am': 3, '12pm': 4, '1pm': 5, '2pm': 6, '3pm': 7, '4pm': 8, '5pm': 9
* define domain value use double-digit
* length_of_time -- a dict include tasks duration hours
* task_basic_value -- a dict tasks include start time and end time, and end time brfore 5pm
* hard_constraints  -- a list include all hard constraints
 * soft_constraints -- a dict include all tasks soft constraints
* soft_constraints_cost -- a dict include all tasks soft constraints cost
"""
day_num = {'mon': '1', 'tue': '2', 'wed': '3', 'thu': '4', 'fri': '5'}
time_num = {'9am': '1', '10am': '2', '11am': '3', '12pm': '4', '1pm': '5', '2pm': '6', '3pm': '7', '4pm': '8', '5pm': '9'}
domain = {'11', '12', '13', '14', '15', '16', '17', '18', '19',
          '21', '22', '23', '24', '25', '26', '27', '28', '29',
          '31', '32', '33', '34', '35', '36', '37', '38', '39',
          '41', '42', '43', '44', '45', '46', '47', '48', '49',
          '51', '52', '53', '54', '55', '56', '57', '58', '59'}
length_of_time = {}
task_basic_value = {}
hard_constraints = []
soft_constraints = {}
soft_constraints_cost = {}

# get input data follow binary constraint
def binary_constraints_before(contrast_one,contrast_two):
    return contrast_one[1] <= contrast_two[0]

def binary_constraints_after(contrast_one,contrast_two):
    return contrast_two[1] <= contrast_one[0]

def binary_constraints_sameday(contrast_one,contrast_two):
    return contrast_one[0]//10 == contrast_two[0]//10

def binary_constraints_startsat(contrast_one,contrast_two):
    return contrast_one[0] == contrast_two[1]

# get input data follow hard constraint
def hard_constraints_day(day):
    """is a value"""
    # isv = lambda x: x == val   # alternative definition
    # isv = partial(eq,val)      # another alternative definition
    def isv(x): return x[0]//10 == int(day)
    isv.__name__ = day+"=="
    return isv

def hard_constraints_time(time):
    def isv(x): return x[0]%10 == int(time)
    isv.__name__ = time+"=="
    return isv

def hard_constraints_startsbefore_daytime(day,time):
    def isv(x): return x[0] <= int(day + time)
    return isv

def hard_constraints_startsafter_daytime(day,time):

    def isv(x): return x[0] >= int(day + time)
    return isv

def hard_constraints_endsbefore_daytime(day,time):
    def isv(x): return x[1] <= int(day + time)
    return isv

def hard_constraints_endsafter_daytime(day,time):
    def isv(x): return x[1] >= int(day + time)
    return isv

def hard_constraints_startin(day1,time1,day2,time2):
    def isv(x):
        giventime1 = int(day1 + time1)
        giventime2 = int(day2 + time2)
        return x[0]>=giventime1 and x[0]<=giventime2
    return isv

def hard_constraints_endin(day1,time1,day2,time2):
    def isv(x): return x[1]>=int(day1 + time1) and x[1]<=int(day2 + time2)
    return isv

def hard_constraints_startsbefore_time(time):
    def isv(x): return x[0]%10 <= int(time)
    isv.__name__ = time + "<="
    return isv

def hard_constraints_endsbefore_time(time):
    def isv(x): return x[1]%10 <= int(time)
    isv.__name__ = time + "<="
    return isv

def hard_constraints_startsafter_time(time):
    def isv(x): return x[0]%10 >= int(time)
    isv.__name__ = time + ">="
    return isv

def hard_constraints_endsafter_time(time):
    def isv(x): return x[1]%10 >= int(time)
    isv.__name__ = time + ">="
    return isv

# get tasks with name and duration, and get domain with all possible work time
def read_task_basic_value(line):
    if line[0] == 'task':
        length_of_time[line[1]] = line[2]
        temp = set()
        duration = int(line[2])
        for str in domain:
            if int(str[1]) + duration <= 9:
                temp.add(int(str))
        task_basic_value[line[1]] = set((t, t + duration) for t in temp)
    else:
        pass
    return task_basic_value

# define heuristic() function to calculation the Minimum soft constraints cost
def heuristic (Search_with_AC_from_Cost_CSP, node) :
    cost_min = []
    for task_num in node:
        if task_num in Search_with_AC_from_Cost_CSP.soft_constraints:
            cost_list = []
            last_time = int(Search_with_AC_from_Cost_CSP.soft_constraints[task_num])
            for costs in node[task_num]:
                if costs[1] > last_time:
                    if (costs[1] // 10 - last_time // 10) ==0:
                        min_cost = ((costs[1] % 10) - (last_time % 10))
                    else:
                        over_oneday_cost = (costs[1] // 10 - last_time // 10) * 24
                        same_day_cost = ((costs[1] % 10) - (last_time % 10))
                        min_cost = over_oneday_cost + same_day_cost
                    cost_list.append(Search_with_AC_from_Cost_CSP.soft_constraints_cost[task] * min_cost)
                else:
                    cost_list.append(0)
            if len(cost_min) != 0:
                cost_list.append(min(cost_list))
    min_cost = sum(cost_min)
    return min_cost

# Read input*.txt and change information to dict number that can easy to calculate binary_constraint、hard_constraints、soft_constraints
filename = sys.argv[1]
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
        # get tasks name and duration in dict
        task_basic_value = read_task_basic_value(line)
        # get tasks binary constraints in dict
        if line[0] == 'constraint':
            contrast_one = line[1]
            contrast_two = line[-1]
            if 'before' in line:
                hard_constraints.append(Constraint((contrast_one, contrast_two), binary_constraints_before))
            if 'after' in line:
                hard_constraints.append(Constraint((contrast_one, contrast_two), binary_constraints_after))
            if 'sameday' in line:
                hard_constraints.append(Constraint((contrast_one, contrast_two), binary_constraints_sameday))
            if 'startsat' in line:
                hard_constraints.append(Constraint((contrast_one, contrast_two), binary_constraints_startsat))
        # get tasks soft constraints in dict
        elif (line[0] == 'domain') and (line[2] =='endsby'):
            task = line[1]
            day = day_num[line[3]]
            time = time_num[line[4]]
            soft_constraints_cost[task] = int(line[-1])
            soft_constraints[task] = int(day + time)
        # get task hard domain constraints in *tuple
        elif len(line)==3:
            task = line[1]
            if (line[0] == 'domain') and (line[2] in day_num):
                day = day_num[line[2]]
                hard_constraints.append(Constraint((task,), hard_constraints_day(day)))
            elif (line[0] == 'domain') and (line[2] in time_num):
                time = time_num[line[2]]
                hard_constraints.append(Constraint((task,), hard_constraints_time(time)))
        elif len(line)>3:
            task = line[1]
            if (line[0] == 'domain') and (line[2] == 'startsbefore') and (line[3] in day_num):
                day = day_num[line[-2]]
                time = time_num[line[-1]]
                hard_constraints.append(Constraint((task,), hard_constraints_startsbefore_daytime(day, time)))
            elif (line[0] == 'domain') and (line[2] == 'startsafter') and (line[3] in day_num):
                day = day_num[line[-2]]
                time = time_num[line[-1]]
                hard_constraints.append(Constraint((task,), hard_constraints_startsafter_daytime(day, time)))
            elif (line[0] == 'domain') and (line[2] == 'endsbefore') and (line[3] in day_num):
                day = day_num[line[-2]]
                time = time_num[line[-1]]
                hard_constraints.append(Constraint((task,), hard_constraints_endsbefore_daytime(day, time)))
            elif (line[0] == 'domain') and (line[2] == 'endsafter') and (line[3] in day_num):
                day = day_num[line[-2]]
                time = time_num[line[-1]]
                hard_constraints.append(Constraint((task,), hard_constraints_endsafter_daytime(day, time)))
            elif (line[0] == 'domain') and (line[2] == 'startsin'):
                day1 = day_num[line[3]]
                if len(line[4])==6:
                    time=line[4][0:3]
                    day=line[4][3:6]
                else:
                    time=line[4][0:4]
                    day=line[4][4:7]
                time1 = time_num[time]
                day2 = day_num[day]
                time2 = time_num[line[5]]
                hard_constraints.append(Constraint((task,), hard_constraints_startin(day1, time1, day2, time2)))
            elif (line[0] == 'domain') and (line[2] == 'endsin'):
                day1 = day_num[line[3]]
                if len(line[4])==6:
                    time=line[4][0:3]
                    day=line[4][3:6]
                else:
                    time=line[4][0:4]
                    day=line[4][4:7]
                time1 = time_num[time]
                day2 = day_num[day]
                time2 = time_num[line[5]]
                hard_constraints.append(Constraint((task,), hard_constraints_endin(day1, time1, day2, time2)))
            elif (line[0] == 'domain') and (line[2] == 'startsbefore') and (line[3] in time_num):
                if len(line) == 5:
                    time = time_num[line[-1]]
                    hard_constraints.append(Constraint((task,), hard_constraints_startsbefore_time(time)))
            elif (line[0] == 'domain') and (line[2] == 'endsbefore') and (line[3] in time_num):
                time = time_num[line[-1]]
                hard_constraints.append(Constraint((task,), hard_constraints_endsbefore_time(time)))
            elif (line[0] == 'domain') and (line[2] == 'startsafter') and (line[3] in time_num):
                time = time_num[line[-1]]
                hard_constraints.append(Constraint((task,), hard_constraints_startsafter_time(time)))
            elif (line[0] == 'domain') and (line[2] == 'endsafter') and (line[3] in time_num):
                time = time_num[line[-1]]
                hard_constraints.append(Constraint((task,), hard_constraints_endsafter_time(time)))

# Modify the standard display format like assignment requirement output
def output_display(min_soft_scheme,search_problem):
    if min_soft_scheme is not None:
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

soft_CSP = Soft_CSP(task_basic_value,hard_constraints,soft_constraints,soft_constraints_cost)
search_problem = Search_with_AC_from_Cost_CSP(soft_CSP)
min_soft_scheme = GreedySearcher(search_problem).search()
output_display(min_soft_scheme,search_problem)
