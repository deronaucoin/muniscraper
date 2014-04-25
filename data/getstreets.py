import sqlite3
import urllib
import urllib2
from bs4 import BeautifulSoup
conn = sqlite3.connect('../tweets.db')

import os.path
COOKIEFILE = 'cookies.lwp'
COOKIEFILE = '/Users/deronaucoin/Library/Cookies/com.apple.appstore.plist'
cj = None
cookielib = None
import cookielib

file = open("sfzips.txt","r")

url = "http://www.melissadata.com/lookups/zipstreet.asp?InData="

for line in file.readlines():
    print line
    line = line.rstrip('\r\n')
    zip = line[:5]
    fullurl = url + zip
    urlopen = urllib2.urlopen
    request = urllib2.Request
    cj = cookielib.LWPCookieJar()
    true = 1
    if cj is not None:
        if true:#os.path.isfile(COOKIEFILE):
            # if we have a cookie file already saved
            # then load the cookies into the Cookie Jar
            #cj.load(COOKIEFILE)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            
            req = request(fullurl)
            #req.add_header('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
            handle = urlopen(req)
            print handle.info()
    
    exit()
    resp = urllib2.urlopen(fullurl)
    html = resp.read()
    soup = BeautifulSoup(html)
    #print soup
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
