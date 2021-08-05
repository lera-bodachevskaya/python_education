from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA


class DimensionReduction:
    def __init__(self, dataset, right_column):
        self.dataset = dataset
        self.right_column = right_column

    def preprocessing(self):
        X = self.dataset.iloc[:, :self.right_column].values
        y = self.dataset.iloc[:, self.right_column].values
        return X, y

    def discriminant(self, **kwargs):
        X, y = self.preprocessing()
        solver = 'svd'
        tol = 0.0001

        clf = LinearDiscriminantAnalysis(solver=solver, tol=tol)
        fit = clf.fit(X, y)

        return fit

    def features(self, **kwargs):
        X, Y = self.preprocessing()
        model = LogisticRegression()
        estimator = 3

        rfe = RFE(model, estimator)
        fit = rfe.fit(X, Y)

        print("Num Features: %s" % fit.n_features_)
        print("Selected Features: %s" % fit.support_)
        print("Feature Ranking: %s" % fit.ranking_)

        return fit

    def pca(self, **kwargs):
        X, Y = self.preprocessing()
        n = 2

        pca = PCA(n_components=n)
        fit = pca.fit(X)

        return fit
