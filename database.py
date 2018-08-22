import json

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, Date

class Database(object):

    user='tsap'
    password='tsap'
    host='localhost'
    port=5432
    db='tsap'

    def __init__(self):
        '''Returns a connection and a metadata object'''
        # We connect with the help of the PostgreSQL URL
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, self.db)

        # The return value of create_engine() is our connection object
        self.engine = create_engine(url, client_encoding='utf8')
        self.metadata = MetaData(self.engine)

    def create_table_tweets(self):
        # Create a table with the appropriate Columns
        self.table_tweets = Table('tweets', self.metadata,
              Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
              Column('text', String),
              Column('created_at', Date))
        # Create the above tables
        self.metadata.create_all(self.engine)

    def persist_tweet(self, raw_data):
        tweet_json = json.loads(raw_data)
        tweet = {'text': tweet_json['text'], 'created_at': tweet_json['created_at']}
        self.engine.execute(self.metadata.tables['tweets'].insert(), tweet)
