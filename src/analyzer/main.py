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
    fim = 21
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

'''
******************************************************************************
************************* PRÉ-PROCESSAMENTO DE TWEETS ************************
******************************************************************************
'''
def preprocessar():
    inicio = 1
    fim = 21
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
    '''dataset = mongo.find_all_classificados()
        tweets = Tweet.get_tweets_texts_from_dataset(dataset)
        # RESET CURSOR
        dataset = mongo.find_all_classificados()
        classifications = Tweet.get_tweets_classifications(dataset)'''

    dataset = pd.read_csv('tweets_mg.csv')
    dataset.count()
    tweets = dataset['Text'].values
    classes = dataset['Classificacao'].values

    ''' Classificador '''
    vectorizer = CountVectorizer(analyzer="word")
    classifier = MultinomialNB()
    classificador = Classifier(vectorizer=vectorizer, classifier=classifier)
    classificador.train(tweets=tweets, classifications=classes)

    testes = ['Esse governo está no início, vamos ver o que vai dar',
              'Estou muito feliz com o governo de Minas esse ano',
              'O estado de Minas Gerais decretou calamidade financeira!!!',
              'A segurança desse país está deixando a desejar',
              'O governador de Minas é do PT']
    t = classificador.predict(testes)
    print(t)

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
    classificar() # Classificação manual de tweets
    # preprocessar() # Pré-processa os tweets
    # analisar_sentimentos() # Analisa os sentimentos dos tweets

if __name__ == "__main__":
    # Calling main function
    main()
