from graph_dictionary import *

def tsp_dynamic(g, start, num_vertices, vertices):
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
    
    # building our storage array of n * 2^n entries:
    # one for each pair of set and city
    # we append inf for each C(S, 1) because we can't end at
    # city 1 after going through a series of cities
    
    for city in range(1, num_vertices + 1):
        D.append([])
        for subsets in range(1, 2**num_vertices):
            if ((subsets % (2**city)) < (2**(city - 1))):
                D[city - 1].append((float("inf"), None))
            elif subsets == (2**(city - 1)):
                D[city - 1].append((g.graph[start][vertices[city - 1]], 0))
            else:
                D[city - 1].append((None, None))
    
    def dec_to_bin (dec):
        """
        Usage: dec_to_bin(decimal)
        Returns the binary representation of a decimal number
        """
        return int(bin(dec)[2:])

    # finds the locations 
    def find_cities(b):
        """
        Usage: find_cities(binary)
        Finds cities by finding locations of all "1"s.
        Returns int list
        """
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
    # The subset will be represented by its representation in binary - 1
    # imagine a set of 3 cities, then:
    # index 0 (+1 = 1)-> 001 (city 1)
    # index 1 (+1 = 2)-> 010 (city 2)
    # index 2 (+1 = 3)-> 011 (city 1 and 2)
    # index 3 (+1 = 4)-> 100 (city 3)
    # index 4 (+1 = 5)-> 101 (city 1 and 3)
    # index 5 (+1 = 6)-> 110 (city 2 and 3)
    # index 6 (+1 = 7)-> 111 (city 1, 2, 3)
    def tsp (D, g, vertices, num_vertices, start):
        # total number of subsets
        total_num_subsets = 2**num_vertices
        # for each size of subset
        for subset_size in range (2, num_vertices + 1):
            # for each subsets of a specific size
            for subsets_dec in range (3, total_num_subsets): 
                subsets_bin = dec_to_bin(subsets_dec)      # converts subset to binary rep
                cities = find_cities(subsets_bin)          # list of tens places that are "1"
                ones = len(cities)                         # number of tens pl aces that are "1"
                if ones == subset_size:
                    for j in cities:                       # for each j in C(S, j)
                        subvalue = subsets_bin - (10**j)                       # determine what the binary rep without j is
                        remaining_cities = find_cities(subvalue)   # determine which cities are left 
                        best_k = (float("inf"), None)                          # accumulator
                        for k in remaining_cities:                             # for each k in C(S-{j}, k) 
                            dist = D[k][int(str(subvalue), 2) - 1][0] + g.graph[vertices[k]][vertices[j]]
                            if dist < best_k[0]:
                                best_k = (dist, (k, int(str(subvalue), 2) - 1))
                        D[j][subsets_dec - 1] = best_k

        # lowest tour distance
        lowest = float("inf")
        # find at which city the tour ends
        end_pt = None
        total = None
        
        for final in range (0, num_vertices):
            total_dist = D[final][total_num_subsets - 2][0] + g.graph[vertices[final]][start]
            if (total_dist) < lowest:
                end_pt, total = (final, total_num_subsets - 2), total_dist


        final = []    
        while (end_pt != 0):
            final.insert(0, vertices[end_pt[0]])
            end_pt = D[end_pt[0]][end_pt[1]][1]
            # print final
        #final.insert(0, start)
        
        return final, total
        
    return tsp(D, g, vertices, num_vertices, start)
    
 
