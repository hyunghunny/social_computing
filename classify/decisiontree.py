# coding=UTF-8

# Unsupervised Classification by Decision Tree with Car+Evaluation data
# @author webofthink@snu.ac.kr
#

from car import Car
from car import read_csv_data

import nltk
import random


def loadCarList(path) :
    car_data_list = read_csv_data(car_csv_path)
    #print len(car_data_list)
    car_list = []
    for car_data in car_data_list :
        if (len(car_data) == 7) :
            car = Car(car_data)
            #print car.price()
            car_list.append(car)
    #print len(car_list)

    return car_list

def getLabeledCars(car_list) :
    all_cars = [(car, car.getClass()) for car in car_list]
    # for shuffling data
    #random.shuffle(all_cars)
    return all_cars

def getFeatureSets(cars, func):
    feature_sets = [ (func(n), g) for (n, g) in cars ]
    return feature_sets

def getAllFeatures(car) :
    features = {}
    features['buying'] = car._buying
    features['maint'] = car._maint
    features['doors'] = car._doors
    features['persons'] = car._persons
    features['lug_boot'] = car._lug_boot
    features['safety'] = car._safety
    return features

def getPriceFeatures(car) :
    features = {}
    features['buying'] = car._buying
    features['maint'] = car._maint

    return features

def getTechFeatures(car) :
    features = {}
    features['doors'] = car._doors
    features['persons'] = car._persons
    features['lug_boot'] = car._lug_boot
    features['safety'] = car._safety

    return features

car_csv_path = '.\\car\\car.data'
cars = loadCarList(car_csv_path)

all_cars = getLabeledCars(cars)

print "using all attributes as features"
print '---------------------------------------------------'
features = getAllFeatures
#features = getPriceFeatures
#features = getTechFeatures


feature_sets = getFeatureSets(all_cars, features)
test_length = int(round(len(feature_sets) / 5))
tree_depth_count = 2


# print 'test set size: ' + str(test_length)
randomKey = random.randrange(1, 6) # select

accuracies = []
n = 5
for step in range(0, n) :
    # for N fold CV
    train_set = []
    test_set = []

    print '5-fold cross validation: ' + str(step)
    idx = 0
    for feature in feature_sets:

        if (idx >= (step * test_length)) and (idx < (step * test_length) + test_length):
            test_set.append(feature)
        else:
            train_set.append(feature)
        idx = idx + 1

    print "number of training sets: " + str(len(train_set))
    print "number of test sets: " + str(len(test_set))

    # Using Decision Tree Classifier

    classifier = nltk.DecisionTreeClassifier.train(train_set)

    accuracy = nltk.classify.accuracy(classifier, test_set)
    accuracies.append(accuracy)
    print "classification accuracy: " + str(accuracy)

    # Print Out Decision Tree
    print classifier.pseudocode(depth=tree_depth_count)
    print '---------------------------------------------------'

# print average accuracy
accuracy_sum = 0.0
for accuracy in accuracies:
    accuracy_sum = accuracy_sum + accuracy

avg_accuracy = (accuracy_sum / len(accuracies))
print "average accuracy: " + str(avg_accuracy)