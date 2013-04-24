def all_pairs_shortest_path(G):
    # shortest path from i->j has to go through intermediate nodes
    # are restricted from 1 to k
    
    # For a subset of cities S : {1,2...n} that includes 1, and j is in S, let C(S,j) be the
    # length of the shortest path visiting each node in S exactly once, starting at 1 and
    # ending at j.
    
    # Let's express C(S,j) in terms of smaller subproblems: We need to start at 1 and end at j:
    #  so what should we pick as the second-to-last city? It has to be some i in S such that the
    #  overall path length is the distance from 1->i, namely C(S-{j}, i), plus the length of the final edge d_ij
    #  We must pick the best such i: C(S,j) = min (i in S, i!= j) : C(S-{j}, i) + d_ij
    
    # D[] is where we will be storing the shortest distances from 1 -> i
    D = []
    
    # vertices is an array of our vertices
    # num_vertices is the number of vertices we have
    vertices = G.graph.keys()
    start = vertices.pop()
    
    num_vertices = len(vertices)
    
    # building our storage array of n * 2^n entries:
    # one for each pair of set and city
    # we append inf for each C(S, 1) because we can't end at
    # city 1 after going through a series of cities
    for city in range(1, num_vertices + 1):
        D.append([])
        for subsets in range(1, 2**num_vertices + 1):
            if ((subsets % (2**city)) < (2**(city - 1))):
                D[city - 1].append(float("inf"))
            elif subsets == (2**(city - 1)):
                D[city - 1].append(G.graph[start][vertices[city - 1]])
            else:
                D[city - 1].append(None)
    			

    # print D
    # The subset will be represented by its representation in binary - 1
    # imagine a set of 3 cities, then:
    # index 0 (+1 = 1)-> 001 (city 1)
    # index 1 (+1 = 2)-> 010 (city 2)
    # index 2 (+1 = 3)-> 011 (city 1 and 2)
    # index 3 (+1 = 4)-> 100 (city 3)
    # index 4 (+1 = 5)-> 101 (city 1 and 3)
    # index 5 (+1 = 6)-> 110 (city 2 and 3)
    # index 6 (+1 = 7)-> 111 (city 1, 2, 3)
    # index 7 (+1 = 8)-> 1000 (city 4)

    def dec_to_bin (dec):
        return int(bin(dec)[2:])

    def find_cities(b):
        res = []
        a = 0
        while (b > 0):
            if b % (10) == 1:
                res.append(a)
            a += 1
            b /= 10
        return res
	
    # recursively fills up array
    # C(S, j) = min[C(S-{j}, k) d_kj]
    def tsp (D, G, vertices, num_vertices):
        for subset_size in range (2, num_vertices + 1):    # size of subset
            for subsets_dec in range (3, 2**num_vertices): # the subset (col)
                subsets_bin = dec_to_bin(subsets_dec)          # converts subset to binary rep
                cities = find_cities(subsets_bin)          # list of tens places that are "1"
                ones = len(cities)                         # number of tens pl aces that are "1"
                if ones == subset_size:
                    for j in cities:                       # for each j in C(S, j)
                        subvalue = subsets_bin - (10**j)                       # determine what the binary rep without j is
                        remaining_cities = find_cities(subvalue)   # determine which cities are left 
                        best_k = (None, float("inf"))                          # accumulator
                        for k in remaining_cities:                             # for each k in C(S-{j}, k)
                            dist = D[k][int(str(subvalue), 2) - 1] + G.graph[vertices[k]][vertices[j]]
                            if dist < best_k[1]:
                                best_k = (k, dist)
                        D[j][subsets_dec - 1] = best_k[1]
        #print D
        return D

    a = tsp(D, G, vertices, num_vertices)
    return a
