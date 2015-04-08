__author__ = '형헌'


import math, random, csv, networkx as nx, operator
graph = nx.Graph()
reader = csv.reader(open('polblogs.csv', 'r'), delimiter=',')

data = [row for row in reader]
nodes = set([row[0] for row in data])
edges = [(row[0], row[2]) for row in data]
num_nodes = len(nodes)
rank = 1/float(num_nodes)
graph.add_nodes_from(nodes, rank=rank)
graph.add_edges_from(edges)

# Assign initial values
V = float(len(graph))
s = 0.85
ranks = dict()
for key, node in graph.nodes(data=True):
    ranks[key] = node.get('rank')

# Calculating PageRanks
for _ in range(10):
    for key, node in graph.nodes(data=True):
        rank_sum = 0.0
        curr_rank = node.get('rank')
        neighbors = graph[key]
        for n in neighbors: # for each neighbors, gather its pagerank
            if ranks[n] is not None:
                outlinks = len(graph.neighbors(n))
                rank_sum += (1 / float(outlinks)) * ranks[n]
        ranks[key] = ((1 - s) * (1/V)) + s*rank_sum
sorted_ranks = sorted(ranks.iteritems(), key=operator.itemgetter(1), reverse=True)

for tuple in sorted_ranks: # print out the results
    print tuple[0], tuple[1]