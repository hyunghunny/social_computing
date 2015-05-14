# coding=UTF-8
##
# Social computing HW#8
#


from math import log

import nltk

from reuter import loadReuterDataSet


def tf(term, doc):
    doc = doc.lower().split()
    return doc.count(term.lower()) / float(len(doc))

def idf(term, corpus):
    num_texts_with_term = len([True for text in corpus if term.lower() in text.lower().split()])
    try:
        return 1.0 + log(float(len(corpus)) / num_texts_with_term)
    except ZeroDivisionError:
        return 1.0

def tf_idf(term, doc, corpus):
    return tf(term, doc) * idf(term, corpus)

# NLTK utility
def printTokenLength(tokens) :
    print len(tokens)

# Number of unique words in the text
def printUniqueWordsSize(fdist) :
    print len(fdist.keys())

# Number of URLs
def printUrlsSize(fdist) :
    print len([w for w in fdist.keys() if w.startswith("http")])

# TF-IDF code in slide
def tfIdfDemo() :
    # corpus and terms
    corpus = {
        'a' : "Mr. Green killed Colonel Mustard in the study with the candlestick. \
            Mr. Green is not a very nice fellow.",
        'b' : "Professor Plum has a green plant in his study.",
        'c' : "Miss Scarlett watered Professor Plum's green plant while he was away  \
            from his office last week."
    }

    terms = {
        'a' : [
            i.lower() for i in corpus['a'].split()
            ],
        'b' : [
            i.lower() for i in corpus['b'].split()
            ],
        'c' : [
            i.lower() for i in corpus['c'].split()
            ]
        }

    query_scores = {
        'a': 0,
        'b': 0,
        'c': 0
    }

    QUERY_TERMS = [ 'mr.', 'green']

    for term in [t.lower() for t in QUERY_TERMS]:
        for doc in sorted(corpus):
            print 'TF(%s): %s' % (doc, term), tf(term, corpus[doc])
        print 'IDF: %s' % ( term, ), idf(term, corpus.values())
        print
        for doc in sorted(corpus):
            score = tf_idf(term, corpus[doc], corpus.values())
            print 'TF-IDF(%s): %s' % (doc, term), score
            query_scores[doc] += score
        print

    print "Overall TF-IDF scores for query '%s'" % (' '.join(QUERY_TERMS), )
    for (doc, score) in sorted(query_scores.items()):
        print doc, score

    # Download ancillary nltk packages if not already installed
    #nltk.download('stopwords')

    all_content = " ".join( [corpus[index] for index in corpus] )

    # Approximate bytes of text
    print len(all_content)

    tokens = all_content.split()
    text = nltk.Text(tokens)

    # Examples of the appearance of the word "open"
    text.concordance("open")

    # Frequent collocations in the text (usually meaningful phrases)
    text.collocations()

    # Frequency analysis for words of interest
    fdist = text.vocab()
    fdist["green"]
    fdist["mr."]
    fdist["the"]


    # Common words that aren't stopwords
    [w for w in fdist.keys()[:100] \
        if w.lower() not in nltk.corpus.stopwords.words('english')]

    # Long words that aren't URLs
    [w for w in fdist.keys() if len(w) > 15 and not w.startswith("http")]


    # Enumerate the frequency distribution
    for rank, word in enumerate(fdist):
        print rank, word, fdist[word]



def getRelevantActivities(dataset, terms) :
    activities = [article['text'].lower().split() for article in dataset]
    # TextCollection provides tf, idf, and tf_idf abstractions so
    # that we don't have to maintain/compute them ourselves
    tc = nltk.TextCollection(activities)

    relevant_activities = []
    for idx in range(len(activities)):
        score = 0
        for term in [t.lower() for t in terms]:
            score += tc.tf_idf(term, activities[idx])
        if score > 0:
            relevant_activities.append({
                'score': score,
                'author': dataset[idx]['author'],
                'filename': dataset[idx]['filename'],
                'filepath': dataset[idx]['filepath']
            })
    return relevant_activities


def print10RelevantActivities(relevant_activities) :
    # Sort by score and display results
    relevant_activities = sorted(relevant_activities, key=lambda p: p['score'], reverse=True)

    for activity in relevant_activities[:10]:
        print activity['author']
        print '\tFile: %s' % (activity['filepath'], )
        print '\tScore: %s' % (activity['score'], )
        print

def tsv10RelevantActivities(relevant_activities) :
    # Sort by score and display results
    relevant_activities = sorted(relevant_activities, key=lambda p: p['score'], reverse=True)
    print "Author\tFile\tScore"
    for activity in relevant_activities[:10]:
        print activity['author'] + "\t" + activity['filename'] + "\t" + str(activity['score'])


# Reuter data set중 C50train 디렉토리에 있는 2500개의 기사들 중에
# 다음 query에 대하여 tf-idf 값이 높은 상위 10개의 기사를 찾아서 각각 리스트를 제출하세요
# XXX: Multigram should be divided if not, it doesn't work properly
topics = [ 'Hong', 'Kong', 'technology', 'government', 'human', 'rights' ]

dataset = loadReuterDataSet("train")
print len(dataset)
#inspectDataSet(dataset)
activities = getRelevantActivities(dataset, topics)
print "For all 4 topics, top 10 articles are as below: "
tsv10RelevantActivities(activities)
print "***************************************************"

topics = [ 'Hong', 'Kong' ]
activities = getRelevantActivities(dataset, topics)
print "For Hong Kong topics, top 10 articles are as below: "
tsv10RelevantActivities(activities)
print "***************************************************"

topics = [ 'technology', 'government' ]

for topic in topics :
    print "For " + topic + "'s top 10 articles are as below: "
    queries = [ topic ]
    activities = getRelevantActivities(dataset, queries)
    tsv10RelevantActivities(activities)
    print "***************************************************"


topics = [ 'human', 'right' ]

activities = getRelevantActivities(dataset, topics)
print "For human rights topics, top 10 articles are as below: "
tsv10RelevantActivities(activities)
print "***************************************************"
