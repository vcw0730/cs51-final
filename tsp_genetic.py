import random, copy
from graph_dictionary import *
import time

def tsp_genetic(num, sols, g, start_end, cities, locs):

    def gen_population(n, lst, solution_lst):
        """Use to generate n random solutions as initial population, can be used
        after initial generation if needed locs is list of locations that must
        be traveled to, passed in by user"""   
        def create_population(n, template, solution_lst):
            """creates n identical solutions from the list of points given"""
            for i in range(n):
                x = copy.copy(template)
                solution_lst.append(x)
            return solution_lst

        def shuffle_sol(sol):
            """shuffles an individual solution, checks that length is preserved"""
            sol_len = len(sol)
            random.shuffle(sol)
            assert (len(sol) == sol_len)
            return sol

        # populate sols with n identical solutions
        solution_lst = create_population(n, lst, solution_lst)
        new_sol_lst = [None] * len(solution_lst)

        # shuffle each of the solutions
        for i in range(len(solution_lst)):
            new_sol_lst[i] = shuffle_sol(solution_lst[i])

        return new_sol_lst

    def solution_len(sol, g, start_end):
        """ Given an order of cities, return total distance of tour from start city
            through our cities back to origin"""
        total_dist = g.distance(start_end, sol[0])
        length = len(sol)
        # distance between each city in solution
        for i in (range(length - 1)):
            total_dist += g.distance(sol[i], sol[i + 1])
        # add distance between end of solution and initial city
        total_dist += g.distance(sol[length - 1], start_end)
        return total_dist

    def fitness(sol, g, initial):
        """ Fitness of a solution is the inverse of its distance"""
        return 1 /(solution_len(sol, g, initial))

    def best_sol(solution_lst, g, initial):
        """ Returns position of the best solution in the solution_lst"""
        best = 0
        for i in range(len(solution_lst) - 1):
            if solution_len(solution_lst[i], g, initial) < solution_len(solution_lst[best], g, initial):
                best = i
        return best

    def worst_sol(solution_lst, g, initial):
        # returns position in the array of the best solution in the array (solution_lst)
        worst = 0
        for i in range(len(solution_lst) - 1):
            if solution_len(solution_lst[i], g, initial) > solution_len(solution_lst[worst], g, initial):
                worst = i
        return worst

    def print_lengths(solution_lst, g, initial):
        #use for testing, mainly
        for i in solution_lst:
            print (solution_len(i), g, initial)
        return

    def weighted_random (solution_lst, g, initial):
        """ choose a solution with probability equal to the inverse of its distance (?)
            use in choose_parents to select "fit" parents"""
        sum = 0
        for i in solution_lst:
            sum += fitness(i, g, initial)
        r = random.uniform(0, sum)
        pos = 0
        for i in solution_lst:
            x = fitness(i, g, initial)
            if pos + x >= r:
                return i
            else:
                pos += x
        return # shouldn't get down to here because of how random and r are defined

    def choose_parents(solution_lst, g, initial):
        """ choose parents from solution list with probability based on their fitness
            returns tuple"""
        p1 = None
        p2 = None
        while p1 is p2:
            p1 = weighted_random(solution_lst, g, initial)
            p2 = weighted_random(solution_lst, g, initial)
        return (p1, p2)

    def get_rand(parentsol, child):
        """ given a parent solution and a child, finds a city in the parent that is
            not in the child, returns that city """
        r = 0
        while (parentsol[r] in child):
            r = random.randint(0, len(parentsol)-1)
        return parentsol[r]

    def crossover_OX(parents, cities):
        """ implements order crossover (OX) algorithm randomly picks an swath of "genes" in one parent and puts that in same location in child
            rest of child is comprised of other parent's genes

            start, end represent absolute positions in list not indices
            cities-2 as upper bound for start and start+1 as lower for end ensure swath is at least 1 long  """
        swath_start = random.randint(1, cities - 2)
        swath_end = random.randint(swath_start + 1, cities - 1)
        # take first parent in tuple as "donor" parent, doesn't matter since "first" was arbitrarily assigned
        donor = parents[0]
        nondonor = parents[1]
        swath = donor[swath_start - 1:swath_end]
        filtered = filter(lambda x: x not in swath, nondonor)

        child = filtered[:swath_start-1] + swath + filtered[swath_start - 1:]
        '''
        latter_length = len(donor) - swath_end
        # reorder to make it easier to concat afterwards
        reordered = nondonor[swath_end:] + nondonor[:swath_end]
        filtered = filter(lambda x: x not in swath, reordered)

        child = filtered[-swath_start:] + swath + filtered[:latter_length]
        '''
        
        return child

    def crossover_greedy(parents, cities):
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
            next1 = parents[0][(parents[0].index(x) + 1) % (cities - 1)]
            next2 = parents[1][(parents[1].index(x) + 1) % (cities - 1)]
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

    def mutation_random(solution_lst, g, initial):
        """ choose solution from solution_lst at random, preserve best solution
            should not change size of solution_lst
            elitism - i.e. don't mutate the solution with shortest path """
        x = 0
        while (solution_lst[x] == best_sol(solution_lst, g, initial)):
            x = random.randint(0, len(parentsol) - 1)
        # mutate solution by swapping two cities at random
        sol = solution_lst[x]
        r1 = random.randint(0, len(sol) - 1)
        r2 = random.randint(0, len(sol) - 1)
        sol[r1], sol[r2] = sol[r2], sol[r1]
        return solution_lst

    def mutation_hill(solution_lst, g, initial):
        """ choose solution from solution_lst at random, preserve best solution, remove
            the worst solution and replace it with a mutation of the best """
        bst = best_sol(solution_lst, g, initial)
        wst = worst_sol(solution_lst, g, initial)
        
        # replace the worst solution with the best
        solution_lst[wst] = solution_lst[bst]
        
        # mutate the copy solution by swapping two cities at random
        length = len(solution_lst[wst])
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        
        solution_lst[wst][r1], solution_lst[wst][r2] = solution_lst[wst][r2], solution_lst[wst][r1]
        return solution_lst

    def mutation_simulatedAnnealing(solution_lst, g, initial):
        """ choose solution from solution_lst at random, preserve best solution, remove
            the worst solution and replace it with a mutation of the best """
        bst = best_sol(solution_lst, g, initial)
        wst = worst_sol(solution_lst, g, initial)
        
        # replace the worst solution with the best
        solution_lst[wst] = solution_lst[bst]
        
        # mutate the copy solution by swapping two cities at random
        length = len(solution_lst[wst])
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        while r1 == r2:
            r1 = random.randint(0, length - 1)
            r2 = random.randint(0, length - 1)
        
        solution_lst[wst][r1], solution_lst[wst][r2] = solution_lst[wst][r2], solution_lst[wst][r1]
        return solution_lst

    def crossover(solution_lst, g, initial, cities):
        """ using helper functions, choose two parent solutions and crossover
            add child solution to solution_lst, increases size by one
            note - will add repeats"""
        child_pop = []
        child_pop.append(solution_lst[best_sol(solution_lst, g, initial)])

        # so that child population has the same number of solutions as the parent population
        for i in range(len(solution_lst) - 1):
            x = choose_parents(solution_lst, g, initial)
            a = crossover_OX(x, cities)
