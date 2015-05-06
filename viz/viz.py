# coding=UTF-8

import networkx as nx

from networkx.readwrite import json_graph
graph = nx.Graph()

##
# Ranking node with page rank algorithm
#
# @param graph the graph to be page-ranked
# @param k the steps
# @return the ranking dictionary
#
def rank_nodes(graph, k=10):
    # Assign initial values
    ranks = dict()
    V = float(len(graph))
    s = 0.85

    for key, node in graph.nodes(data=True):
        ranks[key] = node.get('rank')

    for _ in range(k):
        for key, node in graph.nodes(data=True):
            rank_sum = 0.0
            curr_rank = node.get('rank')
            #print curr_rank

            neighbors = graph[key]
            for n in neighbors: # for each neighbors, gather its pagerank
                if graph.node[n].has_key('rank'):
                    if graph.node[n]['rank'] is not None:
                        out_links = len(graph.neighbors(n))
                        rank_sum += (1 / float(out_links)) * graph.node[n]['rank']
            ranks[key] = ((1 - s) * (1 / V)) + s * rank_sum

            for key, rank in ranks.iteritems():
                graph.node[key]['rank'] = rank
    return ranks


import csv
reader = csv.reader(open('lesmis.csv', 'r'), delimiter=',')
data = [row for row in reader]
nodes = set([row[0] for row in data])
nodes.update([row[2] for row in data])

edges = [(row[0], row[1], row[2]) for row in data] # edge의 weight가 두번째 column에 들어있다


num_nodes = len(nodes)
rank = 1/float(num_nodes)

# what is affected by size? -> no effect, why?
#graph.add_nodes_from(nodes, rank=rank, size=3)
graph.add_nodes_from(nodes, rank=rank, size=10)

# adding different weight for each edges
#graph.add_edges_from(edges, weight=1)
for source, weight, target in edges:
    graph.add_edge(source, target, weight=weight)

ranks = dict()
V = float(len(graph))
MIN_NODE_SIZE = 5.0

# rank node with PageRank algorithm
ranks = rank_nodes(graph);

for key, node in graph.nodes(data=True):
    rank = graph.node[key]['rank']
    # below code resize the node size
    print(round(MIN_NODE_SIZE * rank * V))
    graph.node[key]['size'] = max(round(MIN_NODE_SIZE), round(MIN_NODE_SIZE * rank * V))


node_to_remove = []
for key, rank in ranks.iteritems():
    if rank < 1.0 / V: # PageRank가 처음보다 작아지면
        node_to_remove.append(key)
graph.remove_nodes_from(node_to_remove)

jgraph = json_graph.node_link_data(graph)

import json
json.dump(jgraph, open('force.json','w'))