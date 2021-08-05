import numpy as np
from sklearn.model_selection import KFold, cross_validate, LeaveOneOut, StratifiedShuffleSplit


class Validation:
    def __init__(self, X, y, model):
        self.X = X
        self.y = y
        self.model = model

    def get_scores(self, cv, scoring='accuracy', n_jobs=-1):
        scores = cross_validate(self.model, self.X, self.y, scoring=scoring, cv=cv, n_jobs=n_jobs)
        return scores

    def kfold(self):
        cv = KFold(n_splits=10, random_state=1, shuffle=True)
        scores = self.get_scores(cv)
        return scores

    def loo(self):
        cv = LeaveOneOut()
        scores = self.get_scores(cv)
        return scores

    def random(self):
        cv = StratifiedShuffleSplit()
        scores = self.get_scores(cv)
        return scores
