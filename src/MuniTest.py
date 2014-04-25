from MuniScraper import MuniScraper


muni = MuniScraper()

api = muni.login()
api.GetStatus("425422893615706112")


#print muni.fetchTweetById("425422893615706112")
exit()

muni.connectDB()

tweet = muni.getMostRecentTweet()
print tweet[2]

#tweets = muni.fetchTweetsSince('332975141975904256',2)
tweets = api.GetUserTimeline(screen_name='sfmta_muni',since_id=tweet[2],max_id=331394735845552131,count=200)
print len(tweets)
for s in tweets:
    print s.text, s.created_at, s.id