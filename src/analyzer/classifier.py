import pandas as pd

class Classifier(object):

    def __init__(self, classifier, vectorizer):
        self.classifier = classifier
        self.vectorizer = vectorizer

    def train(self, x_train, y_train):
        train_vectors = self.vectorizer.fit_transform(x_train)
        self.classifier.fit(train_vectors, y_train)
        print('classifier trained on', len(y_train), 'examples')

    def classify(self):
        print('teste')
        dataset = pd.read_csv('tweets_mg.csv')
        print(dataset.count())