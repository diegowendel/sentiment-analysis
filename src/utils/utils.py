'''
    Tweet - Classe utilitária para trabalhar com tweets
'''

class Tweet(object):

    def isRetweet(tweet_json):
        return 'RT @' in tweet_json['text']
