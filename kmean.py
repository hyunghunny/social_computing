# coding=UTF-8

from csvpivot import transpose
from dataloader import TSVDataLoader

from cluster import kcluster
from cluster import printclust
from cluster import jsonclust

from distance import pearson
from distance import euclidean
from distance import tanimoto
from distance import hamdist
from distance import kl
from distance import manhattan



def getWordsGroups(cluster) :
    groups = []
    for c in cluster:
        words = []
        for i in c:
            words.append(dataLoader.names[i])
        groups.append(words)
    return groups


def selectAppleGoogleWordGroups(groups) :
    selected_groups = []
    for words in groups:
        #print words
        for word in words:
            if word == 'google':
                #print 'google is shown in words'
                selected_groups.append(words)
                break
            if word == 'apple':
                #print 'apple is shown in words'
                selected_groups.append(words)
                break
    return selected_groups

# pivot blogdata.txt to transpose.txt
transpose('blogdata.txt', 'transpose.txt')

distances = { 'Euclidean distance':  euclidean,
              'Tanimoto distance' : tanimoto,
              'Pearson distance': pearson,
              'Haming distance' : hamdist,
              'Kullback-Leibler distance': kl,
              'Manhattan distance' :manhattan
              }

dataLoader = TSVDataLoader('transpose.txt')

report = {}

for key in distances:
    cluster = kcluster(dataLoader.data, distances[key], 10)
    groups = getWordsGroups(cluster)
    report[key] = selectAppleGoogleWordGroups(groups)

for key in report :
    print key
    for groups in report[key] :
        print groups
    print '----------------------------'
