# coding=UTF-8

# @brief enron corpus analysis
#
# @author webofthink@snu.ac.kr
#

import json

import networkx as nx
from networkx.readwrite import json_graph
import pymongo # pip install pymongo
from collections import Counter
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


def get_all_senders(mbox) :
    import re
    query = mbox.find({ "X-To": {"$regex" : re.compile(r"^.+")} }) # find valid mail which has (a) recipient(s)
    #query = mbox.find({})
    all_mails = [ msg for msg in query ]
    #print len(all_mails)

    # sort all mails by sender who sent many mails
    all_senders = [ msg["From"] for msg in all_mails ]
    return all_senders


def print_top_rank(all_senders, n):

    sent_occurrences = Counter(all_senders)
    # print top 100 senders
    ranks = sent_occurrences.most_common(n)
    counter = 1
    for ranker in ranks :
        print str(counter) + ", " + ranker[0] + ", " + str(ranker[1])
        counter = counter + 1


# get all nodes from mbox and valid senders
def get_all_nodes(mbox, senders) :

    receivers = [ i for i in mbox.distinct("To") ]
    cc_receivers = [ i for i in mbox.distinct("Cc") ]
    bcc_receivers = [ i for i in mbox.distinct("Bcc") ]

    # get all nodes
    all_nodes = set()
    all_nodes.update(senders)
    all_nodes.update(receivers)
    all_nodes.update(cc_receivers)
    all_nodes.update(bcc_receivers)

    # if node use @enron.com, set id only
    return_nodes = set()
    for node in all_nodes:
        if node.lower().find("@enron.com") > -1 :
            # tokenize id
            return_nodes.add(node[:node.index('@')]) # extract id from email address
        else :
            return_nodes.add(node)

    return return_nodes

def get_mail_exchange(mbox, all_senders):
    sender_recipients = []
    all_senders = set(all_senders) # remove duplicates
    for sender in all_senders:
        # Get all recipient lists for each message
        results = mbox.aggregate([
            {"$match": {"From" : sender }
            },
            {"$project":
                {"From": 1, "To": 1, "Cc": 1, "Bcc": 1 }
            },
            {"$group":
                {"_id":	"$From",
                    "recipients": { "$addToSet" : "$To"   },
                    "carbone_copy" : { "$addToSet" : "$Cc"   },
                    "blind_carbone_copy" : { "$addToSet" : "$Bcc"   },
                    }
                }

        ])
        all_recipients = list()
        for r in results:

            for recipients in r["recipients"]:
                for to in recipients :
                    all_recipients.append(to)
            for recipients in r["carbone_copy"]:
                for cc in recipients :
                    all_recipients.append(cc)
            for recipients in r["blind_carbone_copy"]:
                for bcc in recipients :
                    all_recipients.append(cc)

        sender_recipients.append({
            "id" : sender[:sender.index('@')], # extract id from email address
            "sender" : sender,
            "recipients" : list(all_recipients),
            "count" : len(all_recipients)
        })
        return sender_recipients

def createEdges(exchanges):

    edges = []
    for exchange in exchanges:
        # count the occurrence of selected sender in recipients
        sender = exchange['id']
        recipient_occurrences = Counter(exchange['recipients'])
        print recipient_occurrences
        for key in recipient_occurrences:
            recipient = key[:key.index('@')]
            exchange_count = recipient_occurrences[key]
            edges.append((sender, exchange_count, recipient))

    return edges


# 가장 많은 이메일을 보낸 사람을 순서대로 100명을 구하시오
# 사람을 노드로 그들간의 이메일 교환을 링크로 하는 graph를 구하고 전에 배운 force.html을
# 이용하여 소셜 그래프로 그리고 이를 enron.jpg로 capture해서 제출

#client = pymongo.MongoClient()
client = pymongo.MongoClient('datascience.snu.ac.kr', 27017) # for using lab's db server

# Reference the mbox collection in the Enron database
mbox = client.enron.mbox # The number of messages in the collection


all_senders = get_all_senders(mbox)
print_top_rank(all_senders, 100)
nodes = get_all_nodes(mbox, all_senders)
num_nodes = len(nodes) # of total nodes

print "Total nodes: " + str(num_nodes)

exchanges = get_mail_exchange(mbox, all_senders)
print len(exchanges)
edges = createEdges(exchanges)
print len(edges)


graph = nx.Graph()
rank = 1/float(num_nodes)

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

node_to_remove = []
for key, rank in ranks.iteritems():
    if rank < 1.0 / V: # PageRank가 처음보다 작아지면
        node_to_remove.append(key)
graph.remove_nodes_from(node_to_remove)

# create force.json for visualizing with force.html
writeJSONGraph(graph)
