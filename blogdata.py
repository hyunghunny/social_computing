# coding=UTF-8
from distance import pearson
from distance import euclidean
from distance import tanimoto

class BlogDataLoader :
    def __init__(self, fileName) :

        self.lines = [line for line in file(fileName)]

        # First line is the column titles
        words = self.lines[0].strip().split('\t')[1:]
        #print(words)
        self.blognames = []
        self.data = []
        for line in self.lines[1:]:
            p = line.strip().split('\t')
            # First column in each row is the rowname
            self.blognames.append(p[0])
            # The data for this row is the remainder of the row
            self.data.append([float(x) for x in p[1:]])

class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.vec = vec
        self.left = left
        self.right = right
        self.distance = distance
        self.id = id


def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

    # Clusters are initially just the rows
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)

        closest = distance(clust[0].vec, clust[1].vec)

        # loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                # distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # FIXME: this algorithm makes the prior merged vectors are weaken
        # calculate the average of the two clusters
        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) /
                    2.0 for i in range(len(clust[0].vec))]

        # create the new cluster
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]], right=clust[lowestpair[1]],
                            distance=closest, id=currentclustid)

        # cluster ids that weren't in the original set are negative
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]


def printclust(clust, labels=None, n=0):

    # indent to make a hierarchy layout
    for i in range(n):
        print '',
    if clust.id < 0:
        # negative id means that this is branch
        print '-'
    else:
        # positive id means that this is an endpoint
        if labels == None:
            print clust.id
        else:
            print labels[clust.id]

    # now print the right and left branches
    if clust.left != None:
        printclust(clust.left, labels=labels, n=n + 1)
    if clust.right != None:
        printclust(clust.right, labels=labels, n=n + 1)


def jsonclust(clust, file, last=True, labels=None):

    if clust.id < 0:
        # negative id means that this is branch
        file.write('{ "children": [')
    else:
        # positive id means that this is an endpoint
        if labels == None:
            file.write('{"name": "%s"}' % clust.id)
        else:
            file.write('{"name": "%s"}' % labels[clust.id].replace('"', '').strip())
        if not last:
            file.write(',')

    # now print the right and left branches
    if clust.left != None:
        jsonclust(clust.left, file, False, labels=labels)

    if clust.right != None:
        jsonclust(clust.right, file, True, labels=labels)

    if clust.id < 0:
        if last:
            file.write(']}')
        else:
            file.write(']},')

# Simple test
dataLoader = BlogDataLoader('blogdata.txt')
print dataLoader.blognames
cluster = hcluster(dataLoader.data)
printclust(cluster, dataLoader.blognames)

f = open('dendrogram.json', 'w')
jsonclust(cluster, f, True, dataLoader.blognames)
f.close()