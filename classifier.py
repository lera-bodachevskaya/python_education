from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

import user_exceptions as ex
from validation import Validation


def feature_scaling(X_train, X_test):
    scaler = StandardScaler()
    scaler.fit(X_train)

    train = scaler.transform(X_train)
    test = scaler.transform(X_test)

    return train, test


def predicting(classifier, x_test):
    return classifier.predict(x_test)


def evaluating(y_test, y_pred):
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))


def get_knn_model(k):
    return KNeighborsClassifier(n_neighbors=k)


def get_svm_model(c):
    return svm.SVC(C=c)


def get_nn_model(layers, func):
    return MLPClassifier(hidden_layer_sizes=layers, activation=func)


class Classifier:
    def __init__(self, dataset, right_column, test_size=0.2):
        self.dataset = dataset
        self.test_size = test_size
        self.right_column = right_column

    def preprocessing(self):
        X = self.dataset.iloc[:, :self.right_column].values
        y = self.dataset.iloc[:, self.right_column].values
        return X, y

    def get_params(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size)
        X_train, X_test = feature_scaling(X_train, X_test)

        return X_train, X_test, y_train, y_test

    def knn(self, **kwargs):
        if kwargs['k'] is None:
            raise ex.ArgumentsError('missed -k parameter')

        X, y = self.preprocessing()
        X_train, X_test, y_train, y_test = self.get_params(X, y)

        classifier = get_knn_model(kwargs['k'])
        classifier.fit(X_train, y_train)

        y_predict = predicting(classifier, X_test)
        # evaluating(y_test, y_predict)
        return y_predict

    def svm(self, **kwargs):
        if kwargs['c'] is None:
            c = 1.0
        else:
            c = kwargs['c']

        X, y = self.preprocessing()
        X_train, X_test, y_train, y_test = self.get_params(X, y)

        classifier = get_svm_model(c)
        classifier.fit(X_train, y_train)

        y_predict = classifier.predict(X_test)
        # evaluating(y_test, y_predict)
        return y_predict

    def nn(self, **kwargs):
        if kwargs['layers'] is None:
            layers = (100,)
        else:
            layers = (kwargs['layers'],)

        if kwargs['func'] is None:
            func = 'relu'
        else:
            func = kwargs['func']

        X, y = self.preprocessing()
        X_train, X_test, y_train, y_test = self.get_params(X, y)

        classifier = get_nn_model(layers, func)
        classifier.fit(X_train, y_train)

        y_predict = classifier.predict(X_test)
        # evaluating(y_test, y_predict)
        # self.validation(X, y, classifier)

        if kwargs['cv'] is not None:
            self.validation(X, y, classifier, kwargs['cv'])

        return y_predict

    def validation(self, X, y, model, method):
        val = Validation(X, y, model)

        if method == 'kfold':
            res = val.kfold()
        elif method == 'loo':
            res = val.loo()
        else:
            res = val.random()

        # print(res)
