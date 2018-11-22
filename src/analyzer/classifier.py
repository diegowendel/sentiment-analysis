from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, HashingVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from sklearn import metrics
from pprint import pprint
from time import time

from src.utils.logger import Logger

import pandas as pd
import numpy as np

class Classifier(object):

    def __init__(self):
        self.classificador = SVC(kernel='rbf', C=5, gamma=0.1)

    def treinar_multinomialNB(self, tweets, classificacoes, mostrarLogs):
        # create training and testing vars
        x_train, x_test, y_train, y_test = train_test_split(tweets, classificacoes, test_size=0.20)
        x_train = np.array(x_train)
        x_test = np.array(x_test)
        y_train = np.array(y_train)
        y_test = np.array(y_test)

        pipeline = Pipeline([
            # ('vect', CountVectorizer()),
            # ('vect', CountVectorizer(ngram_range=(1, 2))),
            # ('tfidf', TfidfTransformer(use_idf=True, smooth_idf=True)),
            ('vect', HashingVectorizer(non_negative=True)),
            ('clf', MultinomialNB(alpha=1))
        ])

        pipeline.fit(x_train, y_train)
        mensagem_treino = '\nCLASSIFICADOR MULTINOMIALNB TREINADO EM ' + str(len(x_train)) + ' EXEMPLOS\n'
        Logger.ok(mensagem_treino)

        if mostrarLogs:
            resultados_cv = cross_val_score(pipeline, tweets, classificacoes, cv=10, n_jobs=-1)
            predictions = pipeline.predict(x_test)
            mensagem_acuracia = "ACURÁCIA: %0.4f" % (resultados_cv.mean())
            Logger.ok(mensagem_acuracia)
            print(metrics.classification_report(y_test, predictions), '')

            matriz_confusao = pd.crosstab(y_test, predictions, rownames=['Real'], colnames=['Predito'], margins=True)
            Logger.ok('\nMATRIZ DE CONFUSÃO\n')
            print(matriz_confusao)

    def treinar_SVC(self, tweets, classificacoes, mostrarLogs):
        # create training and testing vars
        x_train, x_test, y_train, y_test = train_test_split(tweets, classificacoes, test_size=0.20)
        x_train = np.array(x_train)
        x_test = np.array(x_test)
        y_train = np.array(y_train)
        y_test = np.array(y_test)

        Cs = [5, 5.2, 5.4, 5.6, 5.8, 6]
        gammas = [0.08, 0.09, 0.1, 0.12, 0.14, 0.16]
        param_grid = {'clf__C': Cs, 'clf__gamma': gammas}

        pipeline = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer(use_idf=True, smooth_idf=True)),
            ('clf', SVC(kernel='rbf'))
        ])

        grid_search = GridSearchCV(pipeline, param_grid, cv=10, verbose=2, n_jobs=-1)

        start = time()
        grid_search.fit(x_train, y_train)
        print("\nGridSearchCV took %.2f seconds"
              " parameter settings." % ((time() - start)))
        print("\nBest Score = " + str(grid_search.best_score_))
        print("\nBest Parameters = " + str(grid_search.best_params_))

        Logger.ok("\nTestes comparativos")
        base_model = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer(use_idf=True, smooth_idf=True)),
            ('clf', SVC(kernel='rbf', C=5, gamma=0.1))
        ])
        base_model.fit(x_train, y_train)
        base_accuracy = cross_val_score(base_model, tweets, classificacoes, cv=10, n_jobs=-1)
        resultados_base_model = base_model.predict(x_test)
        print('acuracias')
        print(base_accuracy)
        mensagem_acuracia_10_fold = "\nModelo base - ACURÁCIA 10-fold: %0.4f" % (base_accuracy.mean())
        Logger.ok(mensagem_acuracia_10_fold)
        print(metrics.classification_report(y_test, resultados_base_model), '')

        matriz_confusao_base_model = pd.crosstab(y_test, resultados_base_model, rownames=['Real'], colnames=['Predito'], margins=True)
        Logger.ok('\nMATRIZ DE CONFUSÃO\n')
        print(matriz_confusao_base_model)

        best_grid = grid_search.best_estimator_
        grid_accuracy = cross_val_score(best_grid, tweets, classificacoes, cv=10, n_jobs=-1)
        resultados_grid = best_grid.predict(x_test)
        print('acuracias')
        print(grid_accuracy)
        mensagem_acuracia_10_fold_grid = "\nModelo gridCV - ACURÁCIA 10-fold: %0.4f" % (grid_accuracy.mean())
        Logger.ok(mensagem_acuracia_10_fold_grid)
        print(metrics.classification_report(y_test, resultados_grid), '')

        matriz_confusao_grid = pd.crosstab(y_test, resultados_grid, rownames=['Real'], colnames=['Predito'], margins=True)
        Logger.ok('\nMATRIZ DE CONFUSÃO\n')
        print(matriz_confusao_grid)

    def preparar_svc(self, tweets, classificacoes):
        # create training and testing vars
        x_train, x_test, y_train, y_test = train_test_split(tweets, classificacoes, test_size=0.20)
        x_train = np.array(x_train)
        x_test = np.array(x_test)
        y_train = np.array(y_train)
        y_test = np.array(y_test)

        self.classificador = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer(use_idf=True, smooth_idf=True)),
            ('clf', SVC(kernel='rbf', C=5, gamma=0.1))
        ])
        self.classificador.fit(x_train, y_train)
        mensagem_treino = '\nCLASSIFICADOR SVC TREINADO EM ' + str(len(x_train)) + ' EXEMPLOS\n'
        Logger.ok(mensagem_treino)
        accuracy = cross_val_score(self.classificador, tweets, classificacoes, cv=10, n_jobs=-1)
        mensagem_acuracia_10_fold = "\nModelo SVC - ACURÁCIA 10-fold: %0.4f" % (accuracy.mean())
        Logger.ok(mensagem_acuracia_10_fold)

    def predict(self, tweets):
        return self.classificador.predict(tweets)

    def preparar_random_forest(self, tweets, classificacoes):
        # create training and testing vars
        x_train, x_test, y_train, y_test = train_test_split(tweets, classificacoes, test_size=0.20)
        x_train = np.array(x_train)
        x_test = np.array(x_test)
        y_train = np.array(y_train)
        y_test = np.array(y_test)

        self.classificador = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer(use_idf=True, smooth_idf=True)),
            ('clf', RandomForestClassifier(n_estimators=800, min_samples_split=5, min_samples_leaf=1, max_features='sqrt', max_depth=90, bootstrap=False))
        ])
        self.classificador.fit(x_train, y_train)
        mensagem_treino = '\nCLASSIFICADOR RF TREINADO EM ' + str(len(x_train)) + ' EXEMPLOS\n'
        Logger.ok(mensagem_treino)
        accuracy = cross_val_score(self.classificador, tweets, classificacoes, cv=10, n_jobs=-1)
        mensagem_acuracia_10_fold = "\nModelo RF - ACURÁCIA 10-fold: %0.4f" % (accuracy.mean())
        Logger.ok(mensagem_acuracia_10_fold)

    def treinar_random_forest(self, tweets, classificacoes, mostrarLogs):
        # create training and testing vars
        x_train, x_test, y_train, y_test = train_test_split(tweets, classificacoes, test_size=0.20)
        x_train = np.array(x_train)
        x_test = np.array(x_test)
        y_train = np.array(y_train)
        y_test = np.array(y_test)

        # Number of trees in random forest
        n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num=10)]
        # Number of features to consider at every split
        max_features = ['auto', 'sqrt']
        # Maximum number of levels in tree
        max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
        max_depth.append(None)
        # Minimum number of samples required to split a node
        min_samples_split = [2, 5, 10]
        # Minimum number of samples required at each leaf node
        min_samples_leaf = [1, 2, 4]
        # Method of selecting samples for training each tree
        bootstrap = [True, False]
        # Create the random grid
        random_grid = {'clf__n_estimators': n_estimators,
                       'clf__max_features': max_features,
                       'clf__max_depth': max_depth,
                       'clf__min_samples_split': min_samples_split,
                       'clf__min_samples_leaf': min_samples_leaf,
                       'clf__bootstrap': bootstrap}
        pprint(random_grid)

        pipeline = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer(use_idf=True, smooth_idf=True)),
            ('clf', RandomForestClassifier())
        ])

        # Random search of parameters, using 3 fold cross validation,
        # search across 100 different combinations, and use all available cores
        rf_random = RandomizedSearchCV(pipeline, param_distributions=random_grid, n_iter=100, cv=3, verbose=2, random_state=42, n_jobs=-1)

        start = time()
        rf_random.fit(x_train, y_train)
        print(rf_random.best_params_)
        print("\nRandomizedSearchCV took %.2f seconds for %d candidates"
              " parameter settings." % ((time() - start), 100))
        print("\nBest Score = " + str(rf_random.best_score_))
        print("\nBest Parameters = " + str(rf_random.best_params_))

        Logger.ok("\nTestes comparativos")
        base_model = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer(use_idf=True, smooth_idf=True)),
            ('clf', RandomForestClassifier(n_estimators=10, random_state=42))
        ])
        base_model.fit(x_train, y_train)
        base_accuracy = cross_val_score(base_model, tweets, classificacoes, cv=10, n_jobs=-1)
        resultados_base_model = base_model.predict(x_test)
        print('acuracias')
        print(base_accuracy)
        mensagem_acuracia_10_fold = "\nModelo base - ACURÁCIA 10-fold: %0.4f" % (base_accuracy.mean())
        Logger.ok(mensagem_acuracia_10_fold)
        print(metrics.classification_report(y_test, resultados_base_model), '')

        matriz_confusao_base_model = pd.crosstab(y_test, resultados_base_model, rownames=['Real'], colnames=['Predito'], margins=True)
        Logger.ok('\nMATRIZ DE CONFUSÃO\n')
        print(matriz_confusao_base_model)

        best_random = rf_random.best_estimator_
        random_accuracy = cross_val_score(best_random, tweets, classificacoes, cv=10, n_jobs=-1)
        resultados_best_random = best_random.predict(x_test)
        print('acuracias')
        print(random_accuracy)
        mensagem_acuracia_10_fold_rand = "\nModelo randomCV - ACURÁCIA 10-fold: %0.4f" % (random_accuracy.mean())
        Logger.ok(mensagem_acuracia_10_fold_rand)
        print(metrics.classification_report(y_test, resultados_best_random), '')

        matriz_confusao_best_random = pd.crosstab(y_test, resultados_best_random, rownames=['Real'], colnames=['Predito'], margins=True)
        Logger.ok('\nMATRIZ DE CONFUSÃO\n')
        print(matriz_confusao_best_random)
