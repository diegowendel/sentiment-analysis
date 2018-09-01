from tweepy import Stream
from tweepy.streaming import StreamListener

from src.database.database_mongo import DatabaseMongo
from src.twitter.twitter_client import TwitterClient
from src.utils.logger import Logger

mongo = DatabaseMongo()

''' 
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
    Main
'''
def main():
    # Criando o objeto TwitterClient que embala a api
    api = TwitterClient()

    '''tweets = api.get_tweets('bolsonaro')
    for tweet in tweets:
        database.persist_tweet(tweet)'''

    # Criando o streamer
    streamer = TweetStreamer()
    streamer.stream(api.get_auth(), ['jair bolsonaro', 'bolsonaro', 'lula'])

if __name__ == "__main__":
    # Calling main function
    main()
