## imports

import tweepy
from tweepy import OAuthHandler
import csv
import datetime
import time
from peewee import *

### create database

db = SqliteDatabase('twitterCrawler.db')


class SaveTweetes(Model):
    tweet_id = IntegerField(unique=True)
    date_tweet = DateTimeField()
    tweet_text = TextField( )
    tweet_retweet = IntegerField()
    tweet_likes = IntegerField()

    class Meta:
        database = db



###########################################
# code
#CRITICAL_DATA#
consumer_key = 'your-consumer_key'
consumer_secret = 'consumer_secret'
access_token = 'your-access_token'
access_secret = 'your-access_secret'

# login in tewiter api
def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.retweet_count, tweet.favorite_count]
                 for tweet in alltweets]
    # insert data to database

    insert_counter = 0
    for record in outtweets:
        try:
            newTable.create(tweet_id=record[0],
                               date_tweet=record[1],
                               tweet_text=record[2],
                               tweet_retweet=record[3],
                               tweet_likes=record[4]
                               )
            insert_counter += 1
        except IntegrityError:
            pass
    print('{} new tweed found and inserted to database.'.format(insert_counter))

    # write the csv
    # with open('%s_tweets.csv' % screen_name, 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["id","created_at","text","retweet_count","favorite_count"])
    #     writer.writerows(outtweets)

    pass


if __name__ == '__main__':
    db.connect()
    while(True):
        with open ('./acont.txt','r+')as f:
            usr=f.readlines()
            print(len(usr))
            for i in usr:
                newTable = type(i, (SaveTweetes,), {})
                print('starting to database inserting tweets from {}'.format(i))
                db.create_tables([newTable], safe=True)
                # pass in the username of the account you want to download
                get_all_tweets(i)
        time.sleep(2700)
