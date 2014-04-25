import urllib
import urllib2
import json
import sqlite3
import requests
import time
import twitter

class MuniScraper():
    
    def __init__(self):
        self.api = None;
        self.c = None;
    
    def login(self):
        ckey = 'REDACTED'  
        csecret = 'REDACTED'
        atoken = 'REDACTED'
        asecret = 'REDACTED'
        self.api = twitter.Api(ckey, csecret, atoken, asecret)
        return self.api
    
    def connectDB(self):
        self.c = sqlite3.connect('../tweets.db')
        
    def saveTweets(self, tweets):
        for tweet in tweets:
            tweetid = tweet['id']
            print "tweetid %s" % ( tweetid)
            ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            text = tweet['text']
            self.c.execute("INSERT INTO tweets (date,text,tweetid,tweetdata) VALUES (?,?,?,?)", [str(ts),text,tweetid,str(tweet)])
            self.c.commit() 
            
            
    
    def fetchTweetsBetween(self, bottom_id, top_id,count=200):

    
        tweets = self.api.GetUserTimeline(
                               include_entities = "false",
                                include_rts="false",
                                screen_name = "sfmta_muni",
                               since_id=bottom_id,
                               max_id = top_id,
                              count=count,
                               exclude_replies = "true",
                                trim_user="true"
                               )
    
        #url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        #r = requests.get(url, params=data)
        #print r.url
        #tweets = json.loads(r.text)
        #print tweets
        #print len(tweets)
        return tweets
    

    def getMostRecentTweet(self):
        sql = "select * from tweets order by tweetid desc limit 1"
        rs = self.c.execute(sql)
        return rs.fetchone()
  
    def fetchTweetById(self,tweetid):
        tweet = self.api.GetStatus(tweetid)
        return tweet
    