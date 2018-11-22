from random import random, shuffle

from src.analyzer.classifier import Classifier
from src.analyzer.preprocessor import PreProcessor
from src.analyzer.sentilex import Sentilex
from src.database.database_mongo import DatabaseMongo
from src.utils.logger import Logger
from src.utils.utils import Tweet
from src.twitter.streamer import TweetStreamer
from src.twitter.twitter_client import TwitterClient

import pandas as pd

classificador = Classifier()
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
**************************** CLASSIFICADOR MANUAL ****************************
******************************************************************************
'''
def classificar_manualmente():
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
*************************** CLASSIFICAÇÃO SENTILEX ***************************
******************************************************************************

    Classificação de 3000 tweets com base no dicionário SentiLex:
    
    - 1000 positivos
    - 1000 negativos
    - 1000 neutros
'''
def classificar_sentilex():
    dicionario = sentilex.get_sentilex_dictionary()
    inicio = 1
    fim = 201
    j = 1
    positivo = 0
    negativo = 0
    neutro = 0
    for i in range(inicio, fim):
        tweets = mongo.find_paginated(100, i)

        for tweet in tweets:
            print(j)
            j = j + 1
            # Verifica se é um tweet com texto estendido
            if 'extended_tweet' in tweet:
                tweet['preprocessado'] = preprocessor.process(tweet['extended_tweet']['full_text'])
            else:
                tweet['preprocessado'] = preprocessor.process(tweet['text'])
            tweet['classificacao'] = sentilex.get_score_phrase(frase=tweet['preprocessado'], dicionario_palavra_polaridade=dicionario)
            if tweet['classificacao'] == 'Positivo':
                if positivo < 1000:
                    positivo = positivo + 1
                    mongo.persist_classified_sentilex(tweet)
            elif  tweet['classificacao'] == 'Negativo':
                if negativo < 1000:
                    negativo = negativo + 1
                    mongo.persist_classified_sentilex(tweet)
            else:
                if neutro < 1000:
                    neutro = neutro + 1
                    mongo.persist_classified_sentilex(tweet)

def classificar_manualmente_1000():
    j = 1
    positivo = 0
    negativo = 0
    neutro = 0
    tweets = mongo.find_all_classificados()

    tweets_shuffle = []
    for tweet in tweets:
        tweets_shuffle.append(tweet)

    shuffle(tweets_shuffle, random)

    for tweet in tweets_shuffle:
        print(j)
        j = j + 1
        if tweet['classificacao'] == 'Positivo':
            if positivo < 1000:
                positivo = positivo + 1
                mongo.persist_classified_manualmente(tweet)
        elif  tweet['classificacao'] == 'Negativo':
            if negativo < 1000:
                negativo = negativo + 1
                mongo.persist_classified_manualmente(tweet)
        else:
            if neutro < 1000:
                neutro = neutro + 1
                mongo.persist_classified_manualmente(tweet)

'''
******************************************************************************
************************* PRÉ-PROCESSAMENTO DE TWEETS ************************
******************************************************************************
'''
def preprocessar():
    inicio = 1
    fim = 101
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
def treinar_classificador_MultinomialNB(mostrarAcuracia):
    dataset = mongo.find_all_classificados_manualmente()
    tweets = Tweet.get_tweets_processed_texts_from_dataset(dataset)
    # RESET CURSOR
    dataset = mongo.find_all_classificados_manualmente()
    classes = Tweet.get_tweets_classifications(dataset)
    # Treino do classificador
    classificador.treinar_multinomialNB(tweets=tweets, classificacoes=classes, mostrarLogs=mostrarAcuracia)

def treinar_classificador_random_forest(mostrarAcuracia):
    dataset = mongo.find_all_classificados()
    tweets = Tweet.get_tweets_processed_texts_from_dataset(dataset)
    # RESET CURSOR
    dataset = mongo.find_all_classificados()
    classes = Tweet.get_tweets_classifications_as_number(dataset)
    # Treino do classificador
    # classificador.treinar_random_forest(tweets=tweets, classificacoes=classes, mostrarLogs=mostrarAcuracia)
    classificador.preparar_random_forest(tweets=tweets, classificacoes=classes)

def treinar_classificador_svc(mostrarAcuracia):
    dataset = mongo.find_all_classificados()
    tweets = Tweet.get_tweets_processed_texts_from_dataset(dataset)
    # RESET CURSOR
    dataset = mongo.find_all_classificados()
    classes = Tweet.get_tweets_classifications_as_number(dataset)
    # Treino do classificador
    #classificador.treinar_SVC(tweets=tweets, classificacoes=classes, mostrarLogs=mostrarAcuracia)
    classificador.preparar_svc(tweets=tweets, classificacoes=classes)

def analisar_sentimentos():
    treinar_classificador_svc(mostrarAcuracia=True)
    # treinar_classificador_random_forest(mostrarAcuracia=True)

    inicio = 1
    fim = 300000
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
            if resultados[index] == 1:
                tweet['classificacao'] = 'Positivo'
            elif resultados[index] == -1:
                tweet['classificacao'] = 'Negativo'
            else:
                tweet['classificacao'] = 'Neutro'
            mongo.update(tweet)

'''
******************************************************************************
************************************ MAIN ************************************
******************************************************************************
'''
def main():
    # stream() # Download de tweets
    # classificar_manualmente() # Classificação manual de tweets
    # salvar_csv()
    # migrar()

    # classificar_sentilex() # Classificação de tweets com SentiLex
    # classificar_manualmente_1000()
    # preprocessar() # Pré-processa os tweets
    analisar_sentimentos() # Analisa os sentimentos dos tweets

    # treinar_classificador_MultinomialNB(mostrarAcuracia=True)
    # treinar_classificador_random_forest(mostrarAcuracia=True)
    # treinar_classificador_svc(mostrarAcuracia=True)

    #grid_search()

if __name__ == "__main__":
    # Calling main function
    main()
