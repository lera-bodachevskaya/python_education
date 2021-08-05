import numpy as np
from sklearn.metrics import mean_squared_error, accuracy_score, precision_score, recall_score, f1_score, roc_curve, \
    multilabel_confusion_matrix, confusion_matrix


from metric import Metric


if __name__ == '__main__':
    # n = 4 test
    class_names4 = np.array(["dog", "rat", "cat", "snake"])
    original4 = np.array(["dog", "rat", "dog", "cat", "cat", "snake", "snake", "dog", "rat", "dog"])
    # predict4 = np.array(["cat", "snake", "dog", "cat", "dog", "rat", "snake", "snake", "rat", "snake"])
    predict_matrix4 = np.array([[0.1, 0.5, 0.8, 0.3],
                              [0.2, 0.3, 0.5, 0.7],
                              [0.9, 0.3, 0.4, 0.7],
                              [0.2, 0.5, 0.9, 0.1],
                              [0.9, 0.3, 0.4, 0.2],\
                              [0.2, 0.9, 0.3, 0.7],
                              [0.2, 0.3, 0.5, 0.9],
                              [0.2, 0.1, 0.3, 0.9],
                              [0.2, 0.9, 0.3, 0.7],
                              [0.2, 0.1, 0.3, 0.9]
                              ])

    # n = 3 test
    class_names3 = np.array(["dog", "cat", "snake"])
    original3 = np.array(["dog", "dog", "dog", "cat", "cat", "snake", "snake", "dog"])
    # predict3 = np.array(["cat", "snake", "dog", "cat", "dog", "cat", "snake", "snake"])
    predict_matrix3 = np.array([[0.1, 0.5, 0.2],
                                [0.2, 0.5, 0.9],
                                [0.9, 0.5, 0.2],
                                [0.1, 0.9, 0.2],
                                [0.7, 0.1, 0.2],
                                [0.7, 0.9, 0.2],
                                [0.7, 0.2, 0.9],
                                [0.7, 0.2, 0.9]
                                ])

    # n = 2 test
    # class_names2 = np.array(["dog", 'cat'])
    # original2 = np.array(['dog', 'cat', 'dog', 'cat', 'dog'])
    # predict2 = np.array(['cat', 'dog', 'cat', 'cat', 'dog'])
    class_names2 = np.array([1, 0])
    original2 = np.array([1, 0, 1, 0, 1])
    predict2 = np.array([0, 1, 0, 0, 1])
    predict_matrix2 = np.array([[0.4, 0.6],
                                [0.7, 0.3],
                                [0.2, 0.8],
                                [0.4, 0.6],
                                [0.9, 0.1]
                                ])

    class_names = np.array([0, 1, 2, 3])
    actuals = np.array([1, 0, 1, 2, 1, 0])
    predictions = np.array([1, 0, 3, 1, 2, 3])
    predict_matrix = np.array([[0, 1, 0, 0],
                               [1, 0, 0, 0],
                               [0, 0, 0, 1],
                               [0, 1, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]
                               ])

    metric = Metric(class_names, actuals, predict_matrix)

    accuracy = metric.accuracy()
    recall = metric.recall()
    f = metric.f_score()
    print(accuracy_score(actuals, predictions))
    print(confusion_matrix(actuals, predictions))
    # roc = metric.ROC()
    # metric.show_roc_curve(roc)
    # metric.show_matrix()
    print(f"TP: {metric.TP}, TN: {metric.TN}, FP: {metric.FP}, FN: {metric.FN}")
    print(f"Accuracy: {accuracy}, Recall: {recall}, F score: {f}")
    print(f"Confusion matrix:\n {metric.matrix}")
