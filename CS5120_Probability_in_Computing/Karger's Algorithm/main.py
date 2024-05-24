import numpy as np

def karger(d , n):
    '''
    Implements the Karger Algorithm for finding the minimum cut in a graph.

    Parameters:
        d (dict): A dictionary containing the pairs of vertices as keys and the number of edges between them as values.
        n (int): The number of vertices in the graph.

    Returns:
        d (dict): Consisting of the final 2 clusters and the minimum cut between them
    '''

    # We run the loop till we have only 2 clusters left
    while(n > 2):
        
        # we create the probability distribution to choose the groups of vertices we wish to merge
        vals = []
        for v in d.values():
            vals.append(v)
        vals = np.array(vals)
        c = np.random.choice(np.arange(0 , len(d) , dtype = np.int64) , 1 , p = vals / vals.sum())

        # we obtain the vertices to be merged, and remove it from the dictionary
        to_be_merged = list(d)[c[0]]
        del d[to_be_merged]

        # extras will store all the keys that have one of the vertices to be merged in them. This will be used to delete them later
        extras = []

        # extra_d will hold the new number of edges between the newly merged nodes and other vertices/nodes
        extra_d = {}

        # we iterate over all the keys in the dictionary
        for k in d.keys():
            
            # if k has already been seen and accounted for, we continue
            if k in extras:
                continue

            # if either of the group to be merged is present in the key, we take it into account
            if to_be_merged[0] in k:
                extras.append(k)
                total = d[k]
                other_vertex = k[0] if k[0] != to_be_merged[0] else k[1]

                # we look for the possibility of the other group sharing edges with other_vertex
                possibility1 = (to_be_merged[1] , other_vertex)
                possibility2 = (other_vertex , to_be_merged[1])

                if possibility1 in d:
                    total += d[possibility1]
                    extras.append(possibility1)
                elif possibility2 in d:
                    total += d[possibility2]
                    extras.append(possibility2)
                
                extra_d[(to_be_merged , other_vertex)] = total

            elif to_be_merged[1] in k:
                extras.append(k)
                total = d[k]
                other_vertex = k[0] if k[0] != to_be_merged[1] else k[1]

                # we look for the possibility of the other group sharing edges with other_vertex
                possibility1 = (to_be_merged[0] , other_vertex)
                possibility2 = (other_vertex , to_be_merged[0])

                if possibility1 in d:
                    total += d[possibility1]
                    extras.append(possibility1)
                elif possibility2 in d:
                    total += d[possibility2]
                    extras.append(possibility2)
                
                extra_d[(to_be_merged , other_vertex)] = total

        # we now delete the extra keys we have in dictionary
        for e in extras:
            if e in d.keys():
                del d[e]

        # we merge our original dictionary and the extra dictionary
        d = d | extra_d
        
        # decrementing n
        n -= 1
    return d

def tuple_to_cut(t , store):
    ''' 
    This converts the multiple nested tuples into a list. 
    This function is necessary because we might have a tuple or integer

    Parameters:
        t (tuple or int): The tuple to be converted
        store (list): The list to store the values in

    Returns:
        store (list): The list containing the values
    '''

    # if t is an integer we cannot iterate over it
    if type(t) == int:      
        store.append(t)
        return store
    for i in t:
        if type(i) == int:
            store.append(i)
        else:
            # we recursively call this function
            tuple_to_cut(i , store) 
    return store



# DRIVER CODE
if __name__ == "__main__":
    
    ##### REPLACE ACCORDINGLY
    input_file = "/Users/tanmaygoyal/Desktop/Assignments and Events/Probability in Computing/Karger's Algorithm/graph1.txt"
    ##### REPLACE ACCORDINGLY

    # reading the input file and getting our data
    data = []
    with open(input_file , 'r') as f:
        for line in f.readlines():
            if line[-1] == '\n':
                line = line[:-1]
            data.append(line.split(' '))

    # storing the number of vertices
    n = int(data[0][0])

    # creating the dictionary
    # WLOG, we assume the first member of pair < second member of pair
    d = {}
    for i in range(2 , len(data)):
        v1 = int(data[i][0])
        v2 = int(data[i][1])
        pair = (min(v1 , v2) , max(v1 , v2))

        if pair not in d:
            d[pair] = 1
        else:
            d[pair] += 1

    # we define the min_cut and the minimum groups
    min_cut = np.inf
    min_grp1 = None
    min_grp2 = None

    # we run the algorithm O(n^2) times to boost the correctness
    for iter in range(n * n // 2):

        # running the karger algorithm
        dic = karger(d.copy() , n)

        # we obtain the minimum cut size
        cut_size = dic[list(dic)[0]]

        if cut_size < min_cut:
            min_cut = cut_size
            grp1 = []
            grp2 = []
            # we obtain the list versions of the cut
            grp1 = tuple_to_cut(list(dic)[0][0] , grp1)
            grp2 = tuple_to_cut(list(dic)[0][1] , grp2)
            min_grp1 = grp1
            min_grp2 = grp2

    # printing the final results
    # for ease of reading, we shall sort the groups
    min_grp1.sort()
    min_grp2.sort()
    print("Minimum cut size: " , min_cut)
    print("Group 1: " , min_grp1)
    print("Group 2: " , min_grp2)