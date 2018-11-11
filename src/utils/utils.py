'''
    Tweet - Classe utilitária para trabalhar com tweets
'''

class Tweet(object):

    def is_retweet(tweet_json):
        return 'RT @' in tweet_json['text']

    def get_tweets_texts_from_dataset(dataset):
        tweets = []
        for tweet in dataset:
            tweets.append(tweet['preprocessado'])
        return tweets

    def get_tweets_classifications(dataset):
        classifications = []
        for tweet in dataset:
            classifications.append(tweet['classificacao'])
        return classifications
