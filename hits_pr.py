import sys
import tracemalloc
import time


def calculate_inoutDegree(file):
    inlink = dict()
    outlink = dict()
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
        
        if link[0] in outlink:
            outlink[link[0]].append(link[1])
        else:
            outlink[link[0]] = [link[1]]
    return inlink, outlink, node_num

def HITS_calculate_and_normalization(auth, hub, inlink, outlink, node_num):
    tmp_hub = hub.copy()
    tmp_auth = auth.copy()

    for j in range(1, node_num+1):
        tmp_a = 0
        tmp_h = 0

        if str(j) in inlink:
            for k in inlink[str(j)]:
                tmp_a = tmp_a + tmp_hub[k]
        if str(j) in outlink:
            for k in outlink[str(j)]:
                tmp_h = tmp_h + tmp_auth[k]
        auth[str(j)] = tmp_a
        hub[str(j)] = tmp_h

    total_h = 0
    total_a = 0
    for j in range(1, node_num+1):
        total_a = total_a + auth[str(j)]
        total_h = total_h + hub[str(j)]
    for j in range(1, node_num+1):
        auth[str(j)] = auth[str(j)] / total_a
        hub[str(j)] = hub[str(j)] / total_h

    delta = 0
    for j in range(1, node_num+1):
        delta = delta + abs(auth[str(j)] - tmp_auth[str(j)])
        delta = delta + abs(hub[str(j)] - tmp_hub[str(j)])

    return auth, hub, delta

def HITS(inlink, outlink, node_num, delta_limit):
    auth = dict()
    hub = dict()

    # auth value and hub value initial 
    for i in range(1, node_num+1):
        auth[str(i)] = 1
        hub[str(i)] = 1

    delta = 10
    iterate_num = 0
    while delta > delta_limit: # iterate
        # calculate auth and hub, then normalize
        auth, hub, delta = HITS_calculate_and_normalization(auth, hub, inlink, outlink, node_num)
        iterate_num += 1
        
    return auth, hub, iterate_num      

def PR_calculate_and_normalization(pr, inlink, outlink, node_num):
    tmp_pr = pr.copy()

    for j in range(1, node_num+1):
        tmp_pr_value = 0

        if str(j) in inlink:
            for k in inlink[str(j)]:
                if k not in outlink: # if no outlink
                    tmp_pr_value = tmp_pr_value + (tmp_pr[k] / node_num)
                else:
                    tmp_pr_value = tmp_pr_value + (tmp_pr[k] / len(outlink[k]))
        
        pr[str(j)] = 0.15 / node_num + 0.85 * tmp_pr_value

    total_pr = 0
    for j in range(1, node_num+1):
        total_pr = total_pr + pr[str(j)]
    for j in range(1, node_num+1):
        pr[str(j)] = pr[str(j)] / total_pr

    delta = 0
    for j in range(1, node_num+1):
        delta = delta + abs(pr[str(j)] - tmp_pr[str(j)])

    return pr, delta

def PR(inlink, outlink, node_num, delta_limit): 
    pr = dict() 

    # pr value initial 
    for i in range(1, node_num+1):
        pr[str(i)] = 1 / node_num

    delta = 10
    iterate_num = 0
    while delta > delta_limit: # iterate
        # calculate auth and hub, then normalize
        pr, delta = PR_calculate_and_normalization(pr, inlink, outlink, node_num)
        iterate_num += 1

    return pr, iterate_num 

if __name__ == '__main__':
    f = open(sys.argv[1], "r")
    # calculate indegree and outdegree
    inlink, outlink, node_num = calculate_inoutDegree(f)
    
    #tracemalloc.start()
    #start_time = time.time()
    
    a, h, hits_iter_num = HITS(inlink, outlink, node_num, float(sys.argv[2]))
    p, pr_iter_num = PR(inlink, outlink, node_num, float(sys.argv[2]))
    
    #print(tracemalloc.get_traced_memory())
    #print("--- %s seconds ---" % (time.time() - start_time))

    
    print('HITS algorithm iterate %d times:' % hits_iter_num)
    print('node\tauthority\thub')
    for i in range(1, node_num+1):
        print('%d\t%.5f\t\t%.5f' % (i, a[str(i)], h[str(i)]))
        
    print('\nPageRank algorithm iterate %d times:' % pr_iter_num)
    print('node\tpageRank')
    for i in range(1, node_num+1):
        print('%d\t%.5f' % (i, p[str(i)])) 
