import random

def gen_rand_solution(locs):
    #locs is list of locations that must be traveled to, passed in by user (?)
    return random.shuffle(range(len(locs)))
    #return list of what order to travel to locations

def check_sol(sol):
    #check that every step in solution given is possible, return boolean
    #use to propagate list of solutions, call in mutate/crossover
    return True

def solution_len(sol):
    x = 0
    for i in range(len(sol) - 1) in sol:
        x += # distance between sol[i] and sol[i+1], get info from dictionary
    x += # add distance between sol[0] and sol[len(sol)-1]
    return x

def fitness(sol):
    return 1/(solution_len(sol))

def best_sol(sol_lst):
    best = sol_lst[0]
    for i in sol_lst:
        if solution_len(i) < solution_len(best):
            best = i
    return best

def weighted_random (sol_lst):
    # choose a solution with probability equal to the inverse of its distance (?)
    sum = 0
    for i in sol_lst
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
    # choose parents from solution list with probability based on their length
    # return as tuple
    x1 = weighted_random(sol_lst)
    x2 = weighted_random(sol_lst)
    if x1 = x2:
        choose_parents(sol_lst)
    else:
        return (x1,x2)

def crossover(parents)
    # given tuple of parents generated from choose_parents, crossover
    # using greedy crossover - choose first city of either parent at random
    # choose next city by looking at paths for that city in both parents
    # pick the shorter path, repeat until path is complete
    # only choose cities that have not already appeared
    # if both have appeared, choose a new city at random
    r = random.randint(0,1)
    x = (parents[r])[0]
    child.append(x)
    while (len(child) < len(x)):
        next1 = parents[0][array.index(x) + 1]
        next2 = parents[1][array.index(x) + 1]
        if next1 in c:
            if next2 in c:
                # choose new city at random
            else:
                child.append(next2)
                x = next2
        else:
            if next2 in c:
                child.append(next1)
                x = next1
            else:
                # pick city with shorter path
    return child

def mutation(sol_lst)
    # choose solution from sol_lst at random, preserve best solution
    # elitism - i.e. don't mutate the solution with shortest path
    x = random.choice(sol_lst)
    if x = best_sol(sol_lst):
        mutation(sol_lst)
    # mutate solution by swapping two cities at random
    r1 = random.randint(0, len(sol_lst) - 1)
    r2 = random.randint(0, len(sol_lst) - 1)
    stor = sol_lst[r1]
    sol_lst[r1] = sol_lst[r2]
    sol_lst[r2] = stor
    return sol_lst
