import random
from graph_dictionary import *

def create_population(n, lst, sols):
    # creates n identical solutions from the list of points given
    for i in range(n):
        sols.append(lst)
    return sols

def shuffle_sol(sol):
    # shuffles an individual solution, checks that length is preserved
    x = list(sol)
    xlen = len(x)
    random.shuffle(x)
    assert (len(x) == xlen)
    return x

def gen_population(n, lst, sols):
    # Use to generate n random solutions as initial population, can be used after
    # initial generation if needed
    # locs is list of locations that must be traveled to, passed in by user
    x = len(sols)
    # populate sols with n identical solutions
    create_population(n, lst, sols)
    for i in range(len(sols) - 1):
        sols[i] = shuffle_sol(sols[i])
    assert len(sols) == n+x
    return
    #return list of what order to travel to locations

def check_sol(sol):
    # Given a solution, return true if the solution is possible
    # use if graph is not complete
    # use to propagate list of solutions, call in mutate/crossover
        # pseudocode: check that every step in solution given is possible, return boolean
    return True

def solution_len(sol, a, start_end):
    # Given a solution (list of cities in the order visited), return total distance
    # including the initial city
    # add distance between initial city and first city visited
    x = Graph.distance(a, start_end, sol[0])
    for i in (range(len(sol) - 2)):
        # distance between each city in solution, get info from dictionary
        x += Graph.distance(a, sol[i],sol[i+1])
    # add distance between end of solution and initial city
    x += Graph.distance(a, sol[len(sol)-1], start_end)
    return x

def fitness(sol,a,initial):
    # since we want the shortest path, the fitness of a solution is the inverse of its distance
    return 1/(solution_len(sol,a,initial))

def best_sol(sol_lst,a,initial):
    # returns position in the array of the best solution in the array (sol_lst)
    best = 0
    for i in range(len(sol_lst) - 1):
        if solution_len(sol_lst[i],a,initial) < solution_len(sol_lst[best],a,initial):
            best = i
    return best

def print_lengths(sol_lst):
    #use for testing, mainly
    for i in sol_lst:
        print (solution_len(i))
    return

def weighted_random (sol_lst,a,initial):
    # choose a solution with probability equal to the inverse of its distance (?)
    # use in choose_parents to select "fit" parents
    sum = 0
    for i in sol_lst:
        sum += fitness(i,a,initial)
    r = random.uniform(0,sum)
    pos = 0
    for i in sol_lst:
        x = fitness(i,a,initial)
        if pos + x >= r:
            return i
        else:
            pos += x
    return # shouldn't get down to here because of how random and r are defined

def choose_parents(sol_lst,a,initial):
    # choose parents from solution list with probability based on their length/fitness
    # return as tuple
    x1 = 0
    x2 = 0
    while x1 == x2:
        x1 = weighted_random(sol_lst,a,initial)
        x2 = weighted_random(sol_lst,a,initial)
    return (x1,x2)

def get_rand(parentsol, child):
    # given a parent solution and a child, finds a city in the parent that is
    # not in the child, returns that city
    r = 0
    while (parentsol[r] in child):
        r = random.randint(0, len(parentsol)-1)
    return parentsol[r]

def crossover_helper(parents,cities):
    # implements order crossover (OX) algorithm
    # randomly picks an swath of "genes" in one parent and puts that in same location in child
    # rest of child is comprised of other parent's genes

    # start, end represent absolute positions in list not indices
    # cities-2 as upper bound for start and start+1 as lower for end ensure swath is at least 1 long
    swath_start = random.randint(1, cities-2)
    swath_end = random.randint(swath_start+1, cities-1)
    # take first parent in tuple as "donor" parent, doesn't matter since "first" was arbitrarily assigned
    donor = parents[0]
    nondonor = parents[1]
    swath = donor[swath_start-1:swath_end]
    filtered = filter(lambda x: x not in swath, nondonor)

    child = filtered[:swath_start-1] + swath + filtered[swath_start-1:]
    '''
    latter_length = len(donor) - swath_end
    # reorder to make it easier to concat afterwards
    reordered = nondonor[swath_end:] + nondonor[:swath_end]
    filtered = filter(lambda x: x not in swath, reordered)

    child = filtered[-swath_start:] + swath + filtered[:latter_length]
    '''
    
    return child


    # given tuple of parents generated from choose_parents, crossover
    # choose first city of either parent at random
    # add consecutive cities by finding the city after it in either parent
    # only add new city if city has not already appeared
    # if both have appeared, choose a new city at random
    # if neither has appeared, pick either
    # Issues: child solution doesn't have characteristics of parent
   
    """
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
    """

def crossover(sol_lst,a,initial,cities):
    # using helper functions, choose two parent solutions and crossover
    # add child solution to sol_lst, increases size by one
    # note - will add repeats
    x = choose_parents(sol_lst,a,initial)
    a = crossover_helper(x,cities)
    sol_lst.append(a)
    return a

def mutation(sol_lst, a, initial):
    # choose solution from sol_lst at random, preserve best solution
    # should not change size of sol_lst
    # elitism - i.e. don't mutate the solution with shortest path
    x = sol_lst[best_sol(sol_lst,a,initial)]
    while (x == sol_lst[best_sol(sol_lst,a,initial)]):
        x = random.choice(sol_lst)
    # mutate solution by swapping two cities at random
    r1 = random.randint(0, len(x) - 1)
    r2 = random.randint(0, len(x) - 1)
    stor = x[r1]
    x[r1] = x[r2]
    x[r2] = stor
    return x

def factorial (n):
    if n < 2:
        return 0
    else:
        return n * factorial(n-1)

def max_num(sols, cities):
    limit = factorial(cities)
    if (len(sols) < limit):
        return False
    else:
        return True

def run_gen(num, sols, a, start_end, cities, locs):
    # use to run genetic
    if (cities < 2):
        sols.append(locs)
        return
    else:
        for i in range(num):
            if max_num(sols, cities):
                return
            else:
                crossover(sols, a, start_end, cities)
                mutation(sols, a, start_end)
                mutation(sols, a, start_end)
        return
