from heap_binary import *
from graph_dictionary import *

def greedy (g, start_end, locs):
    """ greedy applies the greedy algorithm by taking the shortest
        edge coming out of each vertex
        parameters g: graph, start_end: start vertex, locs = vertices
        returns tuple (tour, distance) """

    # not_used: stores unused vertices
    # result: stores subtours
    not_used = []
    result = []

    # number of cities
    num_vertices = len(locs)

    # add all vertices into unused
    for each in locs:
        not_used.append(each)

    
    def next_vertex (g, location, not_used, temp):
        """ Given the graph and the current location, find the
            shortest edge to an unused vertex """
        dist = float("inf")
        for elem in not_used:
            if g.graph[loc][elem] < dist:
                temp = elem
                dist = g.graph[loc][elem]
        return dist, temp

    # location stores our current location
    # tracks total distance
    location = start_end
    total_dist = 0

    # traverse through graph and find next closest vertex until reaches tour
    while len(not_used) != 0:
        temp = None
        distance, elem = next_vertex (g, location, not_used, temp)
        result.append(elem)
        total_dist += distance
        not_used.remove(elem)
        location = elem
        
    # add path returning to start
    total_dist += g.graph[location][start_end]
    
    return result, total_dist
