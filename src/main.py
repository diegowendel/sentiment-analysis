from src.twitter_client import TwitterClient
from src.database import Database
from tweepy import Stream
from tweepy.streaming import StreamListener

database = Database()

''' 
    Streamer - Tempo real
    
    Obtém os tweets em tempo real de acordo com o filter, passado como parâmetro.
    Obs: Não é possível excluir os RTs em nível de API com o Streamer, deve ser implementado manualmente esse filtro.
'''
class TweetStreamer(StreamListener):
    def on_data(self, raw_data):
        database.persist_tweet(raw_data)
        return True

    def on_error(self, status_code):
        print(status_code)

    def stream(self, auth, filter):
        streamer = Stream(auth, self)
        streamer.filter(track=filter, async=True)

'''
    Main
'''
def main():
    # Prepara o banco de dados para receber os tweets
    database.create_table_tweets()

    # Criando o objeto TwitterClient que embala a api
    api = TwitterClient()

    tweets = api.get_tweets('bolsonaro')
    for tweet in tweets:
        database.persist_tweet(tweet)

    # Criando o streamer
    #streamer = TweetStreamer()
    #streamer.stream(api.get_auth(), ['jair bolsonaro', 'bolsonaro', 'lula'])

    print('terminated')

if __name__ == "__main__":
    # Calling main function
    main()
