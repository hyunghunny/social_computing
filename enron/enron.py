# coding=UTF-8

# Top 100 ranking for most e-mail senders in enron
# @author webofthink@snu.ac.kr
#
import json

import networkx as nx
from networkx.readwrite import json_graph
import pymongo # pip install pymongo

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


def writeJSONGraph(graph):
    json.dump(json_graph.node_link_data(graph), open('force.json','w'))

def findTopSenders(n):
    # find top 'n' person who sent many e-mails
    #client = pymongo.MongoClient()
    client = pymongo.MongoClient('datascience.snu.ac.kr', 27017) # for using lab's db server

    # Reference the mbox collection in the Enron database
    mbox = client.enron.mbox # The number of messages in the collection

    # in all senders, calculate the # of recipients for each sender
    all_senders = [ i for i in mbox.distinct("From")
        if i.lower().find("@enron.com") > -1 ]

    sender_recipients = []
    for sender in all_senders:
        # Get the recipient lists for each message
        recipients_per_message = mbox.aggregate([
            { "$match": {"From": sender } },
            {"$project": {"From": 1, "To": 1} },
            {"$group": {"_id": "$From", "recipients": {"$addToSet": "$To" } } }
        ]).next()['recipients']

        # Collapse the lists of recipients into a single list
        all_recipients = [ recipient for message in recipients_per_message for recipient in message]
        #print sender + " has recipients: " + str(len(all_recipients))
        sender_recipients.append({
            "id" : sender[:sender.index('@')], # extract id from email address
            "email" : sender,
            "recipients" : all_recipients,
            "count" : len(all_recipients)
        })

    # sort and select top n senders
    from operator import itemgetter
    sorted_list = sorted(sender_recipients, key=itemgetter("count"), reverse=True)
    selected_list = sorted_list[:n]

    return selected_list


def createEdges(top_senders):

    edges = []
    for top_sender in top_senders:
        # num_of_unique_recipients = len(set(top_sender['recipients'])) # remove duplicates
        #print top_sender['id'] + ":" + str(num_of_unique_recipients)
        # count the occurrence of selected sender in recipients
        for interested_sender in top_senders:
            exchange_count = top_sender['recipients'].count(interested_sender['email'])
            # skip self-received mails and no exchanges between them
            if (top_sender['email'] is not interested_sender['email'] and exchange_count > 0):
                #print top_sender['id'] + ":" + str(exchange_count) + ":" + interested_sender['id']
                edges.append((top_sender['id'], exchange_count, interested_sender['id']))
    return edges


# 가장 많은 이메일을 보낸 사람을 순서대로 100명을 구하시오
# 사람을 노드로 그들간의 이메일 교환을 링크로 하는 graph를 구하고 전에 배운 force.html을
# 이용하여 소셜 그래프로 그리고 이를 enron.jpg로 capture해서 제출

graph = nx.Graph()
num_nodes = 100
rank = 1/float(num_nodes)
top_senders = findTopSenders(num_nodes)

# print top 100 senders
for sender in top_senders :
    print sender['id'] + ": " + str(sender['count'])

nodes = set([sender['id'] for sender in top_senders])
edges = createEdges(top_senders)

graph.add_nodes_from(nodes, rank=rank, size=10)

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
    lank_score = (round(MIN_NODE_SIZE * rank * V))
    if (lank_score >= 10) :
        print key + ": " + str(lank_score)
    graph.node[key]['size'] = max(round(MIN_NODE_SIZE), round(MIN_NODE_SIZE * rank * V))

# create force.json for visualizing with force.html
writeJSONGraph(graph)