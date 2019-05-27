from datetime import date
from typing import List

from sklearn.linear_model import LinearRegression


class Model:

    def __init__(self):
        self._model1 = LinearRegression()
        self._model2 = LinearRegression()

    def fit(self, x_train: List[date], y1_train, y2_train):
        x_train = [[x.toordinal()] for x in x_train]
        self._model1.fit(x_train, y1_train)
        self._model2.fit(x_train, y2_train)

    def predict(self, x_predict: List[date]):
        x_predict = [[x.toordinal()] for x in x_predict]
        y1_predict = self._model1.predict(x_predict)
        y2_predict = self._model2.predict(x_predict)
        return y1_predict, y2_predict
