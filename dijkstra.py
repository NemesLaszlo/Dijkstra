import sys
import json
from heapdict import heapdict

def load_graph(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def create_adj(links_list):
    adj = {}
    for i in range(len(links_list)):
        nodes = links_list[i]['points']
        u = nodes[0]
        v = nodes[1]
        w = links_list[i]['weight']
        if u not in adj:
            adj[u] = []
            adj[u].append((v, w))
        else:
            adj[u].append((v, w))

        if v not in adj:
            adj[v] = []
            adj[v].append((u, w))
        else:
            adj[v].append((u, w))
            
    return adj


def initialization(s, adj):
    E = []
    ready = {}
    pred = {}
    d = {}
    Q = heapdict()
    
    ready[s] = True
    d[s] = 0
    
    for v in adj:
        if v != s:
            ready[v] = False
            d[v] = sys.maxsize

    s_adj = adj.get(s)

    for v in s_adj:
        pred[v[0]] = s
        d[v[0]] = v[1]
        Q[v[0]] = d[v[0]]
        
    return E, ready, pred, d, Q


def dijkstra(E, ready, pred, d, Q, adj):
    it = 1
    while len(Q) > 0:
        print("Iteration: " + str(it))
        v = Q.popitem()
        E.append((pred[v[0]], v[0]))
        print "E: " + str(E)
        ready[v[0]] = True

        v_adj = adj.get(v[0])

        for u in v_adj:
            if u[0] in Q and d[v[0]] + u[1] < d[u[0]]:
                pred[u[0]] = v[0]
                d[u[0]] = d[v[0]] + u[1]
                Q[u[0]] = d[u[0]]
            elif u[0] not in Q and not ready[u[0]]:
                pred[u[0]] = v[0]
                d[u[0]] = d[v[0]] + u[1]
                Q[u[0]] = d[u[0]]
        
        for n in sorted(adj):
            print "d("+n[0]+"): " + str(d[n[0]]),
        print "\n"
        it = it + 1


data = load_graph('graph.json')
adj = create_adj(data['links'])
E, ready, pred, d, Q = initialization(data['start-point'], adj)
dijkstra(E, ready, pred, d, Q, adj)
