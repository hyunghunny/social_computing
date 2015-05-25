# coding=UTF-8

# Top 100 ranking for most e-mail senders in enron
# @author webofthink@snu.ac.kr
#
import json

import networkx as nx
from networkx.readwrite import json_graph
import pymongo # pip install pymongo


def writeJSONGraph(graph):
    json.dump(json_graph.node_link_data(graph), open('force.json','w'))

def findTopSenders(n):
    # TODO: find top 'n' person who sent many e-mails
    client = pymongo.MongoClient()
    #client = pymongo.MongoClient('datascience.snu.ac.kr', 27017) # for using lab's db server

    # Reference the mbox collection in the Enron database
    mbox = client.enron.mbox # The number of messages in the collection

    # in all senders, calculate the # of mails
    senders = [ i for i in mbox.distinct("From")
        if i.lower().find("@enron.com") > -1 ]

    return set()

# TODO 가장 많은 이메일을 보낸 사람을 순서대로 100명을 구하시오
# TODO 사람을 노드로 그들간의 이메일 교환을 링크로 하는 graph를 구하고 전에 배운 force.html을
# TODO 이용하여 소셜 그래프로 그리고 이를 enron.jpg로 capture해서 제출

graph = nx.Graph()
num_nodes = 100
rank = 1/float(num_nodes)
nodes = findTopSenders(num_nodes)
# update nodes
graph.add_nodes_from(nodes, rank=rank, size=10)

# create force.json for visualizing with force.html
#writeJSONGraph(graph)