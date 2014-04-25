import urllib
import urllib2
import json
import sqlite3
import requests
import time
c = sqlite3.connect('tweets.db')

data = {}
data['include_entities'] = "false"
data['include_rts'] = "false"
data['screen_name'] ="sfmta_muni"
data['count'] = 200
data['trim_user'] = "true"
data['exclude_replies'] = "true"
data['contributor_details'] = "false"


url = "https://api.twitter.com/1/statuses/user_timeline.json"
r = requests.get(url, params=data)
tweets = json.loads(r.text)
 
# "create table tweets ( date text, text text, tweetid INTEGER, tweetdata text )"
import twitter

def login():
    ckey = 'boKNTQFwPsyJKtOabu5UA'  
    csecret = 'LLkKM39BBgvYmvGd1Q2p1cCS2uTye6P8FZovXB3rN8'
    atoken = '18793486-vtrhWb91vGfccOd1x62BZceHvEuftbYXMe0AdVh4'
    asecret = 'JZWdLMAIWcFmqKmdQOePPl8zZfen7pel91QEmChv8'
    api = twitter.Api(ckey, csecret, atoken, asecret)
    return api
 

def saveTweets(tweets):
    for tweet in tweets:
        tweetid = tweet['id']
        print "tweetid %s" % ( tweetid)
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        text = tweet['text']
        c.execute("INSERT INTO tweets (date,text,tweetid,tweetdata) VALUES (?,?,?,?)", [str(ts),text,tweetid,str(tweet)])
        c.commit() 
    
class Tweet():   
    def __init__(self, date, text, tweetid, tweetdata):
        self.date = date
        self.text = text
        self.tweetid = tweetid
        self.tweetdata = tweetdata
    
    

def getMostRecentTweet():
    sql = "select * from tweets order by tweetid desc limit 1"
    rs = c.execute(sql)
    return rs.fetchone()
  
def getOldestTweet():
    sql = "select * from tweets order by tweetid asc limit 1"
    rs = c.execute(sql)
    return rs.fetchone()
  
def getTweet(id):
    rs = c.execute("select * from tweets where tweetid = ?",[256944662621868033])
    return rs.fetchone()
    
def fetchTweetsBefore(tweetid,count=200):
    data = {}
    data['include_entities'] = "false"
    data['include_rts'] = "false"
    data['screen_name'] ="sfmta_muni"
    data['count'] = count
    data['trim_user'] = "true"
    data['exclude_replies'] = "true"
    data['contributor_details'] = "false"
    data['max_id'] = tweetid 

    url = "https://api.twitter.com/1/statuses/user_timeline.json"
    r = requests.get(url, params=data)
    #print r.url
    tweets = json.loads(r.text)
    #print tweets
    #print len(tweets)
    return tweets

def fetchTweetsSince(tweetid,count=200):
    data = {}
    data['include_entities'] = "false"
    data['include_rts'] = "false"
    data['screen_name'] ="sfmta_muni"
    data['count'] = count
    data['trim_user'] = "true"
    data['exclude_replies'] = "true"
    data['contributor_details'] = "false"
    data['since_id'] = tweetid 

    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    r = requests.get(url, params=data)
    #print r.url
    tweets = json.loads(r.text)
    #print tweets
    #print len(tweets)
    return tweets

def printTweets(tweets):
    print "# of tweets: " + str(len(tweets))
    for tweet in tweets:
        print time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')), tweet['id'], tweet['text'] 

#https://twitter.com/sfmta_muni/status/256944662621868033
    
    
    
tweet = getMostRecentTweet()
print tweet
tweets = fetchTweetsSince(tweet[2],1)
print tweets
#tweet = getOldestTweet()
#print tweet
#tweets = fetchTweetsBefore(tweet[2])
#printTweets(tweets)
#tweets = fetchTweetsBefore(tweet[2])
#del tweets[0]
#saveTweets(tweets)
#print len(tweets)
