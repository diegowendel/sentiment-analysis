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

    # UniLex: Método Léxico para Análise de Sentimentos Textuais sobre Conteúdo de Tweets em Português Brasileiro*
    stoplist_uniLex = ['a', 'agora', 'ainda', 'alguem', 'algum', 'alguma', 'algumas', 'alguns', 'ampla', 'amplas', 'amplo', 'amplos',
     'ante', 'antes', 'ao', 'aos', 'apos', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aquilo', 'as', 'ate', 'atraves',
     'cada', 'coisa', 'coisas', 'com', 'como', 'contra', 'contudo', 'da', 'daquele', 'daqueles', 'das', 'de', 'dela',
     'delas', 'dele', 'deles', 'depois', 'dessa', 'dessas', 'desse', 'desses', 'desta', 'destas', 'deste', 'deste',
     'destes', 'deve', 'devem', 'devendo', 'dever', 'devera', 'deverao', 'deveria', 'deveriam', 'devia', 'deviam',
     'disse', 'disso', 'disto', 'dito', 'diz', 'dizem', 'do', 'dos', 'e', 'ela', 'elas', 'ele', 'eles', 'em',
     'enquanto', 'entre', 'era', 'essa', 'essas', 'esse', 'esses', 'esta', 'estamos', 'estao', 'estas', 'estava',
     'estavam', 'estavamos', 'este', 'estes', 'estou', 'eu', 'fazendo', 'fazer', 'feita', 'feitas', 'feito', 'feitos',
     'foi', 'for', 'foram', 'fosse', 'fossem', 'grande', 'grandes', 'ha', 'isso', 'isto', 'ja', 'la', 'lhe', 'lhes',
     'lo', 'mas', 'me', 'mesma', 'mesmas', 'mesmo', 'mesmos', 'meu', 'meus', 'minha', 'minhas', 'muita', 'muitas',
     'muito', 'muitos', 'na', 'nao', 'nas', 'nem', 'nenhum', 'nessa', 'nessas', 'nesta', 'nestas', 'ninguem', 'no',
     'nos', 'nossa', 'nossas', 'nosso', 'nossos', 'num', 'numa', 'nunca', 'o', 'os', 'ou', 'outra', 'outras', 'outro',
     'outros', 'para', 'pela', 'pelas', 'pelo', 'pelos', 'pequena', 'pequenas', 'pequeno', 'pequenos', 'per', 'perante',
     'pode', 'podendo', 'poder', 'poderia', 'poderiam', 'podia', 'podiam', 'pois', 'por', 'porem', 'porque', 'posso',
     'pouca', 'poucas', 'pouco', 'poucos', 'primeiro', 'primeiros', 'propria', 'proprias', 'proprio', 'proprios',
     'quais', 'qual', 'quando', 'quanto', 'quantos', 'que', 'quem', 'sao', 'se', 'seja', 'sejam', 'sem', 'sempre',
     'sendo', 'sera', 'serao', 'seu', 'seus', 'si', 'sido', 'so', 'sob', 'sobre', 'sua', 'suas', 'talvez', 'tambem',
     'tampouco', 'te', 'tem', 'tendo', 'tenha', 'ter', 'teu', 'teus', 'ti', 'tido', 'tinha', 'tinham', 'toda', 'todas',
     'todavia', 'todo', 'todos', 'tu', 'tua', 'tuas', 'tudo', 'ultima', 'ultimas', 'ultimo', 'ultimos', 'um', 'uma',
     'umas', 'uns', 'vendo', 'ver', 'vez', 'vindo', 'vir', 'vos', 'vos']

    # Stopwords do nltk + stopwords do UniLex
    stoplist = sorted(set(stoplist_uniLex + stopwords.words('portuguese')))

    def process(self, tweet):
        tweet = self.to_lower(tweet)
        tweet = self.remove_links(tweet)
        tweet = self.remove_mentions(tweet)
        tweet = self.remove_hashtags(tweet)
        tweet = self.remove_numbers(tweet)
        tweet = self.replace_three_or_more(tweet)

        palavras = self.tokenizer.tokenize(tweet)
        palavras = self.remove_punctuation(palavras)
        palavras = self.remove_stopwords(palavras)

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
        return [palavra for palavra in palavras if palavra not in self.stoplist]

    def remove_punctuation(self, palavras):
        return [palavra for palavra in palavras if palavra not in list(punctuation)]
