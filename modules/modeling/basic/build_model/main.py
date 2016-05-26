#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datacanvas.new_runtime import BasicRuntime, DataCanvas
dc = DataCanvas(__name__)


# load my pkg
import csv
import math
import pickle
import random
import string


def load_csv(filename):
    lines = csv.reader(open(filename, "r"))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]        
    return dataset


def split_dataset(dataset, split_ratio):
    train_size = int(len(dataset) * split_ratio)
    train_set = []
    copy = list(dataset)
    while len(train_set) < train_size:
        index = random.randrange(len(copy))
        train_set.append(copy.pop(index))
    return [train_set, copy]


def separate_by_class(dataset):
    separated = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if (vector[-1] not in separated):
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)
    return separated


def mean(numbers):
    return sum(numbers) / float(len(numbers))


def stdev(numbers):
    avg = mean(numbers)
    variance = sum([pow(x-avg, 2) for x in numbers]) / float(len(numbers)-1)
    return math.sqrt(variance)


def summarize(dataset):
    summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
    del summaries[-1]
    return summaries


def summarize_by_class(dataset):
    separated = separate_by_class(dataset)
    summaries = {}
    for class_value, instances in separated.items():
        summaries[class_value] = summarize(instances)
    return summaries


def calculate_probability(x, mean, stdev):
      exponent = math.exp(-(math.pow(x-mean,2) / (2*math.pow(stdev,2))))
      return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent


def calculate_class_probabilities(summaries, input_vector):
    probabilities = {}
    for class_value, class_summaries in summaries.items():
        probabilities[class_value] = 1
        for i in range(len(class_summaries)):
            mean, stdev = class_summaries[i]
            x = input_vector[i]
            probabilities[class_value] *= calculate_probability(x, mean, stdev)
    return probabilities


def predict(summaries, input_vector):
    probabilities = calculate_class_probabilities(summaries, input_vector)
    best_label, best_prob = None, -1
    for class_value, probability in probabilities.items():
                  if best_label is None or probability > best_prob:
                      best_prob = probability
                      best_label = class_value
    return best_label


def get_predictions(summaries, test_set):
    predictions = []
    for i in range(len(test_set)):
        result = predict(summaries, test_set[i])
        predictions.append(result)
    return predictions


def get_accuracy(test_set, predictions):
    correct = 0
    for x in range(len(test_set)):
        if test_set[x][-1] == predictions[x]:
            correct += 1
    return (correct/float(len(test_set))) * 100.0


@dc.basic_runtime(spec_json="spec.json")
def my_module(rt, params, inputs, outputs):
    # TODO : Fill your code here
    # get params
    times =  int(string.atof(params.times))
    split_ratio =  string.atof(params.ratio)
    print('times: {0}  ratio: {1}'.format(times, split_ratio))

    # get inputs
    filename = inputs.datafile
    print('datafile: {0}'.format(filename))

    # get outputs
    modelname = outputs.modelname
    print('modelname: {0}'.format(modelname))

    accuracy_best = -1
    dataset = load_csv(filename)
    print('Load data successfully')

    # training model
    for i in range(times):
        training_set, test_set = split_dataset(dataset, split_ratio)
        print('Split {0} rows into train={1} and test={2} rows'.format(len(dataset), len(training_set), len(test_set)))
        # print('TrainingSet: {0} \n TestSet: {1}'.format(training_set, test_set))

        # get summaries
        summaries_new = summarize_by_class(training_set)
        print('Summaries: {0}'.format(summaries_new))

        # do predictions
        predictions = get_predictions(summaries_new, test_set)
        print('Predictions: {0}'.format(predictions))

        # appraise model
        accuracy_new = get_accuracy(test_set, predictions)
        print('Accuracy: {0}%'.format(accuracy_new))

        # select model
        if accuracy_best < accuracy_new:
            summaries_best = summaries_new
            accuracy_best = accuracy_new
    print('Summaries: {0} Accuracy: {1}%'.format(summaries_best, accuracy_best))

    # save model
    file = open(modelname, 'w')
    pickle.dump(summaries_best, file)            

    print "Done"


if __name__ == "__main__":
    dc.run()
