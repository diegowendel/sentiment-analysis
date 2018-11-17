from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

from src.analyzer.classifier import Classifier
from src.analyzer.preprocessor import PreProcessor
from src.analyzer.sentilex import Sentilex
from src.database.database_mongo import DatabaseMongo
from src.utils.logger import Logger
from src.utils.utils import Tweet
from src.twitter.streamer import TweetStreamer
from src.twitter.twitter_client import TwitterClient

import pandas as pd

mongo = DatabaseMongo()
preprocessor = PreProcessor()
sentilex = Sentilex()

'''
******************************************************************************
********************************** STREAMER **********************************
******************************************************************************
'''
def stream():
    # Criando o objeto TwitterClient que embala a api
    api = TwitterClient()
    # Criando o streamer
    streamer = TweetStreamer()
    streamer.stream(api.get_auth(), api.get_queries())

'''
******************************************************************************
***************************** CLASSIFICADOR MANUAL ***************************
******************************************************************************
'''
def classificar():
    inicio = 1
    fim = 11
    j = 1
    for i in range(inicio, fim):
        tweets = mongo.find_paginated(100, i)

        for tweet in tweets:
            Logger.ok('\n\n----- Classifique: ' + str(j) + ' -----')
            j = j + 1
            # Verifica se é um tweet com texto estendido
            if 'extended_tweet' in tweet:
                print(tweet['extended_tweet']['full_text'])
                classificacao = input("Classificação: ")
                tweet['classificacao'] = classificacao
            else:
                print(tweet['text'])
                classificacao = input("Classificação: ")
                tweet['classificacao'] = classificacao
            mongo.persist_classified(tweet)

def migrar():
    inicio = 1
    fim = 6
    j = 1
    for i in range(inicio, fim):
        tweets = mongo.find_paginated_csv(100, i)

        for tweet in tweets:
            j = j + 1
            print(j)
            classification = tweet['classificacao']
            if classification == 'N':
                tweet['classificacao'] = 'Negativo'
            elif classification == 'P':
                tweet['classificacao'] = 'Positivo'
            else:
                tweet['classificacao'] = 'Neutro'
            mongo.persist_classified(tweet)

def salvar_csv():
    dataset = pd.read_csv('tweets_mg.csv')
    for index, row in dataset.iterrows():
        tweet = {}
        tweet['text'] = row['Text']
        tweet['preprocessado'] = preprocessor.process(row['Text'])
        tweet['classificacao'] = row['Classificacao']
        mongo.persist_classified(tweet)

'''
******************************************************************************
************************* PRÉ-PROCESSAMENTO DE TWEETS ************************
******************************************************************************
'''
def preprocessar():
    inicio = 1
    fim = 150
    j = 1
    for i in range(inicio, fim):
        tweets = mongo.find_paginated_classified(100, i)

        for tweet in tweets:
            print(j)
            j = j + 1
            # Verifica se é um tweet com texto estendido
            if 'extended_tweet' in tweet:
                tweet['preprocessado'] = preprocessor.process(tweet['extended_tweet']['full_text'])
            else:
                tweet['preprocessado'] = preprocessor.process(tweet['text'])
            mongo.persist_classified(tweet)

'''
******************************************************************************
*************************** ANÁLISE DE SENTIMENTOS ***************************
******************************************************************************
'''
def treinar_classificador(mostrarAcuracia):
    dataset = mongo.find_all_classificados()
    tweets = Tweet.get_tweets_processed_texts_from_dataset(dataset)
    # RESET CURSOR
    dataset = mongo.find_all_classificados()
    classes = Tweet.get_tweets_classifications(dataset)

    ''' Classificador '''
    ''' CountVectorizer + Naive Bayes '''
    # vectorizer = CountVectorizer(ngram_range=(1, 2))
    # vectorizer = CountVectorizer(analyzer="word")
    # classifier = MultinomialNB()

    ''' TfidfVectorizer + Support Vector Classification (SVC) '''
    vectorizer = TfidfVectorizer(min_df=0.0, max_df=1.0, sublinear_tf=True, use_idf=True)
    # classifier = SVC(kernel='rbf', C=2.9, gamma=1) # 84,9%
    classifier = SVC(kernel='rbf', C=1.9, gamma=1, random_state=None, verbose=False, shrinking=True)  # 85%

    classificador = Classifier(vectorizer=vectorizer, classifier=classifier)
    classificador.train(tweets=tweets, classifications=classes)

    if mostrarAcuracia:
        resultados = classificador.cross_validation(tweets, classes, 10)
        Logger.ok('ACURÁCIA: ' + str(classificador.accuracy(classes, resultados)))
        classificador.matriz_confusao(classes, resultados)

    return classificador

def analisar_sentimentos():
    classificador = treinar_classificador(mostrarAcuracia=False)

    inicio = 1
    fim = 5000
    j = 1
    for i in range(inicio, fim):
        print(j)
        j = j + 1
        tweets = mongo.find_paginated(100, i)
        tweets_texts = Tweet.get_tweets_texts_from_dataset(tweets)
        resultados = classificador.predict(tweets_texts)

        # RESET CURSOR
        tweets = mongo.find_paginated(100, i)
        for index, tweet in enumerate(tweets):
            tweet['classificacao'] = resultados[index]
            mongo.update(tweet)

'''
******************************************************************************
************************************ MAIN ************************************
******************************************************************************
'''
def main():
    # stream() # Download de tweets
    # classificar() # Classificação manual de tweets

    # salvar_csv()
    # migrar()

    # preprocessar() # Pré-processa os tweets
    analisar_sentimentos() # Analisa os sentimentos dos tweets

    # dicionario = sentilex.get_sentilex_dictionary()
    # inicio = 1
    # fim = 101
    # j = 1
    # for i in range(inicio, fim):
    #     tweets = mongo.find_paginated(100, i)
    #
    #     for tweet in tweets:
    #         print(j)
    #         j = j + 1
    #         # Verifica se é um tweet com texto estendido
    #         if 'extended_tweet' in tweet:
    #             tweet['preprocessado'] = preprocessor.process(tweet['extended_tweet']['full_text'])
    #         else:
    #             tweet['preprocessado'] = preprocessor.process(tweet['text'])
    #         tweet['classificacao'] = sentilex.get_score_phrase(tweet['preprocessado'], dicionario)
    #         mongo.persist_classified(tweet)

if __name__ == "__main__":
    # Calling main function
    main()
