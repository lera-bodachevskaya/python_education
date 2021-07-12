import os
import argparse

import pandas as pd

import user_exceptions as ex
from classifier import Classifier
from clustring import Clustering
from dimension_reduction import DimensionReduction


methods = ["classification", "clustering", "reduction"]
activation_functions = ['identity', 'logistic', 'tanh', 'relu']
cv_types = ['kfold', 'loo', 'random']
description = 'Machine Learning'
arguments = [{'name': '-f',
              'type': str,
              'dest': 'path',
              'required': True,
              'help': 'path to csv file'},
             {'name': '-real',
              'type': int,
              'dest': 'class_column',
              'required': True,
              'help': 'column number with the class names'},
             {'name': '-m',
              'type': str,
              'dest': 'method',
              'required': True,
              'help': 'method type: classification, clustering, reduction'},
             {'name': '-a',
              'type': str,
              'dest': 'algorithm',
              'required': True,
              'help': 'classification: kNN, SVM, NN. clustering: kMeans, hierarchical, Gaussian. '
                      'reduction: PCA, features, discriminant'},
             {'name': '-k',
              'type': int,
              'dest': 'k',
              'required': False,
              'help': 'number of nearest neighbors'},
             {'name': '-c',
              'type': int,
              'dest': 'c',
              'required': False,
              'help': 'regularization parameter'},
             {'name': '-l',
              'type': int,
              'dest': 'layers',
              'required': False,
              'help': 'hidden layers sizes'},
             {'name': '-func',
              'type': str,
              'dest': 'func',
              'required': False,
              'help': 'activation function for the hidden layer: ‘identity’, ‘logistic’, ‘tanh’, ‘relu’'},
             {'name': '-n',
              'type': int,
              'dest': 'n',
              'required': False,
              'help': 'number of clusters'},
             {'name': '-cv',
              'type': str,
              'dest': 'cv',
              'required': False,
              'help': 'cross-validation type: Kfold, LOO, random'}]


def read_csv(path):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        raise ex.PathError("there is no file with this name")

    if not os.access(path, os.R_OK):
        raise ex.PermissionError("no permissions to open the file")

    filename, file_extension = os.path.splitext(path)
    if file_extension != ".csv":
        raise ex.FormatError("file must be in csv format")

    dataset = pd.read_csv(path)
    return dataset


def check_args(args):
    args.method = args.method.lower()
    args.algorithm = args.algorithm.lower()

    if args.method not in methods:
        raise ex.ArgumentsError('argument -m must be correct (enter --help to see details)')

    if args.func is not None:
        if args.func not in activation_functions:
            raise ex.ArgumentsError('argument -func must be correct (enter --help to see details)')

    if args.cv is not None:
        if args.cv not in cv_types:
            raise ex.ArgumentsError('argument -cv must be correct (enter --help to see details)')
        args.cv = args.cv.lower()


def create_parser(**kwargs):
    args = kwargs['args']
    parser = argparse.ArgumentParser(description=kwargs['desc'])
    for arg in args:
        parser.add_argument(arg['name'], type=arg['type'], dest=arg['dest'], required=arg['required'], help=arg['help'])
    return parser


def parse_args(parser):
    args = parser.parse_args()
    return args


def run_function(args, data):
    args_dic = args.__dict__
    class_dic = {
        'classification': Classifier,
        'clustering': Clustering,
        'reduction': DimensionReduction
    }

    method = class_dic[args.method](data, args.class_column)

    try:
        function = getattr(method, args.algorithm)
    except AttributeError as ae:
        raise ex.ArgumentsError(ae)

    result = function(**args_dic)
    return result


if __name__ == '__main__':
    parser = create_parser(desc=description, args=arguments)
    args = parse_args(parser)

    try:
        check_args(args)
        data = read_csv(args.path)
        result = run_function(args, data)
        print(result)

    except ex.ArgumentsError as ae:
        print(f"arguments error: {ae.txt} (enter --help for details)")
    except ex.FileError as fe:
        print(f"file error: {fe.txt} (enter --help for details)")
