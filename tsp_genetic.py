import random
from graph_dictionary import *

def home_graph(n):
    return Graph(n)

cities = int(input("Number of cities to visit: "))
a = home_graph(cities)
sols = []
print ("dkslahfl")

def create_population(n):
    for i in range(n):
        x = list(a.points)
        sols.append(x)

def shuffle_sol(sol):
    x = list(sol)
    random.shuffle(x)
    return x

def gen_population(n):
    #locs is list of locations that must be traveled to, passed in by user (?)
    #in this case, locs = a.points
    create_population(n)
    sol_lst = sols
    for i in range(len(sol_lst) - 1):
        sol_lst[i] = shuffle_sol(sol_lst[i])
    return sol_lst
    #return list of what order to travel to locations

def check_sol(sol):
    #check that every step in solution given is possible, return boolean
    #use to propagate list of solutions, call in mutate/crossover
    return True

def solution_len(sol):
    x = 0
    for i in (range(len(sol) - 2)):
        # distance between sol[i] and sol[i+1], get info from dictionary
        x += Graph.distance(i, sol[i],sol[i+1])
    # add distance between sol[0] and sol[len(sol)-1]
    x += Graph.distance(i, sol[0], sol[len(sol)-1])
    return x

def fitness(sol):
    return 1/(solution_len(sol))

def best_sol(sol_lst):
    best = 0
    for i in range(len(sol_lst) - 1):
        if solution_len(sol_lst[i]) < solution_len(sol_lst[best]):
            best = i
    # bsol = sol_lst[best]
    # returns position in the array of the best solution
    return best

def print_lengths(sol_lst):
    for i in sol_lst:
        print (solution_len(i))
    return

def weighted_random (sol_lst):
    # choose a solution with probability equal to the inverse of its distance (?)
    sum = 0
    for i in sol_lst:
        sum += fitness(i)
    r = random.uniform(0,sum)
    pos = 0
    for i in sol_lst:
        x = fitness(i)
        if pos + x >= r:
            return i
        else:
            pos += x
    return # shouldn't get down to here because of how random and r are defined

def choose_parents(sol_lst):
    # choose parents from solution list with probability based on their length/fitness
    # return as tuple
    x1 = 0
    x2 = 0
    while x1 == x2:
        x1 = weighted_random(sol_lst)
        x2 = weighted_random(sol_lst)
    return (x1,x2)

def get_rand(parentsol, child):
    # given a parent solution and a child, finds a city in the parent that is
    # not in the child, returns that city
    r = 0
    while (parentsol[r] in child):
        r = random.randint(0, len(parentsol)-1)
    return parentsol[r]

def crossover_helper(parents):
    # given tuple of parents generated from choose_parents, crossover
    # choose first city of either parent at random
    # add consecutive cities by finding the city after it in either parent
    # only add new city if city has not already appeared
    # if both have appeared, choose a new city at random
    # if neither has appeared, pick either
    # Issues: child solution doesn't have characteristics of parent
    x = random.choice(parents)
    x = x[0]
    child = []
    child.append(x)
    while (len(child) < len(parents[1])):
        next1 = parents[0][(parents[0].index(x) + 1) % cities]
        next2 = parents[1][(parents[1].index(x) + 1) % cities]
        if next1 in child:
            if next2 in child:
                r = random.randint(0,1)
                get_rand(parents[r], child)
                next2 = child.append(next2)
                x = next2
            else:
                child.append(next2)
                x = next2
        else:
            #doesn't matter which one is appended
            child.append(next1)
            x = next1
    return child

def crossover(sol_lst):
    # using helper functions, choose two parent solutions and crossover
    # add child solution to sol_lst, increases size by one
    # note - will add repeats
    x = choose_parents(sol_lst)
    a = crossover_helper(x)
    sol_lst.append(a)
    return a

def mutation(sol_lst):
    # choose solution from sol_lst at random, preserve best solution
    # should not change size of sol_lst
    # elitism - i.e. don't mutate the solution with shortest path
    x = random.choice(sol_lst)
    if x == best_sol(sol_lst):
        mutation(sol_lst)
    # mutate solution by swapping two cities at random
    r1 = random.randint(0, cities - 1)
    r2 = random.randint(0, cities - 1)
    stor = x[r1]
    x[r1] = x[r2]
    x[r2] = stor
    return x

def run_gen(num):
    for i in range(num):
        crossover(sols)
        mutation(sols)
        mutation(sols)
    return
