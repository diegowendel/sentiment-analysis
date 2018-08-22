from twitter_client import TwitterClient
from database import Database
from tweepy import Stream
from tweepy.streaming import StreamListener

'''def openCSV(tweets):
    with open('tweetsxs.csv', 'w') as csv_file:
        csv_file.write('Tweet, Data\n')
        for tweet in tweets:
            csv_file.write('%s,%s\n' % (tweet.text.encode("utf8"), tweet.created_at))'''

database = Database()

class TweetStreamer(StreamListener):
    def on_data(self, raw_data):
        database.persist_tweet(raw_data)
        return True

    def on_error(self, status_code):
        print(status_code)

    def stream(self, auth):
        streamer = Stream(auth, self)
        streamer.filter(track=['jair bolsonaro', 'bolsonaro', 'lula', 'pt'])

def main():
    # Prepara o banco de dados para receber os tweets
    database.create_table_tweets()

    # Criando o objeto TwitterClient que embala a api
    api = TwitterClient()

    # Criando o streamer
    streamer = TweetStreamer()
    streamer.stream(api.get_auth())

if __name__ == "__main__":
    # Calling main function
    main()
