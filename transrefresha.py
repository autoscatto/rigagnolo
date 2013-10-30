import transmissionrpc
from BeautifulSoup import BeautifulSoup
import urllib2

TRANSMISSION_IP = "127.0.0.1"
SEARCH_URL = "http://torrentz.eu/%s"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

tc = transmissionrpc.Client(address=TRANSMISSION_IP)
torrents = tc.get_torrents()

for t in torrents:
    try:
        hasha = t.hashString
        u =urllib2.Request(SEARCH_URL%hasha,"",{ 'User-Agent' : user_agent} )
        response = urllib2.urlopen(u)
        soup = BeautifulSoup(response.read())
        trackers_div = soup.find('div',{"class":'trackers'})
        trackers = [x['announce'] for x in t.trackers]
        for d in trackers_div.findAll('dt'):
            new_tracker = d.find(text=True)
            if new_tracker not in trackers:
                print "Adds %s to '%s'" %(new_tracker,t.name)
                tc.change_torrent([t.id],trackerAdd=[new_tracker])
    except:
        pass
