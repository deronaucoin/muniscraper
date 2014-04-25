import json
import urllib2
import urllib

def geocode(address):
    url = "http://maps.googleapis.com/maps/api/geocode/json"
    data = {}
    data['sensor'] = "false"
    data['address'] = address
    urldata = urllib.urlencode(data)
    fullurl = url + "?" + urldata
    resp = urllib2.urlopen(fullurl)
    result = json.loads(resp.read())
    geo = {}
    geo['status'] = result['status']
    geo['lat'] = result['results'][0]['geometry']['location']['lat']
    geo['lng'] = result['results'][0]['geometry']['location']['lng']
    geo['type'] = result['results'][0]['types'][0]
    return geo
        
if __name__=="__main__":
    result = geocode("West Portal, San Francisco, CA")
    print result