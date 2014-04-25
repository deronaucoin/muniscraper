import sqlite3

conn = sqlite3.connect('tweets.db')

sql = "drop table tweets"
conn.execute(sql)
sql = "create table tweets ( date text, text text, tweetid primary key, tweetdata text )"
conn.execute(sql)
#sql = "create table street (streetname,zip)"
exit()
sql = "create table incident (line, datetime, tweet, message, lat, long)"

#conn.execute(sql)

conn = sqlite3.connect('tweets.db')
sql = "select distinct streetname from street order by streetname"
sql = "select * from tweets"
rs = conn.execute(sql)
for row in rs:
    print row[0], row[1]