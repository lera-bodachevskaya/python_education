import collections

import numpy as np
import matplotlib.pyplot as plt


def show_roc_curve(roc, save=False):
    plt.plot(roc['FPR'], roc['TPR'], marker='.', label='ROC')
    plt.plot([0, 1], color='green', linestyle='dashed', label='Random Classifier')
    plt.fill_between(roc['FPR'], roc['TPR'], color='blue', alpha=0.1)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()

    if save:
        plt.savefig('roc-curve.png')

    plt.show()


class Metric:
    def __init__(self, class_names, original, prob_matrix):
        self.class_names = class_names
        self.original = original
        self.elements_num = original.size
        self.class_num = class_names.size
        self.predict = self.get_predict_array(prob_matrix)
        self.matrix, self.TP, self.FN, self.FP, self.TN = self.con_matrix()

    def get_predict_array(self, prob_matrix):
        res = np.array([])
        for i in prob_matrix:
            max_index = np.argmax(i)
            res = np.append(res, self.class_names[max_index])
        return res

    def get_params(self, threshold=0.5, positive_label=1):
        ConfusionMatrix = collections.namedtuple('conf', ['tp', 'fp', 'tn', 'fn'])
        tp = fp = tn = fn = 0
        bool_actuals = [act == positive_label for act in self.original]
        for truth, score in zip(bool_actuals, self.predict):
            if score > threshold:
                if truth:
                    tp += 1
                else:
                    fp += 1
            else:
                if not truth:
                    tn += 1
                else:
                    fn += 1
        res = ConfusionMatrix(tp, fp, tn, fn)
        return res

    def con_matrix(self):
        matrix = np.zeros((self.class_num, self.class_num))

        for i in range(self.elements_num):
            if self.original[i] == self.predict[i]:
                class_index = np.where(self.class_names == self.original[i])[0][0]
                matrix[class_index][class_index] += 1
            else:
                original_index = np.where(self.class_names == self.original[i])[0][0]
                pred_index = np.where(self.class_names == self.predict[i])[0][0]
                matrix[original_index][pred_index] += 1

        TP = matrix[0][0]
        FN = np.sum(matrix[0][1:])
        FP = np.sum(matrix[1:, 0])
        TN = np.sum(matrix[1:, 1:])

        return matrix, TP, FN, FP, TN

    def show_matrix(self, save=False):
        plt.imshow(self.matrix)
        plt.colorbar()

        if save:
            plt.savefig('matrix.png')

        plt.show()

    def calc_matrix(self, threshold=0.5, positive_label=1):
        ConfusionMatrix = collections.namedtuple('conf', ['tp', 'fp', 'tn', 'fn'])
        tp = fp = tn = fn = 0
        bool_actuals = [act == positive_label for act in self.original]
        for truth, score in zip(bool_actuals, self.predict):
            if score > threshold:
                if truth:
                    tp += 1
                else:
                    fp += 1
            else:
                if not truth:
                    tn += 1
                else:
                    fn += 1
        return ConfusionMatrix(tp, fp, tn, fn)

    def MSE(self):
        res = np.sum((self.original - self.predict) ** 2) / self.elements_num
        return res

    def accuracy(self):
        equal = self.original == self.predict
        res = np.count_nonzero(equal) / self.elements_num
        return res

    def precision(self):
        res = self.TP / (self.TP + self.FP) if (self.TP + self.FP) != 0 else 0
        return res

    def recall(self):
        res = self.TP / (self.TP + self.FN) if (self.TP + self.FN) != 0 else 0
        return res

    def f_score(self):
        p = self.precision()
        r = self.recall()
        res = 2 * (p * r) / (p + r) if (p + r) != 0 else 0
        return res

    def FPR(self, matrix):
        return matrix.fp / (matrix.fp + matrix.tn) if (matrix.fp + matrix.tn) != 0 else 0

    def TPR(self, matrix):
        return matrix.tp / (matrix.tp + matrix.fn) if (matrix.tp + matrix.fn) != 0 else 0

    def ROC(self):
        return self.apply(FPR=self.FPR, TPR=self.TPR)

    def apply(self, **kwargs):
        low = min(self.predict)
        high = max(self.predict)
        step = (abs(low) + abs(high)) / 1000

        thresholds = np.arange(low - step, high + step, step)
        con_matrix_list = []
        for threshold in thresholds:
            con_matrix_list.append(self.calc_matrix(threshold))

        results = {fname: list(map(fxn, con_matrix_list)) for fname, fxn in kwargs.items()}
        results["THR"] = thresholds
        return results