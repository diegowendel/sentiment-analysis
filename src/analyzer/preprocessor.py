import re
import nltk

from string import punctuation
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

#nltk.download('rslp')
#nltk.download('stopwords')
#nltk.download('punkt')

class PreProcessor(object):

    stemmer = nltk.stem.RSLPStemmer()
    tokenizer = TweetTokenizer(reduce_len=True, preserve_case=False)
    special_char = ['$', '%', '&', '*', '(', ')', '_', '-', '+', '=', '{', '[', '}', ']', '~', '.', ',', ';', 'º', 'ª', '°', '¹', '²', '³']

    def process(self, tweet):
        tweet = self.to_lower(tweet)
        tweet = self.remove_links(tweet)
        tweet = self.remove_mentions(tweet)
        tweet = self.remove_hashtags(tweet)
        tweet = self.remove_numbers(tweet)
        tweet = self.replace_three_or_more(tweet)

        palavras = self.tokenizer.tokenize(tweet)
        palavras = self.remove_punctuation(palavras)
        # palavras = self.remove_stopwords(palavras)

        palavras_processadas = []
        for palavra in palavras:
            # Replace emoji
            if len(palavra) <= 3:
                # replace good emoticons
                palavra = re.sub('[:;=8][\-=^*\']?[)\]Dpb}]|[cCqd{(\[][\-=^*\']?[:;=8]', 'bom', palavra)
                # replace bad emoticons
                palavra = re.sub('[:;=8][\-=^*\']?[(\[<{cC]|[D>)\]}][\-=^*\']?[:;=8]', 'ruim', palavra)

            # Stemming
            # palavra = self.stemmer.stem(palavra)

            # Remove small words
            if len(palavra) <= 2:
                palavra = ''

            for s in self.special_char:
                palavra = palavra.replace(s, '')

            palavras_processadas.append(palavra)

        tweet = ' '.join(palavras_processadas)
        tweet = self.remove_duplicated_spaces(tweet)
        return tweet

    def to_lower(self, tweet):
        return tweet.lower()

    def remove_links(self, tweet):
        # http matches literal characters and \S+ matches all non-whitespace characters (the end of the url)
        return re.sub("http\S+", "", tweet)

    def remove_mentions(self, tweet):
        return re.sub("@\S+", "", tweet)

    def remove_hashtags(self, tweet):
        return re.sub("#", "", tweet)

    def remove_numbers(self, tweet):
        return re.sub("\d+", "", tweet)

    def replace_three_or_more(self, tweet):
        # pattern to look for three or more repetitions of any character, including newlines
        pattern = re.compile(r"(.)\1{2,}", re.DOTALL)
        return pattern.sub(r"\1\1", tweet)

    def remove_duplicated_spaces(self, tweet):
        tweet = tweet.strip()  # Remove spaces before and after string
        return re.sub(" +", " ", tweet)

    def remove_stopwords(self, palavras):
        return [palavra for palavra in palavras if palavra not in stopwords.words('portuguese')]

    def remove_punctuation(self, palavras):
        return [palavra for palavra in palavras if palavra not in list(punctuation)]
