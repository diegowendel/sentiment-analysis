import re

from nltk.tokenize import TweetTokenizer

class PreProcessor(object):

    tokenizer = TweetTokenizer(reduce_len=True, preserve_case=False)
    special_char = ['$', '%', '&', '!', '*', '(', ')', '_', '-', '+', '=', '{', '[', '}', ']', '~', '.', ',', ';']

    def process(self, tweet):
        tweet = self.remove_links(tweet)
        tweet = self.remove_hashtags(tweet)
        return tweet

    # Remove links
    def remove_links(self, tweet):
        # http matches literal characters and \S+ matches all non-whitespace characters (the end of the url)
        return re.sub("http\S+", "", tweet)

    # Remove hashtags
    def remove_hashtags(self, tweet):
        return re.sub("#\S*", "", tweet)

    '''
    def remove_mentions(self, tweet):
        return re.sub("@[A-Za-z0-9_]+", "", tweet)
    '''
