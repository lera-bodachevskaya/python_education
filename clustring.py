from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture

import user_exceptions as ex


class Clustering:
    def __init__(self, dataset, right_column):
        self.dataset = dataset
        self.right_column = right_column

    def preprocessing(self):
        x = self.dataset.iloc[:, :self.right_column].values
        return x

    def kmeans(self, **kwargs):
        if kwargs['n'] is None:
            raise ex.ArgumentsError('missed -n parameter')

        X = self.preprocessing()
        kmeans = KMeans(n_clusters=kwargs['n'])
        kmeans.fit(X)

        labels = kmeans.predict(X)
        return labels

    def hierarchical(self, **kwargs):
        if kwargs['n'] is None:
            raise ex.ArgumentsError('missed -n parameter')

        X = self.preprocessing()
        clustering = AgglomerativeClustering(n_clusters=kwargs['n']).fit(X)

        labels = clustering.labels_
        return labels

    def gaussian(self, **kwargs):
        if kwargs['n'] is None:
            raise ex.ArgumentsError('missed -n parameter')

        X = self.preprocessing()
        clustering = GaussianMixture(n_components=kwargs['n']).fit(X)

        labels = clustering.predict(X)
        return labels
