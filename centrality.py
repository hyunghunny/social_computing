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
reader = csv.reader(open('netscience.csv', 'r'), delimiter=',')
data = [row for row in reader]
nodes = set([row[0] for row in data])
nodes.update([row[2] for row in data])

edges = [(row[0], row[1], row[2]) for row in data]


num_nodes = len(nodes)
rank = 1/float(num_nodes)

# preset node
graph.add_nodes_from(nodes, rank=rank, name='', degree=0, closeness=0,  betweenness=0, eigenvector=0, size=10)

# adding different weight for each edges
for source, weight, target in edges:
    graph.add_edge(source, target, weight=weight)

ranks = dict()
V = float(len(graph))



# rank node with PageRank algorithm
ranks = rank_nodes(graph)

#  metrics
import operator
# print top tankers by PageRank
print sorted(ranks.items(), key=operator.itemgetter(1), reverse=True)

degree_centralities = nx.degree_centrality(graph)
# print top ranker by degree
print sorted(degree_centralities.items(), key=operator.itemgetter(1), reverse=True)

closeness_centralities = nx.closeness_centrality(graph)
# print top ranker by closeness
print sorted(closeness_centralities.items(), key=operator.itemgetter(1), reverse=True)

betweenness_centralities = nx.betweenness_centrality(graph)
# print top ranker by betweenness
print sorted(betweenness_centralities.items(), key=operator.itemgetter(1), reverse=True)

eigenvector_centralities = nx.eigenvector_centrality(graph)
# print top ranker by eigenvector
print sorted(eigenvector_centralities.items(), key=operator.itemgetter(1), reverse=True)

node_to_remove = []
hall_of_fame = [] # for honorable members

MIN_NODE_SIZE = 2.0
MIN_BADGE_NODE_SIZE = 20.0 # show name if the node size exceeds it

for key, node in graph.nodes(data=True):
    rank = graph.node[key]['rank']
    name = graph.node[key]['name']

    degree = degree_centralities[key]
    closeness = closeness_centralities[key]
    betweenness = betweenness_centralities[key]
    eigenvector = eigenvector_centralities[key]

    graph.node[key]['degree'] = degree
    graph.node[key]['closeness'] = closeness
    graph.node[key]['betweenness'] = betweenness
    graph.node[key]['eigenvector'] = eigenvector

    # set criteria e.g. rank, degree, closeness, betweenness, eigenvector
    criteria = betweenness * V / 2
    # remove node if the guy is not so remarkable
    if (round(MIN_NODE_SIZE * criteria) < round(MIN_NODE_SIZE)) :
        #print (key + " is not so remarkable. The rank: " + str(rank))
        node_to_remove.append(key)

    # below code resize the node size
    size = max(round(MIN_NODE_SIZE), round(MIN_NODE_SIZE * criteria))
    graph.node[key]['size'] = size

    # if node is honorable, set badge name
    if (size > MIN_BADGE_NODE_SIZE) :
        # print (key + ' get badge with score ' + str(rank))
        graph.node[key]['name'] = key
        hall_of_fame.append(graph.node[key])


for key, rank in ranks.iteritems():
    if rank < 1.0 / V: # PageRank가 처음보다 작아지면
       # print (key + ' is banned.')
        node_to_remove.append(key)
graph.remove_nodes_from(node_to_remove)

jgraph = json_graph.node_link_data(graph)

import json
json.dump(jgraph, open('force2.json','w'))

# show honors in hall of frame with ascending order
def getKey(item) :
    return item['rank']
idx = 1
for honor in sorted(hall_of_fame, key=getKey, reverse=True) :
    # print str(idx) + '. ' + honor['name'] + ': ' + str(honor['rank'])
    idx = idx + 1
