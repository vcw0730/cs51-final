from graph_dictionary import *
from user_interface import *

# main body
def main():
    print("Initializing...")

    # distances for each algorithm
    # solution for each algorithm
    dist = [None, None, None]
    solutions = [[],[],[]]

    # e_file to store efficiency for analysis
    e_file = open('efficiency.txt','a')

    # prompts for number of cities
    cities = int(raw_input("How many cities would you like to visit? Please only use integers. "))
    while (cities < 2):
        cities = int(raw_input("Please choose a number greater than 1! "))

    # generate_graphs
    g, locs, start_end = generate_graph(cities)

    # empty solution_set, distance_set, time_set
    solution_set = [[], [], []]
    distance_set = [[], [], []]
    time_set = [[], [], []]

    # prompt for algorithm to run
    choose_option(g, start_end, locs, cities, e_file, solution_set, distance_set, time_set)
    

if __name__ == "__main__":
    main()