#            while a in child_pop:
#                x = choose_parents(solution_lst, g, initial)
#                a = crossover_greedy(x,cities)
#                a = crossover_OX(x, cities)
#                print "stalling ..."
            child_pop.append(a)
        return child_pop
        

    global gen_file
    gen_file = open('genetic.txt','a')

    if (cities < 3):
        return (locs, solution_len(locs, g, start_end))
    else:
        t1 = time.time()
        newsols = gen_population(cities, locs, sols)
        best = best_sol(newsols, g, start_end)
        for i in range(num):
            newsols = crossover(newsols, g, start_end, cities) # to change which crossover is used, go to def crossover itself
            r = random.randint(0,10)
            if r == 0:
                newsols = mutation_random(newsols, g, start_end)
#                newsols = mutation_hill(newsols, g, start_end)
#                newsols = mutation_simulatedAnnealing(newsols, g, start_end)
        best = best_sol(newsols, g, start_end)
        t2 = time.time()
        total_time = round(t2 - t1,3)

        # change which one is active depending on which mutation/crossover is run
#        gen_file.write("Time: " + str(total_time) + ". Genetic, random mutation, " + str(cities) + " cities, " + str(num) + " generations. \n")
#        gen_file.write("Time: " + str(total_time) + ". Genetic, hill mutation, " + str(cities) + " cities, " + str(num) + " generations. \n")
#        gen_file.write("Time: " + str(total_time) + ". Genetic, SA mutation, " + str(cities) + " cities, " + str(num) + " generations. \n")


        gen_file.write("Time: " + str(total_time) + ". Genetic, OX crossover, " + str(cities) + " cities, " + str(num) + " generations. \n")
#        gen_file.write("Time: " + str(total_time) + ". Genetic, greedy crossover, " + str(cities) + " cities, " + str(num) + " generations. \n")

        gen_file.close()
        return (newsols[best], solution_len(newsols[best],g,start_end))
