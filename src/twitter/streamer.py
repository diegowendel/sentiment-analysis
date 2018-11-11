from tweepy import Stream
from tweepy.streaming import StreamListener

from src.database.database_mongo import DatabaseMongo
from src.utils.logger import Logger

mongo = DatabaseMongo()

'''
    Streamer - Tempo real

    Obtém os tweets em tempo real de acordo com o filter, passado como parâmetro.
    Obs: Não é possível excluir os RTs em nível de API com o Streamer, deve ser implementado manualmente esse filtro.
'''
class TweetStreamer(StreamListener):

    def __init__(self):
        Logger.success('\nTSAP streamer started...\n')

    def on_data(self, data):
        mongo.persist_tweet(data)
        return True

    def on_error(self, status_code):
        Logger.error(status_code)

    def stream(self, auth, filter):
        streamer = Stream(auth, self)
        streamer.filter(track=filter, async=True)
