import sqlite3
import urllib
import urllib2
import mechanize
from bs4 import BeautifulSoup
conn = sqlite3.connect('../tweets.db')

file = open("sfzips.txt","r")

url = "http://www.melissadata.com/lookups/zipstreet.asp?InData="

for line in file.readlines():
    print line
    line = line.rstrip('\r\n')
    zip = line[:5]
    fullurl = url + zip

    resp = urllib2.urlopen(fullurl)
    html = resp.read()
    soup = BeautifulSoup(html)
    print soup
    #exit()
    table = soup.find(attrs={'class':"Tableresultborder"})
    
    rows = table.findAll('tr')
    del rows[0:2]
    #print rows
    for row in rows:
        anchors = row.findAll("a")
        for anchor in anchors:
            if len(anchor):
                street = anchor.contents[0].lstrip()
                sql = "insert into street (streetname, zip) values ('" + street + "','" + str(zip) + "')"
                conn.execute(sql)
                conn.commit()                    
    #print(soup.prettify())

conn.close()
file.close()
