# coding=UTF-8

##
# Zebo data clustering
# @author webofthink@snu.ac.kr
#

# coding=UTF-8

##
# Blog data clustering
# @author webofthink@snu.ac.kr
#

from cluster import hcluster
from cluster import printclust
from cluster import jsonclust

from distance import pearson
from distance import euclidean
from distance import tanimoto
from distance import hamdist
from distance import kl
from distance import manhattan

from dataloader import JSONDataLoader


# Simple test
dataLoader = JSONDataLoader('zebo.txt')
print dataLoader.names
cluster = hcluster(dataLoader.data, manhattan)
printclust(cluster, dataLoader.names)

f = open('dendrogram.json', 'w')
jsonclust(cluster, f, True, dataLoader.names)
f.close()