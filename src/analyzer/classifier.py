from sklearn.model_selection import cross_val_predict
from sklearn import metrics

from src.utils.logger import Logger

import pandas as pd

class Classifier(object):

    def __init__(self, classifier, vectorizer):
        self.classifier = classifier
        self.vectorizer = vectorizer

    def train(self, tweets, classifications):
        freq_tweets = self.vectorizer.fit_transform(tweets)
        self.classifier.fit(freq_tweets, classifications)
        mensagem = '\nCLASSIFICADOR TREINADO EM ' + str(len(classifications)) + ' EXEMPLOS\n'
        Logger.ok(mensagem)

    def predict(self, tweets):
        freq_testes = self.vectorizer.transform(tweets)
        return self.classifier.predict(freq_testes)

    def cross_validation(self, tweets, classifications, kfolds):
        freq_tweets = self.vectorizer.transform(tweets)
        resultados = cross_val_predict(self.classifier, freq_tweets, classifications, cv=kfolds)
        return resultados

    def accuracy(self, classifications, resultados_cross_val):
        accuracy = metrics.accuracy_score(classifications, resultados_cross_val)
        return accuracy

    def matriz_confusao(self, classifications, resultados_cross_val):
        matriz = pd.crosstab(classifications, resultados_cross_val, rownames=['Real'], colnames=['Predito'], margins=True)
        Logger.ok('\nMATRIZ DE CONFUSÃO\n')
        print(matriz, '')
