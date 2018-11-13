from src.analyzer.preprocessor import PreProcessor

'''
    Tweet - Classe utilitária para trabalhar com tweets
'''

preprocessor = PreProcessor()

class Tweet(object):

    def is_retweet(tweet_json):
        return 'RT @' in tweet_json['text']

    def get_tweets_texts_from_dataset(dataset):
        tweets = []
        for tweet in dataset:
            if 'extended_tweet' in tweet:
                tweets.append(preprocessor.process(tweet['extended_tweet']['full_text']))
            else:
                tweets.append(preprocessor.process(tweet['text']))
        return tweets

    def get_tweets_processed_texts_from_dataset(dataset):
        tweets = []
        for tweet in dataset:
            tweets.append(tweet['preprocessado'])
        return tweets

    def get_tweets_classifications(dataset):
        classifications = []
        for tweet in dataset:
            classifications.append(tweet['classificacao'])
        return classifications
