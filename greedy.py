from heap_binary import *

def greedy (G):
  
    not_used = []
    result = []
    
    # vertices is an array of our vertices
    # num_vertices is the number of vertices we have
    vertices = G.graph.keys()
    num_vertices = len(vertices)
    
    for each in vertices:
            not_used.append(each)
      
    # our start
    start = not_used[0]
    print "Your start city is ", start
    result.append(not_used.pop(0))
    total_dist = 0
      
    def next_vertex (G, start, not_used, temp):
            dist = float("inf")
            for elem in not_used:
                if G.graph[start][elem] < dist:
                    temp = elem
                    dist = G.graph[start][elem]
            return dist, temp
    
    while len(not_used) != 1:
            temp = None
            distance, elem = next_vertex (G, start, not_used, temp)
            result.append(elem)
            total_dist += distance
            not_used.remove(elem)
            result.append(not_used[0])
    
      
    return result, total_dist
