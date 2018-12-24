import sys

def calculate_inDegree(file):
    inlink = dict()
    node_num = 1

    for line in file:
        link = line.rstrip().split(',')
        if int(link[0]) > node_num:
            node_num = int(link[0])
        if int(link[1]) > node_num:
            node_num = int(link[1]) 

        if link[1] in inlink:
            inlink[link[1]].append(link[0])
        else:
            inlink[link[1]] = [link[0]]
        
    return inlink, node_num

def calculate_simrank(node_a, node_b, inlink, sim_inuse, c):
    if node_a == node_b:
        return 1
    elif (node_a not in inlink) or (node_b not in inlink):
        return 0
    else: 
        if frozenset({node_a, node_b}) in sim_inuse['used']: # if there is cycle between two nodes 
            sim_inuse['cycle'] = True
            return 0
        else:
            sim_inuse['used'].append(frozenset({node_a, node_b}))

        a_length = len(inlink[node_a])
        b_length = len(inlink[node_b])
        simrank = 0

        for i in inlink[node_a]:
            for j in inlink[node_b]:
                simrank = simrank + calculate_simrank(i, j, inlink, sim_inuse, c)

        return (c / (a_length * b_length)) * simrank

if __name__ == '__main__':
    f = open(sys.argv[1], "r")
    # calculate indegree and outdegree
    inlink, node_num = calculate_inDegree(f)

    print('pair-wise similarity of nodes:')
    print('nodes\tsimrank')
    for i in range(1, node_num+1):
        for j in range(1, node_num+1):
            if i != j:
                sim_inuse = dict()
                sim_inuse['used'] = list()
                sim_inuse['cycle'] = False

                s = calculate_simrank(str(i), str(j), inlink, sim_inuse, 0.8)
                if sim_inuse['cycle']:
                    print('(%d, %d)\tcycle' % (i, j))
                else:
                    print('(%d, %d)\t%.4f' % (i, j, s))
