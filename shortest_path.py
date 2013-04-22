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
    num_vertices = len(vertices)
    
    # building our storage array of n * 2^n entries:
    # one for each pair of set and city
    for city in range(num_vertices): 
      D.append([])
        for subsets in range(2**num_vertices):
	  if city == 0:
	    D[city].append(float("inf"))
	  elif city == subsets
	  D[city].append(False)
    
    for each in num_vertices:
      D
      
    if k == 0:
        D[0][i][j] = dij if graph[i][j] else 99999999      
        
    for k = 1 to n:p
        for i = 1 to n:
            for j = 1 to n:   
       
                # possibly D[k][i][j] = D[k-1][i][j] if I don't need to use vertex k
                # possibly D[k][i][j] = D[k-1][i][k] + D[k-1][k][j] if k is on the path
                D[k][i][j] = min (D[k-1][i][j], D[k-1][i][k] + D[k-1][k][j])
