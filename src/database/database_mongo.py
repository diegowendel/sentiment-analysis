import json

from pymongo import MongoClient

from src.utils.logger import Logger
from src.utils.utils import Tweet

class DatabaseMongo(object):

    host='localhost'
    port=27017
    db='tsap'

    def __init__(self):
        '''
            Retorna uma instância de uma conexão do mongodb para a coleção de tweets
        '''
        client = MongoClient(self.host, self.port)
        database = client['tsap']
        self.collection = database['tweets']

    def find(self):
        tweets = self.collection.find({})
        return tweets

    def update(self, tweet):
        self.collection.save(tweet)

    def persist_tweet(self, tweet):
        try:
            tweet_json = json.loads(tweet)
            if (Tweet.isRetweet(tweet_json)):
                Logger.warn('Ignorando RT...\n')
            else:
                self.collection.insert(tweet_json)
                Logger.ok(tweet)

        except BaseException as e:
            Logger.error('Falha ao salvar tweet\nStacktrace: {}'.format(e))
