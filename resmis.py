# coding=UTF-8

# code SHOULD be refactored
import networkx as nx, json, csv
from networkx.readwrite import json_graph
graph = nx.Graph()
reader = csv.reader(open('lesmis.csv', 'r'), delimiter=',')
data = [row for row in reader]
nodes = set([row[0] for row in data])
nodes.update([row[2] for row in data])
edges = [(row[0], row[2]) for row in data]
#edges = [(row[0], row[1], row[2]) for row in data] # edge의 weight가 두번째 column에 들어있다


num_nodes = len(nodes)
rank = 1/float(num_nodes)

#graph.add_nodes_from(nodes, rank=rank, size=3)
graph.add_nodes_from(nodes, rank=rank, size=5)


#graph.add_edges_from(edges, weight=1)
for source, weight, target in edges:
    graph.add_edge(source, target, weight=weight)

#
# Some algorithm
#

ranks = dict()
V = float(len(graph))
s = 0.85

# FIX ME

for key, node in graph.nodes(data=True):
    rank = graph.node[key]['rank']
    graph.node[key]['size'] = max(3, round(3.0 * rank * V))



node_to_remove = []
for key, rank in ranks.iteritems():
    if rank < 1.0/V: # PageRank가 처음보다 작아지면
        node_to_remove.append(key)
graph.remove_nodes_from(node_to_remove)

jgraph = json_graph.node_link_data(graph)
json.dump(jgraph, open('force.json','w'))