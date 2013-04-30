from tsp_ants import *

def main():
    run = int(input("How many times should this simulation run? "))

    best_sol = []
    best_dist = max_sol_len
    ants = [None] * max_ants
    best_ant = 0 #position in ants of ant with best path

    for j in range(run):
        start = locs_lst[0]
#        print("Round",j+1)
        for i in range(len(ants)):
            ants[i] = Ant(start)
#            print ("Ant",i,"running...")
            curr_ant = ants[i]
            for k in range(cities):
                curr_ant.to_next_city()
            length = curr_ant.update_dist()
            if length < best_dist:
                best_ant = i
                best_sol = curr_ant.path
                best_dist = length
        ants[0].evaporate_pher() # since it doesn't matter which ant calls it
        ants[best_ant].deposit_ant_pher()

    print("Best solution found:",best_sol)
    print("Total distance:",best_dist)
    return best_sol

main()
