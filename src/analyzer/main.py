from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from src.analyzer.classifier import Classifier
from src.analyzer.preprocessor import PreProcessor
from src.database.database_mongo import DatabaseMongo
from src.utils.logger import Logger
from src.utils.utils import Tweet
from src.twitter.streamer import TweetStreamer
from src.twitter.twitter_client import TwitterClient

import pandas as pd

mongo = DatabaseMongo()
preprocessor = PreProcessor()

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
def analisar_sentimentos():
    dataset = mongo.find_all_classificados()
    tweets = Tweet.get_tweets_texts_from_dataset(dataset)
    # RESET CURSOR
    dataset = mongo.find_all_classificados()
    classes = Tweet.get_tweets_classifications(dataset)

    ''' Classificador '''
    vectorizer = CountVectorizer(analyzer="word")
    classifier = MultinomialNB()
    classificador = Classifier(vectorizer=vectorizer, classifier=classifier)
    classificador.train(tweets=tweets, classifications=classes)

    resultados = classificador.cross_validation(tweets, classes, 10)
    print('accuracy', classificador.accuracy(classes, resultados))

    classificador.matriz_confusao(classes, resultados)

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

    preprocessar() # Pré-processa os tweets
    analisar_sentimentos() # Analisa os sentimentos dos tweets

if __name__ == "__main__":
    # Calling main function
    main()
