# coding=UTF-8

import math, random

##
# read data from csv file
# @param csv_file CSV file to be loaded
# @return table data
#
def read_csv_data(csv_file):
    import csv
    reader = csv.reader(open(csv_file, 'r'), delimiter=',')
    data = [row for row in reader]
    return data

##
# create a graph to be page-ranked
# @param data CSV data to be loaded
# @return graph which is prepared
#
def create_graph(data):

    graph = nx.Graph()
    data = read_csv_data(data + '.csv')
    nodes = set([row[0] for row in data])
    edges = [(row[0], row[2]) for row in data]
    num_nodes = len(nodes)
    rank = 1/float(num_nodes)
    graph.add_nodes_from(nodes, rank=rank)
    graph.add_edges_from(edges)
    return graph


##
# page rank algorithm (old)
# @brief this version excerpted from the lecture slide
# @return the ranking dictionary
#
def calculate_page_ranks_old(graph):
    # Assign initial values
    ranks = dict()
    V = float(len(graph))
    s = 0.85

    for key, node in graph.nodes(data=True):
        ranks[key] = node.get('rank')

    for _ in range(10):
        for key, node in graph.nodes(data=True):
            rank_sum = 0.0
            curr_rank = node.get('rank')
            neighbors = graph[key]
            for n in neighbors: # for each neighbors, gather its pagerank
                if ranks[n] is not None:
                    out_links = len(graph.neighbors(n))
                    rank_sum += (1 / float(out_links)) * ranks[n]
            ranks[key] = ((1 - s) * (1/V)) + s*rank_sum
    return ranks

##
# fixed page rank algorithm (new)
# @brief this version excerpted from the notice by prof.
# @param graph the graph to be page-ranked
# @return the ranking dictionary
#
def calculate_page_ranks_new(graph):
    # Assign initial values
    ranks = dict()
    V = float(len(graph))
    s = 0.85

    for key, node in graph.nodes(data=True):
        ranks[key] = node.get('rank')

    for _ in range(10):
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


def write_file(filename, lines) :
    f = file(filename, 'w')
    for word in lines:
        try:
            f.write(word.encode('utf-8') + '\n')
        except UnicodeEncodeError, e:
            print 'Encoding error ' + word + '\n'
    f.close()


import networkx as nx, operator

#csv_data = 'polblogs'
#csv_data = 'lesmis'
csv_data = 'dolphins'


graph = create_graph(csv_data)
ranks = calculate_page_ranks_new(graph)

sorted_ranks = sorted(ranks.iteritems(), key=operator.itemgetter(1), reverse=True)

# print out the results
f = file(csv_data +'.txt', 'w')
for tuple in sorted_ranks:
    line = tuple[0] + '\t' + str(tuple[1]) + '\n'
    f.write(line)
f.close()

