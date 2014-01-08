import transmissionrpc
from BeautifulSoup import BeautifulSoup
import urllib2
from threading import Thread
from Queue import Queue


TRANSMISSION_IP = "192.168.1.3"
SEARCH_URL = "http://torrentz.eu/%s"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

tc = transmissionrpc.Client(address=TRANSMISSION_IP)
torrents = tc.get_torrents()

class Fistino(Thread):
    def __init__(self, t):
        Thread.__init__(self)
        self.t = t

    def run(self):
        try:
            hasha = self.t.hashString
            u =urllib2.Request(SEARCH_URL%hasha,"",{ 'User-Agent' : user_agent} )
            response = urllib2.urlopen(u)
            soup = BeautifulSoup(response.read())
            trackers_div = soup.find('div',{"class":'trackers'})
            trackers = [x['announce'] for x in self.t.trackers]
            for d in trackers_div.findAll('dt'):
                new_tracker = d.find(text=True)
                if new_tracker not in trackers:
                    print "Adds %s to '%s'" %(new_tracker,self.t.name)
                    tc.change_torrent([self.t.id],trackerAdd=[new_tracker])
        except:
            pass

threads = [Fistino(t) for t in torrents]
[x.start() for x in threads]
[x.join() for x in threads]


