from tweepy import Stream
from tweepy.streaming import StreamListener

from src.analyzer.preprocessor import PreProcessor
from src.database.database_mongo import DatabaseMongo
from src.twitter.twitter_client import TwitterClient
from src.utils.logger import Logger
from src.analyzer.classifier import Classifier
from src.utils.utils import Tweet

mongo = DatabaseMongo()
preprocessor = PreProcessor()

queries = ['@alvarodias_', 'alvaro dias', 'alvaro',
           '@CaboDaciolo', 'cabo daciolo', 'daciolo',
           '@cirogomes', 'ciro gomes', 'ciro',
           '@Haddad_Fernando', 'fernando haddad', 'haddad',
           '@geraldoalckmin', 'geraldo alckmin', 'alckmin',
           '@GuilhermeBoulos', 'guilherme boulos', 'boulos',
           '@meirelles', 'henrique meirelles', 'meirelles',
           '@jairbolsonaro', 'jair bolsonaro', 'bolsonaro',
           '@joaoamoedonovo', 'joao amoedo', 'amoedo',
           '@joaogoulart54', 'joao goulart', 'goulart',
           '@Eymaeloficial', 'jose maria eymael', 'eymael',
           '@LulaOficial', 'luiz inácio lula da silva', 'lula',
           '@MarinaSilva', 'marina silva', 'marina',
           '@verapstu', 'vera lucia', 'vera']

'''
******************************************************************************
********************************** STREAMER **********************************
******************************************************************************
 
Streamer - Tempo real
    
Obtém os tweets em tempo real de acordo com o filter, passado como parâmetro.
Obs: Não é possível excluir os RTs em nível de API com o Streamer, deve ser implementado manualmente esse filtro.

'''
class TweetStreamer(StreamListener):
    def __init__(self):
        Logger.success('TSAP streamer started...')

    def on_data(self, data):
        mongo.persist_tweet(data)
        return True

    def on_error(self, status_code):
        Logger.error(status_code)

    def stream(self, auth, filter):
        streamer = Stream(auth, self)
        streamer.filter(track=filter, async=True)

'''
******************************************************************************
******************************** CLASSIFICADOR *******************************
******************************************************************************
'''
def classificar():
    inicio = 1
    fim = 21
    j = 1
    for i in range(inicio, fim):
        tweets = mongo.find_paginated(100, i)

        for tweet in tweets:
            Logger.ok(' ----- Classifique ----- ')
            print(j)
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
            mongo.persist_treino(tweet)

def preprocessar():
    inicio = 1
    fim = 21
    j = 1
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
            mongo.persist_treino(tweet)

'''
******************************************************************************
************************************ MAIN ************************************
******************************************************************************
'''
def main():
    #classifier.classify()

    # Criando o objeto TwitterClient que embala a api
    api = TwitterClient()

    # Criando o streamer
    #streamer = TweetStreamer()
    #streamer.stream(api.get_auth(), queries)
    j=1
    dataset = mongo.find_all_classificados()
    tweets = Tweet.get_tweets_texts_from_dataset(dataset)
    classifications = Tweet.get_tweets_classifications(dataset)
    for tweet in tweets:
        print(j)
        j = j + 1
        print(tweet)

    #preprocessar()
    Logger.success('FINALIZADO!!!')
'''
    inicio = 1
    #fim = 144369
    fim = 2

    for i in range(inicio, fim):
        tweets = skiplimit(100, i)

        for tweet in tweets:
            print('tweeeet')
            # Verifica se é um tweet com texto estendido
            if 'extended_tweet' in tweet:
                tweet['texto_full_processado'] = preprocessor.process(tweet['extended_tweet']['full_text'])
            tweet['texto_processado'] = preprocessor.process(tweet['text'])
            mongo.update(tweet)'''

if __name__ == "__main__":
    # Calling main function
    main()
