import random
from graph_dictionary import *

cities = int(input("How many cities to travel? "))
max_distance = 150 # max distance between two cities, technically square root of 2(100^2)
max_sol_len = cities * max_distance
max_ants = cities

home_graph = Graph(cities)
locs_lst = home_graph.points
pher_matrix = [[(1.0/cities) for _ in range(cities)] for _ in range(cities)]
evap = 0.5
wd = 5 # how we weight distance vs. pheromones (distance ^ 5)
pher_val = 100 # constant used to calculate pheromone deposited

class Ant(object):

    current_loc = None # coordinates of current city
    next_loc = None
    path = [0] * cities # solution that will be returned
    current_step = 0 # how many cities the ant has traveled to
    dist_traveled = 0.0 # length of the path, calculate only when current_step = cities

    # initialize ants with the position of the starting city
    def __init__ (self, initial_city):
        assert initial_city in locs_lst
        self.current_loc = initial_city
        self.path = [0] * cities
        self.path[0] = initial_city
        assert self.path[0] == initial_city
        self.current_step += 1

    def update_dist (self):
        assert self.current_step == cities
        for i in range(len(self.path) - 2):
            self.dist_traveled += Graph.distance(home_graph,self.path[i],self.path[i+1])
        self.dist_traveled += Graph.distance(home_graph, self.path[len(self.path)-1],self.path[0])
        return self.dist_traveled

    # updates amount of ant pheromone on edge between locs_lst[a] and locs_lst[b]
    # only used by ant with best path
    def deposit_ant_pher(self):
        assert self.dist_traveled > 0
        assert len(self.path) == cities
        for i in range(len(self.path)-1):
            x = locs_lst.index(self.path[i])
            y = locs_lst.index(self.path[i+1])
            pher_matrix[x][y] += (pher_val / self.dist_traveled)
            pher_matrix[y][x] = pher_matrix[x][y]
        x = locs_lst.index(self.path[0])
        y = locs_lst.index(self.path[cities-1])
        pher_matrix[x][y] = (pher_val/self.dist_traveled)
        pher_matrix[y][x] = pher_matrix[0][cities-1]
        return 

    # run to evaporate pheromones
    def evaporate_pher(self):
        for a in range(cities):
            for b in range(cities):
                pher_matrix[a][b] = evap * pher_matrix[a][b]
        return

    # generate list of probabilities of going to each city in possible from curr (index)
    def gen_prob(self, curr, possible):
        assert curr > -1 and curr < cities
        if len(possible) > 1:
            prob_lst = [0] * len(possible)
            denom = 0.0
            for i in range(len(possible)):
                denom += pher_matrix[curr][i] * (Graph.distance(home_graph,locs_lst[curr],locs_lst[i]) ** wd)
            if denom == 0.0:
                return [0.0]
            for i in range(len(prob_lst)):
                prob_lst[i] = (pher_matrix[curr][i] * (Graph.distance(home_graph,locs_lst[curr],locs_lst[i]) ** 5)/ denom)
        return [0.0]

    def choose_city(self, lst):
        sum = 0
        for i in lst:
            sum += i
        r = random.uniform(0,sum)
        pos = 0
        for i in range(len(lst)):
            if pos + lst[i] >= r:
                return i
            else:
                pos += lst[i]

    def to_next_city (self):
        possible_locs = list(filter(lambda x: x not in self.path,locs_lst))
        if len(possible_locs) > 0:
            prob = self.gen_prob(locs_lst.index(self.current_loc), possible_locs)
            move_to = possible_locs[self.choose_city(prob)]
            self.path[self.current_step] = move_to
            self.current_loc = move_to
            self.current_step += 1
            return
        else:
            return self.path
   

    

