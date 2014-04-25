import urllib2
import urllib
import json
import sqlite3
import time
import string
import re
import itertools 
def findStreet(street):
    
    exclude = set(string.punctuation)
    street = ''.join(ch for ch in street if ch not in exclude)
    print "searching for :" + street
    sql = "select distinct streetname from street where streetname like '" + street + "' order by streetname asc;"
    rs = c.execute(sql)   
    results = rs.fetchall() 
    for row in results:
        print row
    return len(results)

def searchDirections(string):
    for direction in directions:
        result = re.search(direction,string,re.IGNORECASE)
        if result:
            return result


def runSplit(split, attnMatch, dirties, matches):
    ampMatch = re.search(split,attnMatch)
    matchResult = 0
    if ampMatch:                                   
        print "Found an " + split + " match: " + ampMatch.string
        exp = "(?:\S+\s)?[a-zA-Z0-9_]*"+ split + "[a-zA-Z0-9_]*(?:\s\S+)?"
        #exp = "(?\w+) &amp; (?\w+)"
        # get before and after words
        beforeafter = re.findall(exp,ampMatch.string)
        if len(beforeafter) > 0:
            # search each element against streets
            for poss in beforeafter:
                streets = poss.split()
                #search word 1
                found = 0
                if findStreet(streets[0]) > 0:
                    found = 1
                    #search word 2
                if findStreet(streets[2]) > 0:
                    found = 1                    
                if found:
                    #geocode what we found
                    matchResult = 1
                    matches.append(tweet)
    else:    
        #noamp match
        dirties.append(tweet)
        matchResult = 0
        #return dirties, matches
    return matchResult

c = sqlite3.connect('tweets.db')

#===============================================================================
# url = "https://api.twitter.com/1/statuses/user_timeline.json?include_entities=false&include_rts=false&screen_name=sfmta_muni&count=200"
# resp = urllib2.urlopen(url)
# tweets = json.loads(resp.read())
# 
# 
# c.execute("delete from tweets")
# for tweet in tweets:
#    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
#    text = tweet['text']
#    c.execute("INSERT INTO tweets VALUES (?,?)", [str(ts),text])
# c.commit()
#===============================================================================

lines = ['F','J','J Church','K','L','M','N','N Judah','T']
directions = ['southbound','northbound','eastbound','westbound']

pointWords = ['delay','blocked','delayed']
pointJoins = ['at','@']

troubleStreet = ['VAN NESS']

rs = c.execute("select tweetid, date, text from tweets where tweetid >= 194953640635662337 order by tweetid desc limit 20;")

dirties = []
noattns = []
matches = []

for row in rs:
    tweet = row[2]
    result = re.search("ATTN:",tweet,re.IGNORECASE)
    if result:
        print "Found ATTN tweet: " + result.string
        attnMatch = result.string
        split = "&amp;"
        if runSplit(split, attnMatch, dirties, matches) == 0:
            runSplit("and",attnMatch, dirties, matches)
    else:
        noattns.append(tweet)
        

print "dirties",len(dirties)
print "matches", len(matches)
print "no attns", len(noattns)

c.close()