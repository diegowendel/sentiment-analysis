from twitter_client import TwitterClient

def main():
    # Creating object of TwitterClient Class
    api = TwitterClient()
    # Calling function to get tweets
    tweets = api.get_tweets(query= 'Bolsonaro', count = 200)

    # Picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # Percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

    # Picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # Percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

    # Picking negative tweets from tweets
    nttweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    # Percentage of neutral tweets
    print("Neutral tweets percentage: {} %".format(100 * len(nttweets) / len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

if __name__ == "__main__":
    # Calling main function
    main()
