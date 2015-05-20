# coding=UTF-8

# Unsupervised Classification by Decision Tree with Car+Evaluation data
# @author webofthink@snu.ac.kr
#

import nltk
import random

from car import Car
from car import read_csv_data


def loadCarList(path) :
    car_data_list = read_csv_data(car_csv_path)
    #print len(car_data_list)
    car_list = []
    for car_data in car_data_list :

        if (len(car_data) == 7) :
            if (car_data[6].find('unacc') < 0): # XXX: surpass when classification is unacc
                car = Car(car_data)
                #print car.price()
                car_list.append(car)
        else:
            print car_data
    #print len(car_list)

    return car_list

def getLabeledCars(car_list) :
    all_cars = [(car, car.getClass()) for car in car_list]
    # for shuffling data
    random.shuffle(all_cars)
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


def n_fold_cv(n, feature_sets, func) :
    print '---------------------------------------------------'

    feature_sets_size = len(feature_sets)
    print "total data set: " + str(feature_sets_size)

    accuracies = []

    # print 'test set size: ' + str(test_length)
    # randomKey = random.randrange(0, n) # select random value
    test_set_size = int(round(feature_sets_size / n))

    for step in range(0, n) :

        train_set = []
        test_set = []

        print str(n) + '-fold cross validation: ' + str(step)
        idx = 0
        for feature in feature_sets:

            if (idx >= (step * test_set_size)) and (idx < (step * test_set_size) + test_set_size):
                test_set.append(feature)
            else:
                train_set.append(feature)
            idx = idx + 1

        print "number of training sets: " + str(len(train_set))
        print "number of test sets: " + str(len(test_set))

        accuracy = func(train_set, test_set)
        accuracies.append(accuracy)

        print '---------------------------------------------------'

    # print average accuracy
    accuracy_sum = 0.0
    for accuracy in accuracies:
        accuracy_sum = accuracy_sum + accuracy

    avg_accuracy = (accuracy_sum / len(accuracies))
    print "average accuracy: " + str(avg_accuracy)

def runDecisionTree(train_set, test_set) :
    classifier = nltk.DecisionTreeClassifier.train(train_set)
    accuracy = nltk.classify.accuracy(classifier, test_set)
    print "classification accuracy: " + str(accuracy)
    # Print Out Decision Tree
    print classifier.pseudocode(depth = 4)

    return accuracy


# Simple Test

car_csv_path = '.\\car\\car.data'
cars = loadCarList(car_csv_path)

all_cars = getLabeledCars(cars)

print "using tech attributes as feature set: "
features = getAllFeatures
#features = getPriceFeatures
#features = getTechFeatures

feature_sets = getFeatureSets(all_cars, features)
# 5 fold CV
n_fold_cv(5, feature_sets, runDecisionTree)

