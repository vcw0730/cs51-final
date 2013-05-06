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

        for i in range(len(new_sol_lst)):
            assert new_sol_lst[i] != None

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
        assert total_dist > 0
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
        """ returns position of the worst solution in the solution_lst"""
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
        """ assigns segment of sum proportional to fitness for each individual,
            the better the fitness the larger the segment of the sum that
            corresponds to it and thus the more likely it is to be chosen at random
    
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
        """ choose parents from solution list with probability based on fitness
            returns tuple"""
        p1 = None
        p2 = None
        while p1 is p2:
            p1 = weighted_random(solution_lst, g, initial)
            p2 = weighted_random(solution_lst, g, initial)
        assert p1 != None
        assert p2 != None
        return (p1, p2)

    def get_rand(parentsol, child):
        """ given a parent solution and a child, finds a city in the parent that is
            not in the child, returns that city """
        r = 0
        while (parentsol[r] in child):
            r = random.randint(0, len(parentsol)-1)
        return parentsol[r]

    def crossover_OX(parents, cities):
        """ implements order crossover (OX) algorithm:
            randomly picks an swath of "alleles" in one parent and puts that
            in same location in child, rest of child is comprised of other parent's
            alleles, starting from end of swath and looping back around
            
            start, end represent indices in list, so go from 0 to length-1
            cities-2 as upper bound for start and start+1 as lower for end ensure
            swath is at least 1 long

            produces 1 child at a time for any 2 given parents """
        
        swath_start = random.randint(0, cities - 3)
        swath_end = random.randint(swath_start + 1, cities - 2)
        # take first parent in tuple as "donor" parent, doesn't matter since "first" was arbitrarily assigned
        donor = parents[0]
        nondonor = parents[1]
        swath = donor[swath_start:swath_end]
        
        rest_length = len(donor) - swath_end
        # reorder to make it easier to concat afterwards
        reordered = nondonor[swath_end:] + nondonor[:swath_end]
        filtered = filter(lambda x: x not in swath, reordered)

        child = filtered[:swath_start] + swath + filtered[-rest_length:]
        assert len(child) == len(donor)
        
        return child

    def crossover_PMX(parents,cities):
        """ partially matched crossover algorithm:
            splice in random swath from donor parent into child, add in non-conflicting
            alleles from nondonor in same absolute positions, then use procedure to
            fill remaining positions in child with conflict """
        
        swath_start = random.randint(0, cities - 3)
        swath_end = random.randint(swath_start + 1, cities - 2)
        donor = parents[0]
        nondonor = parents[1]
        swath1 = donor[swath_start:swath_end]
        swath2 = nondonor[swath_start:swath_end]

        child = [None]*len(donor)
        # splice swath from donor into child, put everything else as nondonor
        for i in range(len(child)):
            if i >= swath_start and i < swath_end:
                child[i] = donor[i]
            else:
                child[i] = nondonor[i]

        # eliminate repeats by checking the values in swath, swap out ones that appear
        # elsewhere with corresponding value in same index in other basically
        for i in range(len(child)):
            if i >= swath_start and i < swath_end:
                for j in range(len(child)):
                    if child[j] == child[i] and j != i:
                        y = nondonor[i]
                        while y in swath1:
                            y = nondonor[donor.index(y)]
                        child[j] = y

        """
        # insert non-conflicting alleles from nondonor into child
        for i in nondonor:
            if (i not in swath1) and (i not in swath2):
                child[nondonor.index(i)] = i

        def cross_value(donor, nondonor, ind):
            match = nondonor[ind]
            donor_index = donor.index(match)
            x = nondonor[donor_index]
            return x


        # fill in rest of child
        for i in range(len(child)):
            if child[i] == None:
                x = cross_value(donor, nondonor, i)
                x1 = x
                while x in swath1 or x in swath2:
                    x = cross_value(donor, nondonor, x[2])
                    print x, child
                assert x not in child
                child[i] = x
        """

        return child

    def apply_hillclimb(solution, start_end, iterations):
        best = solution
        best_distance = solution_len(best, g, start_end)
        while (iterations > 0):
            temp = best
            r1 = random.randint(0, len(temp) - 1)
            r2 = random.randint(0, len(temp) - 1)
            temp[r1], temp[r2] = temp[r2], temp[r1]
            distance = solution_len(temp, g, start_end)
            if distance < best_distance:
                best = temp
                best_distance = distance
            iterations -= 1
        return best
        
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
        assert len(child) == len(parents[2])
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

    def crossover(solution_lst, g, initial, cities, choice):
        """ using helper functions, choose two parent solutions and crossover
            add child solution to solution_lst, increases size by one
            note - will add repeats"""
        child_pop = []
        child_pop.append(solution_lst[best_sol(solution_lst, g, initial)])

        # so that child population has the same number of solutions as the parent population
        for i in range(len(solution_lst) - 1):
            x = choose_parents(solution_lst, g, initial)
            if choice == 3:
                a = crossover_greedy(x, cities)
            elif choice == 2:
                a = crossover_PMX(x, cities)
            else: 
                a = crossover_OX(x, cities)
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
        iterations = 10
        cross_choice = int(raw_input("Which crossover would you like to use? \n 1: OX (default) \n 2: PMX \n 3: greedy \n --> "))
        mut_choice = int(raw_input("Which mutation would you like to use? \n 1: random (default) \n 2: hill \n --> "))
        hill_choice = int(raw_input("Would you like to run hill climbing on each population? \n 1: yes \n 2: no (default) \n --> "))
        for i in range(num):
            newsols = crossover(newsols, g, start_end, cities, cross_choice) 
            r = random.randint(0, 10)
            if r == 0:
                if mut_choice == 2:
                    newsols = mutation_hill(newsols, g, start_end)
                else:
                    newsols = mutation_random(newsols, g, start_end)
            if hill_choice == 1:
                for each in range(len(newsols)):
                   newsols[each] = apply_hillclimb(newsols[each], start_end, iterations)
                
        best = best_sol(newsols, g, start_end)
        t2 = time.time()
        total_time = round(t2 - t1,3)

        # change which one is active depending on which mutation/crossover is run

        cross_name = None
        mut_name = None
        hill_enabled = None

        if cross_choice == 3:
            cross_name = "greedy"
        elif cross_choice == 2:
            cross_name = "PMX"
        else:
            cross_name = "OX"

        if mut_choice == 2:
            mut_name = "hill"
        else:
            mut_name = "random"

        if hill_choice == 1:
            hill_enabled = "enabled"
        else:
            hill_enabled = "disabled"
        
        gen_file.write("Time: " + str(total_time) + ". Genetic, " + cross_name + " crossover, " + mut_name + " mutation, with hill climbing " + hill_enabled + " on " + str(cities) + " cities, " + str(num) + " generations. \n")

        gen_file.close()
        return (newsols[best], solution_len(newsols[best],g,start_end))
